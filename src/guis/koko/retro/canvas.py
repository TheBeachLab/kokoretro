import os
import weakref
from math import sin, cos, pi

import wx

import koko.retro.shapes.menu

from koko.retro.shapes.shape_set import ShapeSet
from koko.retro.edit_panel import EditPanel
import koko.retro.globals as globals

from themes import DARK_THEME

class Canvas(wx.Panel):
    def __init__(self, parent, callbacks, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.Bind(wx.EVT_PAINT, self.paint)
        self.Bind(wx.EVT_MOTION, self.mouse_move)
        self.Bind(wx.EVT_LEFT_DOWN, self.mouse_lclick)
        self.Bind(wx.EVT_MIDDLE_DOWN, self.mouse_mclick)
        self.Bind(wx.EVT_LEFT_DCLICK, self.mouse_dclick)
        self.Bind(wx.EVT_RIGHT_DOWN, self.show_menu)
        self.Bind(wx.EVT_LEFT_UP, self.mouse_lrelease)
        self.Bind(wx.EVT_MIDDLE_UP, self.mouse_mrelease)
        self.Bind(wx.EVT_MOUSEWHEEL, self.mouse_scroll)
        self.Bind(wx.EVT_SIZE, self.onViewChange)
        self.Bind(wx.EVT_CHAR, self.char)

        # Silly tricks to ensure that focus moves seamlessly
        # between the editor, canvas, and text boxes in the
        # edit window.
        def focus(event):
            if self.last_focus and type(self.last_focus) is wx.TextCtrl:
                self.last_focus.SetFocus()
            elif self.edit_panel:
                self.edit_panel.Hide()
                self.SetFocus()
                self.edit_panel.Show()
            else:
                self.SetFocus()
            self.last_focus = None
        def lost_focus(event):
            self.last_focus = self.FindFocus()
            self.Refresh()
        self.Bind(wx.EVT_ENTER_WINDOW, focus)
        self.Bind(wx.EVT_LEAVE_WINDOW, lost_focus)
        self.last_focus = None

        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda e: None)

        # Used for click+drag operators
        mx, my = wx.GetMousePosition()
        dx, dy = self.GetScreenPosition()
        self.click = wx.Point(mx - dx, my - dy)
        self.mouse = wx.Point(mx - dx, my - dy)

        # Image boundaries
        self.center = [0.0, 0.0]
        self.rotate = [0.0, 0.0]
        self.scale = 100.0

        # Callback to trigger a rerender
        self.view_change = callbacks['view']

        # Create a default image for the initial drawing
        width, height = self.Size
        self.image = wx.EmptyImage(*self.Size)
        self.image.view = self.view.copy()

        # Create an initial empty bitmap
        self.bitmap = wx.BitmapFromImage(self.image)
        self.bitmap.view = self.image.view.copy()

        self.dc = None

        # Interactive geometry tools
        self.shape_set = ShapeSet()
        globals.SHAPES = weakref.proxy(self.shape_set)

        self.edit_panel = None
        self.drag_target = None

        # Create an undo stack
        self.undo_stack = []
        self.push_stack(callback=False)

        # We are not unsaved at the start
        self.unsaved_callback = callbacks['unsaved']
        self.unsaved = False

        # By default, we don't show bounds
        self.show_bounds = False
        self.bounds = (0,0,0,0)

################################################################################

    @property
    def border(self):
        try:
            return self._border
        except AttributeError:
            self._border = (100, 100, 100)
            return self._border
    @border.setter
    def border(self, value):
        self._border = value
        wx.CallAfter(self.Refresh)

################################################################################

    def mouse_move(self, event):
        '''Handles a mouse move across the canvas.'''
        self.mouse = wx.Point(event.GetX(), event.GetY())

        # Drags the view around
        changed = False
        if self.drag_target is not None:
            delta = self.mouse - self.click
            self.click = self.mouse
            self.drag_target.drag(delta.x/self.scale, -delta.y/self.scale)
            self.did_drag = True
            changed = True
        else:
            x, y = self.pixel_to_pos(*self.mouse)
            r    = 5/self.scale
            if self.shape_set.check_hover(x, y, r):
                changed = True

        if changed:
            self.Refresh()

########################################

    def mouse_lclick(self, event):
        '''Records a left click event in the canvas.'''
        self.click = self.mouse

        x, y = self.pixel_to_pos(*self.mouse)
        r    = 10/self.scale

        if self.drag_target:
            self.drag_target.drop()
            self.shape_set.check_hover(x, y, r)

        self.drag_target = self.shape_set.get_target(x, y, r)
        if self.drag_target is not None:
            self.drag_target.dragging = True
            self.did_select = True
        else:
            self.did_select = False
            self.drag_target = self

        self.did_drag = False

        self.Refresh()

    def mouse_mclick(self, event):
        self.click = self.mouse
        self.drag_target = self
        self.Refresh()

    def mouse_mrelease(self, event):
        self.drag_target = None
########################################

    def mouse_dclick(self, event):
        '''Double-click to open up the point editing box.'''

        x, y = self.pixel_to_pos(*self.mouse)
        r    = 10/self.scale

        target = self.shape_set.get_target(x, y, r)
        if target is not None:
            self.open_edit_panel(target)

########################################

    def mouse_lrelease(self, event):
        '''If we just did a null click (no dragging, no selecting)
           then deselect the currently selected node.'''
        if self.did_select == False and self.did_drag == False:
            self.close_edit_panel()

        if self.drag_target:
            self.drag_target.drop()

        self.push_stack()
        self.drag_target = None

        self.Refresh()

########################################

    def mouse_scroll(self, event):
        '''Handles mouse scrolling by adjusting window scale.'''
        width, height = self.Size

        origin = ((width/2 - self.mouse[0]) / self.scale - self.center[0],
                  (self.mouse[1] - height/2) / self.scale - self.center[1])

        dScale = 1.0025
        if event.GetWheelRotation() < 0:
            dScale = 1 / dScale
        for i in range(abs(event.GetWheelRotation())):
            self.scale *= dScale
        if self.scale > (1 << 32):
            self.scale = 1 << 32

        # Reposition the center so that the point under the mouse cursor remains
        # under the mouse cursor post-zoom.
        self.center = ((width/2 - self.mouse[0]) / self.scale - origin[0],
                       (self.mouse[1] - height/2) / self.scale - origin[1])

        self.onViewChange()


    def char(self, event):
        if event.CmdDown() and event.GetKeyCode() == ord('Z'):
            if self.can_undo:
                self.undo()
        elif event.GetKeyCode() == 127:

            x, y = self.pixel_to_pos(*self.mouse)
            r    = 10/self.scale

            target = self.shape_set.get_target(x, y, r)

            if self.edit_panel and self.edit_panel.target == target:
                self.close_edit_panel()
            self.shape_set.delete(target)

            self.push_stack()
            self.Refresh()
        else:
            event.Skip()

################################################################################

    def open_edit_panel(self, target):
        '''Open an edit panel aimed at the current target.'''
        if self.edit_panel and self.edit_panel.target == target:
            return
        self.close_edit_panel()
        self.edit_panel = EditPanel(self, target)

    def close_edit_panel(self, event=None):
        '''Safely closes the edit panel, doing nothing if there
           is not an edit panel currently visible.'''
        if self.edit_panel is None:
            return
        self.edit_panel.target.selected = False
        self.edit_panel.Destroy()
        self.edit_panel = None
        self.SetFocus()

########################################

    def edit_panel_closed(self, evt):
        '''Callback when an edit panel is closed - pushes geometry
           state to the stack.'''
        self.push_stack()

################################################################################

    def show_menu(self, event):
        menu = wx.Menu()

        # Function generator to fix sneaky for loop binding problem.
        def function_wrapper(constructor):
            return lambda e: build_from(constructor)

        # Constructor to create an object at the mouse position.
        def build_from(constructor):
            mx, my = wx.GetMousePosition()
            dx, dy = self.GetScreenPosition()
            scale = 100/self.scale

            self.click = wx.Point(mx - dx, my - dy)
            self.mouse = wx.Point(mx - dx, my - dy)

            x, y = self.pixel_to_pos(mx - dx, my - dy)
            objs = constructor(x, y, scale)
            self.shape_set.add_shapes(objs)
            self.push_stack()

            self.open_edit_panel(objs[-1])
            self.drag_target = objs[-1]
            objs[-1].dragging = True

        constructors = koko.retro.shapes.menu.constructors
        for T in sorted(constructors):
            sub = wx.Menu()
            for name, constructor in sorted(constructors[T]):
                m = sub.Append(wx.ID_ANY, text=name)
                self.Bind(wx.EVT_MENU, function_wrapper(constructor), m)
            menu.AppendMenu(wx.ID_ANY, T, sub)

        menu.AppendSeparator()

        # Get the a target node to delete
        x, y = self.pixel_to_pos(*self.mouse)
        r    = 10/self.scale
        target = self.shape_set.get_target(x, y, r)

        def del_shape(evt):
            if self.edit_panel and self.edit_panel.target == target:
                self.close_edit_panel()
            self.shape_set.delete(target)

            self.push_stack()
            self.Refresh()

        delete = menu.Append(wx.ID_ANY, text='Delete')
        if target is not None:
            self.Bind(wx.EVT_MENU, del_shape, delete)
        else:
            delete.Enable(False)

        undo = menu.Append(wx.ID_ANY, text='Undo')
        if self.can_undo:
            self.Bind(wx.EVT_MENU, self.undo, undo)
        else:
            undo.Enable(False)


        self.PopupMenu(menu)

########################################

    def drag(self, dx, dy):
        ms = wx.GetMouseState()

        if 'middleIsDown' in dir(ms):
            mid = ms.cmdDown or ms.middleIsDown
        else:
            mid = ms.middleDown

        if mid:
            self.rotate = (self.rotate[0] - dx*self.scale/100.,
                           self.rotate[1] - dy*self.scale/100.)
        else:
            self.center = (self.center[0] - dx, self.center[1] - dy)
        self.onViewChange()

    def drop(self):
        pass

################################################################################

    def pos_to_pixel(self, x, y=None):
        width, height = self.Size
        xcenter, ycenter = self.center

        if y is not None:
            return ((x - xcenter) * self.scale + (width / 2.),
                     height/2. - (y - ycenter) * self.scale)
        else:
            return x*self.scale

########################################

    def pixel_to_pos(self, x, y):
        width, height = self.Size
        xcenter, ycenter = self.center

        return ((x - width/2) / self.scale + xcenter,
               (height/2 - y) / self.scale + ycenter)

################################################################################

    def get_crop(self):
        ''' Calculates a cropping rectangle to discard portions of self.image
            that do not fit into the current view. '''
        if self.image.view['xmin'] < self.view['xmin']:
            x0 = (self.image.view['pixels/unit'] *
                 (self.view['xmin'] - self.bitmap.view['xmin']))
        else:
            x0 = 0

        if self.image.view['xmax'] > self.view['xmax']:
            x1 = self.image.Width - (self.image.view['pixels/unit'] *
                 (self.image.view['xmax'] - self.view['xmax']))
        else:
            x1 = self.image.Width

        if self.image.view['ymin'] < self.view['ymin']:
            y1 = self.image.Height - (self.image.view['pixels/unit'] *
                (self.view['ymin'] - self.image.view['ymin']))
        else:
            y1 = self.image.Height

        if self.image.view['ymax'] > self.view['ymax']:
            y0 = (self.image.view['pixels/unit'] *
                  (self.image.view['ymax'] - self.view['ymax']))
        else:
            y0 = 0

        return wx.Rect(x0, y0, x1-x0, y1 - y0)

################################################################################

    def paint(self, event=None):
        '''Redraws the window.'''

        # Update the edit panel (coordinates, values, etc)
        if self.edit_panel and self.edit_panel.IsShown():
            self.edit_panel.update()

        self.dc = wx.PaintDC(self)
        self.dc.SetBackground(wx.Brush((20,20,20)))
        self.dc.Clear()

        width, height = self.Size
        xcenter, ycenter = self.center[0], self.center[1]

        if self.scale == self.image.view['pixels/unit']:
            # If the image is at the correct scale, then we're fine
            # to simply render it at its set position
            bitmap = self.bitmap
            xmin = self.image.view['xmin']
            ymax = self.image.view['ymax']
        else:
            # Otherwise, we have to rescale the image
            # (and we'll pre-emptively crop it to avoid
            #  blowing it up to a huge size)
            crop = self.get_crop()
            scale = self.scale / self.image.view['pixels/unit']
            if self.image.IsOk():
                img = self.image.Copy().GetSubImage(crop)
                img.Rescale(img.Width  * scale,
                            img.Height * scale)
                bitmap = wx.BitmapFromImage(img)

                xmin = max(self.view['xmin'], self.image.view['xmin'])
                ymax = min(self.view['ymax'], self.image.view['ymax'])

        # Draw image
        imgX, imgY = self.pos_to_pixel(xmin, ymax)
        self.dc.SetBrush(wx.Brush((0,0,0)))
        self.dc.SetPen(wx.TRANSPARENT_PEN)
        self.dc.DrawRectangle(imgX, imgY, bitmap.Width, bitmap.Height)
        self.dc.DrawBitmap(bitmap, imgX, imgY)

        # Draw bounds by fading outside region
        if self.show_bounds:
            self.draw_bounds()

        # Draw x and y axes
        self.draw_axes()

        # Draw the rest of the geometry
        self.shape_set.draw()

        # Draw border
        self.draw_border()

        self.dc = None


    def SetPen(self, *args, **kwargs):
        if type(args[0]) is wx.Pen:
            self.dc.SetPen(args[0])
        else:
            self.dc.SetPen(wx.Pen(*args, **kwargs))
    def SetBrush(self, *args, **kwargs):
        if type(args[0]) is wx.Brush:
            self.dc.SetBrush(args[0])
        else:
            self.dc.SetBrush(wx.Brush(*args, **kwargs))

################################################################################

    def draw_axes(self):

        def spin(x, y, z, alpha, beta):
            ca, sa = cos(alpha), sin(alpha)
            x, y, z = (ca*x - sa*y, sa*x + ca*y, z)

            cb, sb = cos(beta), sin(beta)
            x, y, z = (x, cb*y + sb*z, -sb*y + cb*z)

            return x, y, z

        center = self.pos_to_pixel(0, 0)
        self.dc.SetPen(wx.Pen(wx.Colour(255, 0, 0), 2))
        x, y, z = spin(50, 0, 0, -self.rotate[0], -self.rotate[1])
        self.dc.DrawLine(center[0], center[1], center[0] + x, center[1] - y)

        self.dc.SetPen(wx.Pen(wx.Colour(0, 255, 0), 2))
        x, y, z = spin(0, 50, 0, -self.rotate[0], -self.rotate[1])
        self.dc.DrawLine(center[0], center[1], center[0] + x, center[1] - y)

        self.dc.SetPen(wx.Pen(wx.Colour(0, 0, 255), 2))
        x, y, z = spin(0, 0, 50, -self.rotate[0], -self.rotate[1])
        self.dc.DrawLine(center[0], center[1], center[0] + x, center[1] - y)

    def draw_border(self):
        if self.border:
            self.dc.SetPen(wx.TRANSPARENT_PEN)
            self.dc.SetBrush(wx.Brush(self.border))

            border_width = 3
            self.dc.DrawRectangle(0, 0, self.Size[0], border_width)
            self.dc.DrawRectangle(0, self.Size[1]-border_width,
                                  self.Size[0], border_width)
            self.dc.DrawRectangle(0, 0, border_width, self.Size[1])
            self.dc.DrawRectangle(self.Size[0]-border_width, 0,
                                  border_width, self.Size[1])

    def draw_bounds(self):
        b = self.bounds
        xmin, ymin = map(int, self.pos_to_pixel(b[0], b[2]))
        xmax, ymax = map(int, self.pos_to_pixel(b[1], b[3]))


        self.dc.SetPen(wx.TRANSPARENT_PEN)
        self.dc.SetBrush(wx.Brush(wx.Colour(64, 64, 64, 128)))
        if xmin >= 0:
            self.dc.DrawRectangle(0, 0, xmin, self.Size[1])
        if xmax <= self.Size[0]:
            self.dc.DrawRectangle(xmax, 0, self.Size[0] - xmax + 1, self.Size[1])
        if ymin >= 0:
            self.dc.DrawRectangle(xmin, 0, xmax - xmin, ymax)
        if ymin <= self.Size[1]:
            self.dc.DrawRectangle(xmin, ymin, xmax - xmin, self.Size[1] - ymin + 1)

#        self.dc.DrawRectangle(-10, 0, 30, self.Size[1])
#        if xmin < 0:    xmin = 0
#        if xmin > self.Width:   xmin = self.Width
#        print xmin, ymin, xmax, ymax

################################################################################

    @property
    def view(self):
        width, height = self.Size

        xmin = self.center[0] - width/2./self.scale
        xmax = self.center[0] + width/2./self.scale
        ymin = self.center[1] - height/2./self.scale
        ymax = self.center[1] + height/2./self.scale

        return {'xmin': xmin, 'xmax': xmax,
                'ymin': ymin, 'ymax': ymax,
                'alpha': self.rotate[0],
                'beta':  self.rotate[1],
                'pixels/unit': self.scale}


    def onViewChange(self, event=None):
        '''Callback for when the window size or view changes.'''
        self.Refresh()
        self.view_change() # Run callback to rerender image

################################################################################

    def load_image(self, filename, view):
        '''Loads an image from a file.'''

        # Load the image from file and save its associated view
        self.image = wx.Image(filename)
        self.image.view = view

        # Create an initial bitmap, with the same view as the image
        if self.image.IsOk():
            self.bitmap = wx.BitmapFromImage(self.image)
            self.bitmap.view = self.image.view.copy()
            os.remove(filename)

        # Redraw the world
        self.Refresh()

    def set_image(self, img, view):
        ''' Loads a provided PIL image.'''

#        self.image = wx.EmptyImage(*img.size)
#        self.image.SetData(img.convert('RGB').tostring())
#        self.image.view = view
        self.image = img
        self.image.view = view

        self.bitmap = wx.BitmapFromImage(self.image)
        self.bitmap.view = self.image.view.copy()

        self.Refresh()

################################################################################

    def snap_bounds(self, cad):
        if not cad:
            return

        width, height = self.Size

        self.center = [cad.xmin + cad.dx/2.,
                       cad.ymin + cad.dy/2.]

        self.scale = float(min(width/cad.dx, height/cad.dy))
        self.rotate = (0, 0)
        self.onViewChange()

    def snap_axis(self, axis):
        if axis == '+x':
            self.rotate = (pi/2, 0)
        elif axis == '+y':
            self.rotate = (0, pi/2)
        elif axis == '+z':
            self.rotate = (0, 0)
        elif axis == '-x':
            self.rotate = (-pi/2, 0)
        elif axis == '-y':
            self.rotate = (0, -pi/2)
        elif axis == '-z':
            self.rotate = (pi, 0)
        self.onViewChange()

################################################################################

    @property
    def can_undo(self):
        return (len(self.undo_stack) >= 2 or
                self.shape_set.reconstructor() != self.undo_stack[-1])

########################################

    def push_stack(self, callback=True):
        shapes = self.shape_set.reconstructor()
        if self.undo_stack == [] or shapes != self.undo_stack[-1]:
            self.undo_stack.append(shapes)
            self.unsaved = True
            if callback:
                self.unsaved_callback()

########################################

    def undo(self, event=None):
        shapes = self.shape_set.reconstructor()

        # Save whoever the edit panel is pointing to - we'll
        # attempt to re-establish this connection after we reload
        # the shapes from the stack.
        if self.edit_panel:
            target = self.edit_panel.target['name'].expr
            id = [s[1]['name'] for s in shapes].index(target)
            self.close_edit_panel()
        else:
            target = None

        if shapes != self.undo_stack[-1]:
            self.shape_set.reconstruct(self.undo_stack[-1])
        elif len(self.undo_stack) >= 2:
            self.shape_set.reconstruct(self.undo_stack[-2])
            self.undo_stack = self.undo_stack[:-1]

        # Attempt to re-open the edit panel pointing at the same
        # thing.  This will fail under name changes, or if
        # the undo deletes the target point.
        if target is not None:
            try:
                self.open_edit_panel(self.shape_set[target])
            except KeyError:

                # If that failed, try to get the item in the same position
                # as the previous object - this should compensate for name
                # changes.
                try:
                    old_name = self.shape_set.reconstructor()[id][1]['name']
                except IndexError:
                    pass
                else:
                    self.open_edit_panel(self.shape_set[old_name])

        self.unsaved = True
        self.unsaved_callback()

        self.Refresh()

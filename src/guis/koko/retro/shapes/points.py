_MENU_NAME = 'Vertices'

import math
import wx

from koko.retro.shapes.core import Point
import koko.retro.globals

################################################################################


class FreePoint(Point):
    ''' A free point with x and y as parameters.

        Dragging modifies x and y directly.
    '''

    _MENU_NAME = 'Free point'

    def __init__(self, name='free_point', x=0, y=0):
        Point.__init__(self, name)
        self.create_evaluators(x=(x, float), y=(y, float))

########################################

    @staticmethod
    def new(x, y, scale=1):
        name = koko.retro.globals.SHAPES.get_name('pt')
        pt = FreePoint(name, x, y)
        return [pt]

    @property
    def _x_free(self):
        try:
            float(self['x'].expr)
            return True
        except ValueError:
            return False

    @property
    def _y_free(self):
        try:
            float(self['y'].expr)
            return True
        except ValueError:
            return False

########################################

    def draw(self, canvas):
        ''' Draws a free point on the canvas.

            The point is drawn with small handles showing the axes along
            which it can be dragged.
        '''

        x, y = canvas.pos_to_pixel(self.x, self.y)

        dark_grey   = (60, 60, 60)
        light_grey  = (100, 100, 100)


        # If the vertex is being dragged, draw small
        # arrows to show in which ways it is free
        if self.valid and (self.dragging or self.hover):

            canvas.SetPen(self.light_color if self._x_free else light_grey, 8)
            canvas.dc.DrawLine(x-10, y, x+10, y)

            canvas.SetPen(self.light_color if self._y_free else light_grey, 8)
            canvas.dc.DrawLine(x, y-10, x, y+10)

            canvas.SetPen(self.dark_color if self._x_free else dark_grey, 4)
            canvas.dc.DrawLine(x-10, y, x+10, y)

            canvas.SetPen(self.dark_color if self._y_free else dark_grey, 4)
            canvas.dc.DrawLine(x, y-10, x, y+10)

        Point.draw(self, canvas)


########################################

    def drag(self, dx, dy):
        ''' Attempts to drag the point by interpreting its x and y expressions
            as floating-point numbers then adding to each one.
        '''
        if self._x_free:
            self['x'].expr = str(float(self['x'].expr) + dx)
            self['x'].result = float(self['x'].expr)
        if self._y_free:
            self['y'].expr = str(float(self['y'].expr) + dy)
            self['y'].result = float(self['y'].expr)

################################################################################


class LinkedPoint(Point):
    ''' A linked point with a parent and an offset dx, dy.

        Calculates x and y with (parent.x + dx, parent.y + dy)

        Dragging modifies dx and dy.
    '''
    _MENU_NAME = 'Linked point'

    def __init__(self, name='linked_point', parent='', dx=0, dy=0):
        Point.__init__(self, name)
        self.create_evaluators(dx=(dx, float),
                               dy=(dy, float),
                               parent=(parent, Point))

########################################

    @staticmethod
    def new(x, y, scale=1):
        name = koko.retro.globals.SHAPES.get_name('pt')
        pt = LinkedPoint(name, '', dx=x, dy=y)
        return [pt]

    @property
    def x(self): return self.parent.x + self.dx

    @property
    def y(self): return self.parent.y + self.dy

    @property
    def _x_free(self):
        try:
            float(self['dx'].expr)
            return True
        except ValueError:
            return False

    @property
    def _y_free(self):
        try:
            float(self['dy'].expr)
            return True
        except ValueError:
            return False

########################################

    def draw(self, canvas):
        ''' Draws a linked point on the canvas.

            The point is drawn with small handles showing the axes along
            which it can be dragged.
        '''

        x, y = canvas.pos_to_pixel(self.x, self.y)

        dark_grey   = (60, 60, 60)
        light_grey  = (100, 100, 100)

        if self.valid:
            canvas.SetPen(self.dark_color, 4, wx.LONG_DASH)
            canvas.SetBrush(self.dark_color)
            self.arrow_from(self.parent)

        # If the vertex is being dragged, draw small
        # arrows to show in which ways it is free
        if self.valid and (self.dragging or self.hover):

            canvas.SetPen(self.light_color if self._x_free else light_grey, 8)
            canvas.dc.DrawLine(x-10, y, x+10, y)

            canvas.SetPen(self.light_color if self._y_free else light_grey, 8)
            canvas.dc.DrawLine(x, y-10, x, y+10)

            canvas.SetPen(self.dark_color if self._x_free else dark_grey, 4)
            canvas.dc.DrawLine(x-10, y, x+10, y)

            canvas.SetPen(self.dark_color if self._y_free else dark_grey, 4)
            canvas.dc.DrawLine(x, y-10, x, y+10)

        Point.draw(self, canvas)


########################################

    def drag(self, dx, dy):
        '''If we can add a float to x and y values, then do so;
           otherwise leave them as they are.'''
        if self._x_free:
            self['dx'].expr = str(float(self['dx'].expr) + dx)
            self['dx'].result = float(self['dx'].expr)
        if self._y_free:
            self['dy'].expr = str(float(self['dy'].expr) + dy)
            self['dy'].result = float(self['dy'].expr)

################################################################################

class PerpendicularPoint(Point):
    ''' Defines a point perpendicular to a line between two other points.

        This point can be dragged along this perpendicular.
    '''
    _MENU_NAME = 'Perpendicular vertex'

    def __init__(self, name='perp', parent='parent', perp='perp', offset=0.0):
        Point.__init__(self, name)
        self.create_evaluators(parent=(parent, Point),
                               perp=(perp, Point),
                               offset=(offset, float))

    @staticmethod
    def new(x, y, scale=1):
        name = koko.retro.globals.SHAPES.get_name('pt')
        pt = PerpendicularPoint(name, '', '', 0)
        return [pt]

    @property
    def angle(self):
        dy = self.parent.y - self.perp.y
        dx = self.parent.x - self.perp.x
        return math.atan2(dy, dx) + math.pi/2

    @property
    def x(self):
        return self.parent.x + self.offset*math.cos(self.angle)

    @property
    def y(self):
        return self.parent.y + self.offset*math.sin(self.angle)

    @property
    def _offset_free(self):
        try:    float(self['offset'].expr)
        except: return False
        else:   return True

    def drag(self, dx, dy):
        ''' Project the dragged direction onto the free
            axis of the point and slide it an appropriate amount.
        '''
        if not self._offset_free:
            return

        mag = (dx**2 + dy**2)**0.5
        angle = math.atan2(dy, dx)
        delta = mag*math.cos(angle - self.angle)
        self['offset'].expr = str(float(self['offset'].expr) + delta)
        self['offset'].result = float(self['offset'].expr)

    def draw(self, canvas):

        x, y = canvas.pos_to_pixel(self.x, self.y)

        dark_grey   = (60, 60, 60)
        light_grey  = (100, 100, 100)

        if self.valid:
            canvas.SetPen(self.dark_color, 4, wx.LONG_DASH)
            canvas.SetBrush(self.dark_color)
            self.arrow_from(self.parent)

        if self.valid and (self.dragging or self.hover):

            x0 = x - math.cos(self.angle)*10
            x1 = x + math.cos(self.angle)*10
            y0 = y + math.sin(self.angle)*10
            y1 = y - math.sin(self.angle)*10
            if self._offset_free:
                canvas.SetPen(self.light_color, 8)
                canvas.dc.DrawLine(x0, y0, x1, y1)
                canvas.SetPen(self.dark_color, 4)
                canvas.dc.DrawLine(x0, y0, x1, y1)
            else:
                canvas.SetPen(light_grey, 8)
                canvas.dc.DrawLine(x0, y0, x1, y1)
                canvas.SetPen(dark_grey, 4)
                canvas.dc.DrawLine(x0, y0, x1, y1)

        Point.draw(self, canvas)

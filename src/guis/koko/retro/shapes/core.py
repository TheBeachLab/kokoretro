import math
import inspect
import wx

from koko.retro.shapes.evaluator  import *
from koko.retro.lib.math_string   import MathString
import koko.retro.globals

################################################################################

class Primitive(object):
    '''Defines a geometric object that the user can interact with.'''

    HIDDEN_PROPERTIES = []

    def __init__(self, name='primitive'):

        self.parameters = {'name': NameEvaluator(self, name)}

        self.parents = {}
        self.children = {}

        # Variables related to user interaction.
        self.selected   = False
        self.deleted    = False
        self.dragging   = False
        self.hover      = False

        # Priority for selection (lower is more important)
        self.priority = 0

    @property
    def name(self):
        ''' Returns the primitive's name.'''
        return self.parameters['name'].eval()

    @property
    def valid(self):
        '''Returns true if all parameters are valid.'''
        return all(p.valid for p in self.parameters.itervalues())

    @property
    def modified(self):
        ''' Returns true if any parameters are modified.'''
        return any(p.modified for p in self.parameters.itervalues())

    @modified.setter
    def modified(self, value):
        ''' Sets the modified flag of each parameter to the provided value.'''
        for p in self.parameters.itervalues():
            p.modified = value

    # Child classes should redefine these to appropriate values.
    @property
    def x(self): return 0
    @property
    def y(self): return 0

    @property
    def dragging(self):
        return self._dragging
    @dragging.setter
    def dragging(self, value):
        self._dragging = value

    @property
    def hover(self):
        return self._hover
    @hover.setter
    def hover(self, value):
        self._hover = value

    def __getitem__(self, i):
        ''' Overloaded [] operator returns a parameter.'''
        return self.parameters[i]

    def drag(self, dx, dy):
        ''' This function should drag a point by the given offsets.'''
        pass

    def drop(self):
        ''' This function is called when a point is dropped.'''
        self.dragging  = False

    def reconstructor(self):
        ''' Function that defines how to reconstruct this object.

            Returns a tuple containing the object class and a
            dictionary mapping parameter names to their expressions.'''

        argspec = inspect.getargspec(self.__class__.__init__)
        args = argspec.args[1:]
        return (self.__class__,
                dict((k, self.parameters[k].expr) for k in self.parameters
                if k in args))


    def create_evaluators(self, **kwargs):
        ''' Create a set of evaluators with initial values and types.

            Arguments should be of the form
                name = (expression, type)
            e.g.
                child = ('otherPoint', Point)
                x = (12.3, float)

            The evaluators live in self.parameters, and are also added
            to the class as a property (so they can be accessed as
            self.child, self.x, etc.)
           '''

        for arg in kwargs.keys():

            # Create an evaluator with initial expression and desired type
            self.parameters[arg] = Evaluator(self, *kwargs[arg])

            # Create a property to automatically get a value from
            # the evaluator.  The lambda is a bit strange looking to
            # prevent problems with for loop variable binding.
            prop = property(lambda i, p=arg: i[p].eval())
            setattr(self.__class__, arg, prop)


    def clear_cache(self):
        ''' Clears cached evaluator results and parent/child links.'''
        self.parents = {}
        self.children = {}
        for p in self.parameters:
            self[p].cached = False


    def fill_cache(self):
        ''' Fills all evaluator caches. '''
        for p in self.parameters:
            self[p].eval()

    def draw_label(self, canvas):
        ''' Labels this node with its name.'''
        x, y = canvas.pos_to_pixel(self.x, self.y)

        canvas.dc.SetFont(wx.Font(12 + 4*self.priority,
                                  wx.FONTFAMILY_DEFAULT,
                                  wx.FONTSTYLE_NORMAL,
                                  wx.FONTWEIGHT_NORMAL))

        w, h = canvas.dc.GetTextExtent(self.name)

        canvas.SetBrush((0, 0, 0, 150))
        canvas.SetPen(wx.TRANSPARENT_PEN)
        canvas.dc.DrawRectangle(x, y - h - 10, w + 10, h+10)

        canvas.dc.SetTextForeground((255,255,255))
        canvas.dc.DrawText(self.name, x + 5, y - h - 5)

    @staticmethod
    def draw_arrow(canvas, pt1, pt2, double=False):
        ''' Draws an arrow from one node to another. '''
        x1, y1 = canvas.pos_to_pixel(pt1.x, pt1.y)
        x2, y2 = canvas.pos_to_pixel(pt2.x, pt2.y)

        angle = -math.atan2(y2-y1, x2-x1)
        size = 15

        x2 -= (5+size)*math.cos(angle)
        y2 += (5+size)*math.sin(angle)

        if double:
            x1 += (5+size)*math.cos(angle)
            y1 -= (5+size)*math.sin(angle)

        canvas.dc.DrawLine(x1, y1, x2, y2)

        x2 += size*math.cos(angle)
        y2 -= size*math.sin(angle)

        p = canvas.dc.GetPen()
        canvas.SetPen(wx.TRANSPARENT_PEN)

        shape = [(x2, y2),
                 (x2-size*math.cos(angle+math.pi/8),
                  y2+size*math.sin(angle+math.pi/8)),
                 (x2-size*math.cos(angle-math.pi/8),
                  y2+size*math.sin(angle-math.pi/8))]
        canvas.dc.DrawPolygon(shape)

        if double:
            # Draw the second arrow head
            x1 -= size * math.cos(angle)
            y1 += size * math.sin(angle)

            angle += math.pi
            shape = [(x1, y1),
                     (x1-size*math.cos(angle+math.pi/8),
                      y1+size*math.sin(angle+math.pi/8)),
                     (x1-size*math.cos(angle-math.pi/8),
                      y1+size*math.sin(angle-math.pi/8))]
            canvas.dc.DrawPolygon(shape)

        canvas.SetPen(p)


    def arrow_to(self, target):
        '''Helper function to draw an arrow to another node.'''
        Primitive.draw_arrow(koko.retro.globals.CANVAS, self, target)

    def arrow_from(self, target):
        '''Helper function to draw an arrow from another node.'''
        Primitive.draw_arrow(koko.retro.globals.CANVAS, target, self)

    def arrow_bi(self, target):
        '''Helper function to draw an arrow to/from another node.'''
        Primitive.draw_arrow(koko.retro.globals.CANVAS, self, target, double=True)

    def draw_links(self, canvas):
        ''' Draws arrows to parents and children nodes.'''

        both = self.children.keys() + self.parents.keys()
        both = filter(lambda k: k in self.children and k in self.parents,
                      both)

        for k in both:
            canvas.SetPen(k.dark_color, 4, wx.LONG_DASH)
            canvas.SetBrush(k.dark_color)
            self.arrow_bi(k, k.dark_color)

        for k in self.children:
            if k in both:
                continue
            canvas.SetPen(k.dark_color, 4, wx.LONG_DASH)
            canvas.SetBrush(k.dark_color)
            self.arrow_to(k, k.dark_color)

        for k in self.parents:
            if k in both:
                continue
            canvas.SetPen(k.dark_color, 4, wx.LONG_DASH)
            canvas.SetBrush(k.dark_color)
            self.arrow_from(k, k.dark_color)



################################################################################

class Point(Primitive):
    ''' Defines a basic point with intersect and draw functions.

        Needs to be further subclassed to actually define x, y.'''

    def __init__(self, name='point'):
        Primitive.__init__(self, name)
        self.dark_color  = (140, 140, 140)
        self.light_color = (200, 200, 200)

    def intersects(self, x, y, r):
        ''' Checks whether a circle with center (x,y) and radius r
            intersects this point.'''
        distance = ((x - self.x)**2 + (y - self.y)**2)**0.5
        return distance < r

    def draw(self, canvas):
        ''' Draws a vertex on the given canvas.

            A valid point is drawn as a circle, while an invalid vertex
            is drawn as a red X.  In each case, a highlight is drawn
            if the object is hovered, selected, or dragged.
        '''

        # Deleted vertexs should never be drawn
        if self.deleted:
            print 'Warning! draw function called from deleted vertex.'
            return

        # Find canvas-space coordinates
        x, y = canvas.pos_to_pixel(self.x, self.y)

        # Colors for an invalid point
        dark_red    = (255, 0, 0)
        light_red   = (255, 80, 60)

        # Valid vertexs are drawn as circles
        if self.valid:
            canvas.SetBrush(self.dark_color)
            if self.hover:
                canvas.SetPen(self.light_color, 4)
                canvas.dc.DrawCircle(x, y, 6)
            elif self.selected or self.dragging:
                canvas.SetPen(self.light_color, 2)
                canvas.dc.DrawCircle(x, y, 5)
            else:
                canvas.SetPen(wx.TRANSPARENT_PEN)
                canvas.dc.DrawCircle(x, y, 4)

        # Invalid vertexs are drawn as red Xs
        else:
            r = 3
            if self.hover:
                canvas.SetPen(light_red, 10)
                canvas.dc.DrawLine(x-r, y-r, x+r, y+r)
                canvas.dc.DrawLine(x-r, y+r, x+r, y-r)
            elif self.selected or self.dragging:
                canvas.SetPen(light_red, 8)
                canvas.dc.DrawLine(x-r, y-r, x+r, y+r)
                canvas.dc.DrawLine(x-r, y+r, x+r, y-r)
            canvas.SetPen(dark_red, 4)
            canvas.dc.DrawLine(x-r, y-r, x+r, y+r)
            canvas.dc.DrawLine(x-r, y+r, x+r, y-r)

################################################################################

class Shape(Primitive, MathString):
    ''' Defines a basic math-string shape.'''

    HIDDEN_PROPERTIES = ['x', 'y']

    def __init__(self, name='obj'):
        Primitive.__init__(self, name)
        self.priority = 1

        self.dark_color  = (60, 160, 255)
        self.light_color = (150, 200, 232)

        self.children = []

    @property
    def _math(self):    return '0'

    @property
    def dragging(self):
        return self._dragging
    @dragging.setter
    def dragging(self, value):
        self._dragging = value
        for p in self.parameters:
            i = self[p].eval()
            if isinstance(i, Point) and 'parent' not in i.parameters:
                i.dragging = value

    @property
    def hover(self):
        try:
            return self._hover
        except AttributeError:
            self._hover = False
        return self._hover
    @hover.setter
    def hover(self, value):
        self._hover = value
        for p in self.parameters:
            i = self[p].eval()
            if isinstance(i, Point):
                i.hover = value


    def drag(self, dx, dy):
        ''' Drag each one of the children.

            Only drags a child if it is a point without a parent parameter.
            (this is to prevent double-dragging something like a LinkedPoint.
        '''
        for c in self.parameters.itervalues():
            c = c.eval()
            if isinstance(c, Point) and 'parent' not in c.parameters:
                c.drag(dx, dy)

    def drop(self):
        self.dragging = False

    @property
    def _lines(self):
        return []

    def intersects(self, x, y, r):
        ''' Checks whether the mouse is hovering over an edge.'''
        for L in self._lines:
            if L.distance_to(x, y) < r:
                return True
        return False


    def draw(self, canvas, pen=wx.SHORT_DASH):
        ''' Draws a set of lines.'''


        lines = [canvas.pos_to_pixel(L.x0, L.y0) +
                  canvas.pos_to_pixel(L.x1, L.y1) for L in self._lines]

        canvas.SetBrush(wx.TRANSPARENT_BRUSH)

        # Draw highlight
        if self.hover or self.dragging:
            width = 6
        elif self.selected:
            width = 4
        else:
            width = 0

        if width:
            canvas.SetPen(self.light_color if self.valid else (255, 80, 60),
                          width)
            canvas.dc.DrawLineList(lines)


        if self.valid:
            canvas.SetPen(self.dark_color, 2, pen)
        else:
            canvas.SetPen((255, 0, 0), 2, pen)

        canvas.dc.DrawLineList(lines)




    class Line(object):
        ''' Simple line object used when drawing shapes.'''
        def __init__(self, x0, y0, x1, y1):
            self.L = math.sqrt((x1 - x0)**2 + (y1 - y0)**2)
            self.x0 = x0
            self.y0 = y0
            self.x1 = x1
            self.y1 = y1

            try:
                self.perp = ((y1 - y0)/self.L, -(x1 - x0)/self.L)
            except ZeroDivisionError:
                self.perp = (float('inf'), float('inf'))
            try:
                self.para = ((x1 - x0)/self.L,  (y1 - y0)/self.L)
            except ZeroDivisionError:
                self.para = (float('inf'), float('inf'))


        def distance_to(self, x, y):
            ''' Returns the distance from a line to a point.'''

            # Parallel distance from line's start
            para = -((self.x0 - x)*self.para[0] + (self.y0 - y)*self.para[1])

            if para < 0:
                return float('inf')
            if para > self.L:
                return float('inf')

            # Perpendicular distance to line
            return abs((self.x0 - x)*self.perp[0] +
                       (self.y0 - y)*self.perp[1])


################################################################################

class Transform(Shape):
    def __init__(self, name, target):
        Shape.__init__(self, name)
        self.create_evaluators(target=(target, MathString))

        self.dark_color  = (230, 197, 69)
        self.light_color = (255, 219, 77)

    def draw(self, canvas):
        Shape.draw(self, canvas, pen=wx.SHORT_DASH)

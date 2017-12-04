_MENU_NAME = '2D shapes'

import math

import wx

from koko.retro.shapes.core import Point, Shape
from koko.retro.shapes.points import *

import koko.retro.lib.shapes

import koko.retro.globals

################################################################################

class Circle(Shape):
    ''' A circle with points for center and edge.'''
    _MENU_NAME = 'Circle'

    def __init__(self, name='circle', center='c', edge='e'):
        Shape.__init__(self, name)
        self.create_evaluators(center=(center, Point),
                               edge=(edge, Point))

    @staticmethod
    def new(x, y, scale=1):
        cname = koko.retro.globals.SHAPES.get_name('center')
        ename = koko.retro.globals.SHAPES.get_name('edge')
        name  = koko.retro.globals.SHAPES.get_name('circle')

        c = FreePoint(cname, x, y)
        e = FreePoint(ename, x, y+scale)

        return [c, e, Circle(name, cname, ename)]

    @property
    def x(self): return self.center.x + self.r
    @property
    def y(self): return self.center.y

    @property
    def r(self):
        return math.sqrt((self.edge.x - self.center.x)**2 +
                         (self.edge.y - self.center.y)**2)


    @property
    def _math(self):
        return koko.retro.lib.shapes.circle(
            self.center.x, self.center.y, self.r)._math

    def intersects(self, x, y, r):
        ''' Returns true if the cursor is sufficiently close to the
            edge of the circle.'''
        R = math.sqrt((self.center.x - x)**2 +
                       (self.center.y - y)**2)
        if abs(R - self.r) < r:
            return True
        L = Shape.Line(self.center.x, self.center.y,
                       self.edge.x, self.edge.y)
        return L.distance_to(x, y) < r

    def draw(self, canvas):
        ''' Draws the circle, with a highlight if the mouse is over it.'''

        x, y = canvas.pos_to_pixel(self.center.x, self.center.y)
        r    = canvas.pos_to_pixel(self.r)

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
            canvas.SetBrush(wx.TRANSPARENT_BRUSH)
            canvas.dc.DrawCircle(x, y, r)
            canvas.dc.DrawLine(x, y, *canvas.pos_to_pixel(self.edge.x,
                                                          self.edge.y))

        if self.valid:
            canvas.SetPen(self.dark_color, 2, wx.SHORT_DASH)
        else:
            canvas.SetPen((255, 0, 0), 2, wx.SHORT_DASH)

        canvas.SetBrush(wx.TRANSPARENT_BRUSH)
        canvas.dc.DrawCircle(x, y, r)
        canvas.dc.DrawLine(x, y, *canvas.pos_to_pixel(self.edge.x,
                                                      self.edge.y))


################################################################################

class Rectangle(Shape):
    _MENU_NAME = 'Rectangle'

    def __init__(self, name='rect', cornerA='', cornerB=''):
        Shape.__init__(self, name)
        self.create_evaluators(cornerA=(cornerA, Point),
                               cornerB=(cornerB, Point))

    @staticmethod
    def new(x, y, scale=1):
        name = koko.retro.globals.SHAPES.get_name('rect')
        cAname, cBname = koko.retro.globals.SHAPES.get_name('corner', 2)
        cA = FreePoint(cAname, x, y)
        cB = FreePoint(cBname, x+scale, y+scale)

        return [cA, cB, Rectangle(name, cAname, cBname)]

    @property
    def _math(self):
        return koko.retro.lib.shapes.rectangle(self.xmin, self.xmax,
                                         self.ymin, self.ymax)._math

    @property
    def xmin(self): return min(self.cornerA.x, self.cornerB.x)
    @property
    def xmax(self): return max(self.cornerA.x, self.cornerB.x)
    @property
    def ymin(self): return min(self.cornerA.y, self.cornerB.y)
    @property
    def ymax(self): return max(self.cornerA.y, self.cornerB.y)

    @property
    def x(self): return self.xmax
    @property
    def y(self): return self.ymin

    def intersects(self, x, y, r):
        ''' Checks if a point is within a radius r of the rectangle edges.'''
        L = Shape.Line(self.xmin, self.ymin, (self.xmax+self.xmin)/2, self.ymax)

        if self.ymin-r < y < self.ymax+r:
            if abs(x - self.xmin) < r or abs(x - self.xmax) < r:
                return True
        if self.xmin-r < x < self.xmax+r:
            if abs(y - self.ymin) < r or abs(y - self.ymax) < r:
                return True
        return False

    def draw(self, canvas):
        ''' Draws the rectangle, with a highlight if the mouse is over it.'''

        xmin, ymin = canvas.pos_to_pixel(self.xmin, self.ymin)
        xmax, ymax = canvas.pos_to_pixel(self.xmax, self.ymax)

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
            canvas.dc.DrawRectangle(xmin, ymin, xmax - xmin, ymax - ymin)

        if self.valid:
            canvas.SetPen(self.dark_color, 2, wx.SHORT_DASH)
        else:
            canvas.SetPen((255, 0, 0), 2, wx.SHORT_DASH)

        canvas.dc.DrawRectangle(xmin, ymin, xmax - xmin, ymax - ymin)

################################################################################

class Triangle(Shape):
    _MENU_NAME = 'Triangle'

    def __init__(self, name, cornerA, cornerB, cornerC):
        Shape.__init__(self, name)
        self.create_evaluators(cornerA=(cornerA, Point),
                               cornerB=(cornerB, Point),
                               cornerC=(cornerC, Point))

    @staticmethod
    def new(x, y, scale=1):
        name = koko.retro.globals.SHAPES.get_name('tri')
        c1, c2, c3 = koko.retro.globals.SHAPES.get_name('corner', 3)
        C1 = FreePoint(c1, x, y)
        C2 = FreePoint(c2, x+scale, y)
        C3 = FreePoint(c3, x, y+scale)

        T = Triangle(name, c1, c2, c3)

        return [C1, C2, C3, T]

    @property
    def x(self): return (self.cornerA.x + self.cornerB.x) / 2
    @property
    def y(self): return (self.cornerA.y + self.cornerB.y) / 2


    @property
    def _math(self):
        angleA = math.atan2(self.cornerC.y - self.cornerA.y,
                            self.cornerC.x - self.cornerA.x)
        angleB = math.atan2(self.cornerC.y - self.cornerB.y,
                            self.cornerC.x - self.cornerB.x)

        if (angleA - angleB)%(2*math.pi)<math.pi:
            return koko.retro.lib.shapes.triangle(
                            self.cornerC.x, self.cornerC.y,
                            self.cornerA.x, self.cornerA.y,
                            self.cornerB.x, self.cornerB.y)._math
        else:
            return koko.retro.lib.shapes.triangle(
                            self.cornerC.x, self.cornerC.y,
                            self.cornerB.x, self.cornerB.y,
                            self.cornerA.x, self.cornerA.y)._math

    @property
    def _lines(self):
        return [Shape.Line(self.cornerA.x, self.cornerA.y,
                           self.cornerB.x, self.cornerB.y),
                Shape.Line(self.cornerB.x, self.cornerB.y,
                           self.cornerC.x, self.cornerC.y),
                Shape.Line(self.cornerC.x, self.cornerC.y,
                           self.cornerA.x, self.cornerA.y)]

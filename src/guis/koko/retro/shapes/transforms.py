_MENU_NAME = 'Transforms'

import math

from koko.retro.shapes.core import Point, Shape, Transform
from koko.retro.shapes.points import *

import koko.retro.lib.shapes

import koko.retro.globals

################################################################################
class ReflectX(Transform):
    ''' Reflection across an X coordinate.'''
    _MENU_NAME = 'Reflect X'

    def __init__(self, name='reflect', position='', target=''):
        Transform.__init__(self, name, target)
        self.create_evaluators(position=(position,Point))

    @staticmethod
    def new(x, y, scale=1):
        pname = koko.retro.globals.SHAPES.get_name('xpos')
        name  = koko.retro.globals.SHAPES.get_name('reflect')

        pt = FreePoint(pname, x, y)

        return [pt, ReflectX(name, pname, 0)]

    @property
    def _height(self):
        return 250./koko.retro.globals.CANVAS.scale

    @property
    def x(self): return self.position.x
    @property
    def y(self): return self.position.y + self._height/4

    @property
    def _math(self):
        return koko.retro.lib.shapes.reflect_x(self.target, self.x)._math

    @property
    def _lines(self):
        return [Shape.Line(self.position.x, self.position.y - self._height/2,
                           self.position.x, self.position.y + self._height/2)]

################################################################################
class ReflectY(Transform):
    ''' Reflection across an Y coordinate.'''
    _MENU_NAME = 'Reflect Y'

    def __init__(self, name='reflect', position='', target=''):
        Transform.__init__(self, name, target)
        self.create_evaluators(position=(position,Point))

    @staticmethod
    def new(x, y, scale=1):
        pname = koko.retro.globals.SHAPES.get_name('ypos')
        name  = koko.retro.globals.SHAPES.get_name('reflect')

        pt = FreePoint(pname, x, y)

        return [pt, ReflectY(name, pname, 0)]

    @property
    def _length(self):
        return 250./koko.retro.globals.CANVAS.scale

    @property
    def _lines(self):
        return [Shape.Line(self.position.x - self._length/2, self.position.y,
                           self.position.x + self._length/2, self.position.y)]

    @property
    def x(self): return self.position.x + self._length/4
    @property
    def y(self): return self.position.y

    @property
    def _math(self):
        return koko.retro.lib.shapes.reflect_y(self.target, self.y)._math

class Attract(Transform):
    ''' Attraction '''
    _MENU_NAME = 'Attract'

    def __init__(self, name='reflect', center='', radius='', target=''):
        Transform.__init__(self, name, target)
        self.create_evaluators(center=(center,Point), radius=(radius,Point))

    @property
    def r(self):
        return math.sqrt((self.radius.x - self.center.x)**2 +
                         (self.radius.y - self.center.y)**2)

    @property
    def _math(self):
        return koko.retro.lib.shapes.attract(self.target, self.r,
                                       self.x, self.y)._math

    @property
    def x(self): return self.center.x + self.r
    @property
    def y(self): return self.center.y

    @staticmethod
    def new(x, y, scale=1):
        cname = koko.retro.globals.SHAPES.get_name('center')
        rname = koko.retro.globals.SHAPES.get_name('radius')

        c = FreePoint(cname, x, y)
        r = FreePoint(rname, x + scale, y)
        s = Attract(koko.retro.globals.SHAPES.get_name('attract'),
                    cname, rname, '0')
        return [c, r, s]

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
            canvas.dc.DrawLine(x, y, *canvas.pos_to_pixel(self.radius.x,
                                                          self.radius.y))

        if self.valid:
            canvas.SetPen(self.dark_color, 2, wx.SHORT_DASH)
        else:
            canvas.SetPen((255, 0, 0), 2, wx.SHORT_DASH)

        canvas.SetBrush(wx.TRANSPARENT_BRUSH)
        canvas.dc.DrawCircle(x, y, r)
        canvas.dc.DrawLine(x, y, *canvas.pos_to_pixel(self.radius.x,
                                                      self.radius.y))


    def intersects(self, x, y, r):
        ''' Returns true if the cursor is sufficiently close to the
            edge of the circle.'''
        R = math.sqrt((self.center.x - x)**2 +
                       (self.center.y - y)**2)
        if abs(R - self.r) < r:
            return True
        L = Shape.Line(self.center.x, self.center.y,
                       self.radius.x, self.radius.y)
        return L.distance_to(x, y) < r

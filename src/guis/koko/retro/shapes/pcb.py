#_MENU_NAME = 'PCB'

import math

import wx

from koko.retro.shapes.evaluator import StrEvaluator
from koko.retro.shapes.core import Point, Shape

from koko.retro.lib.math_string import MathString
from koko.retro.lib.text import text
from koko.retro.lib.shapes import *

import koko.retro.globals

class Component(Point, MathString):
    ''' PCB component.'''

    def __init__(self, name, x, y, angle=0, value=''):
        Point.__init__(self, name)
        self.create_evaluators(x=(x, float), y=(y, float),
                               angle=(angle, float))
        self.parameters['value'] = StrEvaluator(self, value)
        self.pads = {}
        self._i = 1

        self.priority = 1

        self.light_color = (0, 255, 0)
        self.dark_color  = (0, 150, 0)

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

    def drag(self, dx, dy):
        ''' Attempts to drag the component by interpreting its x and y
            expressions as floating-point numbers then adding to each one.
        '''
        if self._x_free:
            self['x'].expr = str(float(self['x'].expr) + dx)
            self['x'].result = float(self['x'].expr)
        if self._y_free:
            self['y'].expr = str(float(self['y'].expr) + dy)
            self['y'].result = float(self['y'].expr)

    @property
    def value(self):
        return self['value'].eval()

    def add_pad(self, pad):
        ''' Adds a pad, to be looked up by number or label text.'''
        pad.parent = self
        self.pads[self._i] = pad
        self._i += 1
        if pad.label:
            self.pads[pad.label] = pad


    @property
    def _math(self):
        ''' Returns a boolean math string with pads for this IC.'''
        angle = math.radians(self.angle)
        traces = MathString('0')

        for p in set(self.pads.itervalues()):
            traces += move(rotate(p.shape, math.degrees(angle)), p.x, p.y)
        return traces._math

    def intersects(self, x, y, r):
        ''' Checks if a point is within a radius r of the rectangle edges.'''
        if (x > self.x - self.w/2  and x < self.x + self.w/2 and
            y > self.y - self.h/2  and y < self.y + self.h/2):
            return True
        else:
            return False

    def draw_label(self, canvas): pass
    def draw(self, canvas):
        ''' Draws a rectangle around the object label.'''
        x, y  = canvas.pos_to_pixel(self.x, self.y)

        canvas.SetBrush(wx.TRANSPARENT_BRUSH)

        # Draw highlight
        if self.hover or self.dragging or self.selected:
            alpha = 200
        else:
            alpha = 150


        if self.valid:
            canvas.SetBrush(self.dark_color + (alpha,))
        else:
            canvas.SetBrush((255, 0, 0) + (alpha,))


        if self.valid:
            canvas.SetPen(self.light_color, 2)
        else:
            canvas.SetPen((255, 0, 0), 2)

        mine = self.name
        if self.value:
            mine += '\n%s' % self.value

        canvas.dc.SetFont(wx.Font(16,
                                  wx.FONTFAMILY_DEFAULT,
                                  wx.FONTSTYLE_NORMAL,
                                  wx.FONTWEIGHT_NORMAL))
        canvas.dc.SetTextForeground((255,255,255))

        w, h, _ = canvas.dc.GetMultiLineTextExtent(mine)

        canvas.dc.DrawRectangle(x - w/2 - 5, y - h/2 - 5,
                                w + 10, h + 10)

        canvas.dc.DrawText(mine, x - w/2, y - h/2)

        self.w = w  / canvas.scale
        self.h = h  / canvas.scale

        canvas.dc.SetFont(wx.Font(14/560.*canvas.scale,
                                  wx.FONTFAMILY_DEFAULT,
                                  wx.FONTSTYLE_NORMAL,
                                  wx.FONTWEIGHT_NORMAL))
        canvas.dc.SetTextForeground((255,90,60))
        for p in set(self.pads.itervalues()):
            ''' Draw labels for the PCB pads '''
            if not p.label:
                continue
            p.draw(canvas)

    ########################################

    class Pad(object):
        def __init__(self, dx=0, dy=0, shape='0', label=''):
            self.dx = dx
            self.dy = dy
            self.shape = shape
            self.label = label
            self.parent = None # populated by add_pad


        @property
        def x(self):
            angle = math.radians(self.parent.angle)
            x = cos(angle)*self.dx - sin(angle)*self.dy
            return x + self.parent.x

        @property
        def y(self):
            angle = math.radians(self.parent.angle)
            y = sin(angle)*self.dx + cos(angle)*self.dy
            return y + self.parent.y

        def draw(self, canvas):
            ''' Draws an appropriately rotated pad on the canvas. '''
            x, y = canvas.pos_to_pixel(self.x, self.y)
            w, h = canvas.dc.GetTextExtent(self.label)

            if (-90 < self.parent.angle <= 90):
                angle_deg = self.parent.angle
            else:
                angle_deg = self.parent.angle - 180

            angle_rad = math.radians(angle_deg)
            x -=  math.cos(angle_rad)*w/2 + math.sin(angle_rad)*h/2
            y -= -math.sin(angle_rad)*w/2 + math.cos(angle_rad)*h/2

            canvas.dc.DrawRotatedText(self.label, x, y, angle_deg)


################################################################################

class Wire(Shape):

    _MENU_NAME = 'Wire'

    def __init__(self, name, start, mid, end, width):
        Shape.__init__(self, name)
        self.create_evaluators(start=(start, Component.Pad),
                               mid=(mid, None),
                               end=(end, Component.Pad),
                               width=(width, float))

        self.light_color = (0, 255, 0)
        self.dark_color  = (0, 150, 0)

        self.priority = 2

    @staticmethod
    def new(self, x, y, scale=1):
        name = koko.retro.globals.SHAPES.get_name('wire', minimum=1)
        return [Wire(name, '', '', '', 0.016)]

    @property
    def _lines(self):

        if self.start.parent:
            start = (self.start.x, self.start.y)
        else:
            start = (-0.5, 0)
        if self.end.parent:
            end = (self.end.x, self.end.y)
        else:
            end = (0.5, 0)

        points = [start]

        # Automagically allow single points and (x,y) tuples
        if self['mid'].expr:
            if self.mid and type(self.mid) is tuple:
                if type(self.mid[0]) is tuple or (hasattr(self.mid[0], 'x')
                                              and hasattr(self.mid[0], 'y')):
                    mid = self.mid
                else:
                    mid = (self.mid,)
            elif self.mid:
                mid = (self.mid,)
            else:
                mid = ()

            for p in mid:
                try:
                    if type(p) is tuple:
                        points += [(float(p[0]), float(p[1]))]
                    else:
                        points += [(float(p.x), float(p.y))]
                except:
                    self['mid'].valid = False
        else:
            self['mid'].valid = True
            self['mid'].result = None
        points += [end]



        diags = [Shape.Line(points[i-1][0], points[i-1][1],
                           points[i][0], points[i][1])
                for i in range(1, len(points))]
        lines = []
        for L in diags:
            if (L.x0 != L.x1):
                lines += [Shape.Line(L.x0, L.y0, L.x1, L.y0)]
            if (L.y0 != L.y1):
                lines += [Shape.Line(L.x1, L.y0, L.x1, L.y1)]
        return lines

    @property
    def x(self):
        L = self._lines
        target = L[len(L)/2]
        return (target.x0 + target.x1) / 2.
    @property
    def y(self):
        L = self._lines
        target = L[len(L)/2]
        return (target.y0 + target.y1) / 2.

    @property
    def _math(self):
        traces = '0'
        for L in self._lines:
            if (L.x0 < L.x1):
                traces += rectangle(L.x0-self.width/2,L.x1+self.width/2,
                                    L.y0-self.width/2,L.y0+self.width/2)
            elif (L.x1 < L.x0):
                traces += rectangle(L.x1-self.width/2,L.x0+self.width/2,
                                    L.y0-self.width/2,L.y0+self.width/2)
            if (L.y0 < L.y1):
                traces += rectangle(L.x1-self.width/2,L.x1+self.width/2,
                                    L.y0-self.width/2,L.y1+self.width/2)
            elif (L.y1 < L.y0):
                traces += rectangle(L.x1-self.width/2,L.x1+self.width/2,
                                    L.y1-self.width/2,L.y0+self.width/2)
        return traces._math




################################################################

##
## PCB library
##

#
# Discretes
#
_pad_1206 = rectangle(-.032,.032,-.034,.034)

class R_1206(Component):
    ''' 1206 resistor'''
    _MENU_NAME = 'Resistor (1206)'

    def __init__(self, name, x, y, angle=0, value=''):
        Component.__init__(self, name, x, y, angle, value)
        self.add_pad(Component.Pad(-0.06, 0, _pad_1206))
        self.add_pad(Component.Pad( 0.06, 0, _pad_1206))

    @staticmethod
    def new(x, y, scale=1):
        name = koko.retro.globals.SHAPES.get_name('R', minimum=1)
        return [R_1206(name, x, y)]

class C_1206(Component):
    ''' 1206 capacitor'''
    _MENU_NAME = 'Capacitor (1206)'

    def __init__(self, name, x, y, angle=0, value=''):
        Component.__init__(self, name, x, y, angle, value)
        self.add_pad(Component.Pad(-0.06, 0, _pad_1206))
        self.add_pad(Component.Pad( 0.06, 0, _pad_1206))

    @staticmethod
    def new(x, y, scale=1):
        name = koko.retro.globals.SHAPES.get_name('C', minimum=1)
        return [C_1206(name, x, y)]

_pad_XTAL_EFOBM = cube(-.016,.016,-.085,.085,0,0)
class XTAL_EFOBM(Component):
    ''' Crystal (Panasonic EFOBM series) '''
    _MENU_NAME = 'Crystal'
    def __init__(self, name, x, y, angle=0, value=''):
        Component.__init__(self, name, x, y, angle, value)
        self.add_pad(Component.Pad(-0.053, 0, _pad_XTAL_EFOBM))
        self.add_pad(Component.Pad(0, 0, _pad_XTAL_EFOBM))
        self.add_pad(Component.Pad(0.053, 0, _pad_XTAL_EFOBM))

    @staticmethod
    def new(x, y, scale=1):
        name = koko.retro.globals.SHAPES.get_name('XTAL', minimum=1)
        return [XTAL_EFOBM(name, x, y)]

#
# Microcontrollers
#
_pad_SOIC = rectangle(-.041,.041,-.015,.015)

class ATtiny45_SOIC(Component):
    ''' ATtiny45 microcontroller'''
    _MENU_NAME = "ATtiny45 (SOIC)"
    def __init__(self, name, x, y, angle=0):
        Component.__init__(self, name, x, y, angle, 't45')

        pin1 = _pad_SOIC + circle(-0.041, 0, 0.015)
        self.add_pad(Component.Pad(-0.14,  0.075, pin1, 'RST'))
        self.add_pad(Component.Pad(-0.14,  0.025, _pad_SOIC, 'PB3'))
        self.add_pad(Component.Pad(-0.14, -0.025, _pad_SOIC, 'PB4'))
        self.add_pad(Component.Pad(-0.14, -0.075, _pad_SOIC, 'GND'))
        self.add_pad(Component.Pad( 0.14, -0.075, _pad_SOIC, 'PB0'))
        self.add_pad(Component.Pad( 0.14, -0.025, _pad_SOIC, 'PB1'))
        self.add_pad(Component.Pad( 0.14,  0.025, _pad_SOIC, 'PB2'))
        self.add_pad(Component.Pad( 0.14,  0.075, _pad_SOIC, 'VCC'))

    @staticmethod
    def new(x, y, scale=1):
        name = koko.retro.globals.SHAPES.get_name('IC', minimum=1)
        return [ATtiny45_SOIC(name, x, y)]

_pad_SOICN = rectangle(-.035,.035,-.015,.015)
class ATtiny44_SOICN(Component):
    ''' ATtiny44 microcontroller'''
    _MENU_NAME = "ATtiny44 (SOIC)"
    def __init__(self, name, x, y, angle=0):
        Component.__init__(self, name, x, y, angle, 't44')
        py =  0.15
        px = -0.12

        pin1 = _pad_SOICN + circle(-0.035, 0, 0.015)
        for p in ['VCC','PB0','PB1','PB3','PB2','PA7','PA6']:
            if p == 'VCC':
                self.add_pad(Component.Pad(px, py, pin1, p))
            else:
                self.add_pad(Component.Pad(px, py, _pad_SOICN, p))
            py -= 0.05
        px =  0.12
        py += 0.05
        for p in ['PA5','PA4','PA3','PA2','PA1','PA0','GND']:
            self.add_pad(Component.Pad(px, py, _pad_SOICN, p))
            py += 0.05

    @staticmethod
    def new(x, y, scale=1):
        name = koko.retro.globals.SHAPES.get_name('IC', minimum=1)
        return [ATtiny44_SOICN(name, x, y)]

#
# Headers
#
_pad_header = rectangle(-.05,.05,-.025,.025)
class header_ISP(Component):
    ''' ISP header
        FCI 95278-101A06LF Bergstik 2x3x0.1'''
    _MENU_NAME = 'ISP header'
    def __init__(self, name, x, y, angle=0):
        Component.__init__(self, name, x, y, angle)
        self.add_pad(Component.Pad( 0.107, -0.1, _pad_header, 'MISO'))
        self.add_pad(Component.Pad(-0.107, -0.1, _pad_header, 'VCC'))
        self.add_pad(Component.Pad( 0.107,  0.0, _pad_header, 'SCK'))
        self.add_pad(Component.Pad(-0.107,  0.0, _pad_header, 'MOSI'))
        self.add_pad(Component.Pad( 0.107,  0.1, _pad_header, 'RST'))
        self.add_pad(Component.Pad(-0.107,  0.1, _pad_header, 'GND'))

    @staticmethod
    def new(x, y, scale=1):
        name = koko.retro.globals.SHAPES.get_name('J', minimum=1)
        return [header_ISP(name, x, y)]


class header_FTDI(Component):
    ''' FTDI header '''
    _MENU_NAME = 'FTDI header'

    def __init__(self, name, x, y, angle=0):
        Component.__init__(self, name, x, y, angle)
        pin1 = _pad_header + circle(-0.05, 0, 0.025)
        self.add_pad(Component.Pad(0,  0.25, pin1, 'G (blk)'))
        self.add_pad(Component.Pad(0,  0.15, _pad_header, 'CTS'))
        self.add_pad(Component.Pad(0,  0.05, _pad_header, 'VCC'))
        self.add_pad(Component.Pad(0, -0.05, _pad_header, 'TX'))
        self.add_pad(Component.Pad(0, -0.15, _pad_header, 'RX'))
        self.add_pad(Component.Pad(0, -0.25, _pad_header, 'RTS'))

    @staticmethod
    def new(x, y, scale=1):
        name = koko.retro.globals.SHAPES.get_name('J', minimum=1)
        return [header_FTDI(name, x, y)]

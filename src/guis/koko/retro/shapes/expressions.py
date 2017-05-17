import koko

from core import MathString
from points import FreePoint

_MENU_NAME = 'Expressions'

################################################################################

class Expression(FreePoint):
    ''' Defines any expression. '''

    HIDDEN_PROPERTIES = ['x', 'y']

    def __init__(self, name='obj', x=0, y=0):
        FreePoint.__init__(self, name, x, y)

        self.priority = 1

        self.dark_color  = (84, 153, 45)
        self.light_color = (127, 230, 67)

class FRepExpression(Expression, MathString):
    _MENU_NAME = 'F-Rep expression'

    def __init__(self, name, x, y, expr):
        Expression.__init__(self, name, x, y)
        self.create_evaluators(expr=(expr, MathString))

    @staticmethod
    def new(x, y, scale=1):
        name = koko.retro.globals.SHAPES.get_name('expr')

        return [FRepExpression(name, x, y, '0')]

    @property
    def _math(self):    return str(self.expr)

class FloatExpression(Expression):
    _MENU_NAME = 'Floating-point value'

    def __init__(self, name, x, y, value):
        Expression.__init__(self, name, x, y)
        self.create_evaluators(value=(value, float))

    @staticmethod
    def new(x, y, scale=1):
        name = koko.retro.globals.SHAPES.get_name('constant')

        return [FloatExpression(name, x, y, '0')]

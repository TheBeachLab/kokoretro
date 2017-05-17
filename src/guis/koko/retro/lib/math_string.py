#   koko.retro.lib.math_string.py
#   Overloaded string class for math expressions

#   Matt Keeter
#   matt.keeter@cba.mit.edu

#   kokompe.cba.mit.edu

class MathString(object):
    def __init__(self, string='0'):
        self._math = str(string)

    def __repr__(self):
        return 'MathString(%s)' % self

    def __str__(self):
        return self._math

    def __neq__(self, other):
        return not self.__eq__(other)

    def __len__(self):
        return len(str(self))

    def __or__(self, other):
        return MathString("(%s) || (%s)" % (self, other))

    def __ror__(self, other):
        return MathString("(%s) || (%s)" % (other, self))

    def __and__(self, other):
        return MathString("(%s) && (%s)" % (self, other))

    def __rand__(self, other):
        return MathString("(%s) && (%s)" % (other, self))

    def __invert__(self):
        return MathString("!(%s)" % (self))

    def __add__(self, other):
        return self | other

    def __radd__(self, other):
        return other | self

    def __sub__(self, other):
        return self & ~MathString(other)

    def __rsub__(self, other):
        return other & ~MathString(self)

    def replace(self, target, substitution):
        return MathString(str(self).replace(target, substitution))

    def map(self, x=None, y=None, z=None):
        if x is None and y is None and z is None:
            return MathString(str(self))
        return MathString('{%s%s%s%s}' % ('X:%s;'%x if x is not None else '',
                                          'Y:%s;'%y if y is not None else '',
                                          'Z:%s;'%z if z is not None else '',
                                          str(self)))

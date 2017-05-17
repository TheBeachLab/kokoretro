import re

import koko.retro.globals

class Evaluator(object):
    '''Class to do lazy evaluation of expressions.'''
    symbol_regex = re.compile('([^0-9a-zA-Z_][a-zA-Z_][0-9a-zA-Z_]*|' +
                                '\A[a-zA-Z_][0-9a-zA-Z_]*)')

    def __init__(self, parent, expr, out):
        self.parent = parent
        self.type   = out
        self._expr  = str(expr)

        # Add a default value for self.result
        self.result = None if self.type is None else self.type()

        self.valid      = False
        self.modified   = True
        self.cached     = False
        self.recursing  = False

    def symbols(self):
        return self.symbol_regex.findall(self.expr)

    def eval(self):
        '''Evaluate the given expression.

           Sets self.valid to True or False depending on whether the
           evaluation succeeded.'''

        if self.cached: return self.result

        # Prevent recursive loops (e.g. defining pt0.x = pt0.x)
        if self.recursing:
            self.valid = False
            raise RuntimeError('Bad recursion')

        # Set a few local variables
        self.recursing  = True
        self.valid      = True


        try:
            #Evaluate the magical expression
            c = eval(self._expr, {}, koko.retro.globals.SHAPES.map)
        except:
            self.valid = False
        else:
            # If we have a desired type and we got something else,
            # try to coerce the returned value into the desired type
            if self.type is not None and not isinstance(c, self.type):
                try:    c = self.type(c)
                except: self.valid = False

            # Make sure that we haven't ended up invalid
            # due to bad recursion somewhere down the line
            if self.valid: self.result = c

        # We're no longer recursing, so we can unflag the variable
        self.recursing = False

        self.cached = True
        return self.result


    @property
    def expr(self):
        return self._expr
    @expr.setter
    def expr(self, value):
        value = str(value)
        if self._expr != value:
            self.modified = True
        self._expr = value


################################################################################

class NameEvaluator(Evaluator):
    '''Class to store valid variable names.'''
    def __init__(self, parent, expr):
        Evaluator.__init__(self, parent, expr, str)

    def eval(self):
        ''' Check to see that the expression is a valid variable name
            and return it.'''
        if self.valid_regex.match(self.expr):
            self.valid = True
            self.result = self.expr
        else:
            self.valid = False
        return self.result

    valid_regex = re.compile('[a-zA-Z_][0-9a-zA-Z_]*$')

################################################################################

class StrEvaluator(Evaluator):
    '''Class to store any string.'''
    def __init__(self, parent, expr):
        Evaluator.__init__(self, parent, expr, str)
        self.valid = True

    def eval(self):
        self.result = self.expr
        return self.result

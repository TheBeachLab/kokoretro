import re
import sys

import koko.retro.globals
import math

################################################################################
class ShapeSet(object):

    class ShapeDict(object):
        def __init__(self, L):
            self.L = L

        def __getitem__(self, name):
            try:
                return getattr(math, name)
            except AttributeError:
                try:
                    return [s for s in self.L if s.name == name][0]
                except IndexError:
                    raise KeyError(name)

    def __init__(self, reconstructor=None):
        self.shapes = []
        self.map    = ShapeSet.ShapeDict(self.shapes)

        # Used by the main app to check when we have
        # to rerender the whole image.
        self.reeval_required = False
        self.modified = True

        if reconstructor is not None:
            self.reconstruct(reconstructor)

########################################

    def __getitem__(self, name):
        return self.map[name]

    def propagate_name_change(self, old, new):
        if not new:
            return
        regex = re.compile("([^a-zA-z_0-9]|\A)(%s)([^a-zA-z0-9]+|\Z)" % old)
        for s in self.shapes:
            for k in s.parameters:
                if k == 'name':
                    continue
                p = s.parameters[k]
                if re.search(regex, p.expr):
                    p.expr = re.sub(regex, '\1%s\3'%new, p.expr)[1:-1]

########################################

    def reconstructor(self):
        '''Returns a set of reconstructor objects, used to regenerate
           a set of shapes.'''
        return [s.reconstructor() for s in self.shapes]

    def to_script(self):
        ''' Returns a string that can be embedded in a script;
            this is the same as a normal reconstructor, but classes
            have been replaced by their names.'''
        r = [s.reconstructor() for s in self.shapes]
        def f(cls):
            return cls.__module__ + '.' + cls.__name__
        r = map(lambda q: (f(q[0]), q[1]), r)
        return '[' + ','.join('(%s, %s)' % q for q in r) + ']'

########################################

    def reconstruct(self, R):
        ''' Reload the set of shapes from a reconstructor object.
            Returns self.'''
        self.clear()
        for r in R:
            self.shapes += [r[0](**r[1])]

########################################

    def clear(self):
        while self.shapes:
            self.delete(self.shapes[0])

########################################

    def add_shapes(self, shapes):
        '''Adds a new shape to the shape set.'''
        self.shapes += shapes

########################################

    def delete(self, point):
        ''' Delete a particular point.'''

        if point in self.shapes:
            point.deleted = True
            point.hover = False
            point.selected = False
            self.shapes.remove(point)

            self.modified = True

########################################

    def get_name(self, prefix, count=1, minimum=0):
        '''Returns a non-colliding name with the given prefix.'''
        vals = []
        for s in self.shapes:
            try:
                vals += [int(s.name.replace(prefix,''))]
            except ValueError:
                pass

        results = []
        while len(results) < count:
            i = minimum
            while i in vals:
                i += 1
            results += ['%s%i' % (prefix, i)]
            vals    += [i]

        return results[0] if count == 1 else results

########################################

    @property
    def dict(self):
        return dict((s.name, s) for s in self.shapes)

########################################

    def check_hover(self, x, y, r):
        '''Based on mouse position, updates the hover status of points.
           Returns True if the hover status has changed, false otherwise.'''

        t = self.get_target(x, y, r)

        changed = []
        for s in self.shapes:
            if s.hover:
                changed += [s]
            s.hover = False

        if t:
            if t in changed:
                changed.remove(t)
            else:
                changed += [t]
            t.hover = True

        return changed != []

########################################

    def get_target(self, x, y, r):
        '''Returns the shape under the mouse with the lowest rank.'''
        found = []
        for s in self.shapes:
            if s.intersects(x, y, r):
                found += [s]
        if not found:
            return None
        ranks = [f.priority for f in found]
        return found[ranks.index(min(ranks))]

########################################

    @property
    def modified(self):
        return self._modified or any(s.modified for s in self.shapes)
    @modified.setter
    def modified(self, value):
        self._modified = value
        for s in self.shapes:
            s.modified = value


########################################

    def draw(self):
        '''Draws the set of shapes.'''
        if self.modified:
            self.update_cache()

#        for s in self.shapes:
#            if s.selected or s.dragging or s.hover:
#                s.draw_links(koko.retro.globals.CANVAS)

        ranked = {}
        for s in self.shapes:
            ranked[s.priority] = ranked.get(s.priority, []) + [s]
        for k in sorted(ranked.keys())[::-1]:
            for s in ranked[k]:
                s.draw(koko.retro.globals.CANVAS)

        for s in self.shapes:
            if s.hover and not s.selected:
                s.draw_label(koko.retro.globals.CANVAS)

        if self.modified:
            self.modified = False
            self.reeval_required = True


########################################

    def update_cache(self):
        self.clear_cache()
        self.fill_cache()

    def clear_cache(self):
        for s in self.shapes:
            s.clear_cache()

    def fill_cache(self):
        for s in self.shapes:
            s.fill_cache()

#   koko.retro.lib.shapes.py
#   Standard library of shapes and operations

#   Assembled by Matt Keeter (with code from Neil Gershenfeld)
#   matt.keeter@cba.mit.edu

#   kokompe.cba.mit.edu

###############################################################################

# 2D shapes:
#   circle(x0, y0, r)
#   rectangle(x0, x1, y0, y1)
#   right_triangle(x0, y0, l)
#   triangle(x0, y0, x1, y1, x2, y2) [clockwise order]
#   polygon(x, y, r, n)
#   tab(x, y, width, height, angle=0, chamfer=0.2)

# 3D shapes:
#   extrusion(part, z0, z1)
#   cylinder(x0, y0, z0, z1, r)
#   sphere(x0, y0, z0, r)
#   cube(x0, x1, y0, y1, z0, z1)
#   cone(x0, y0, z0, z1, r0)
#   pyramid(x0, x1, y0, y1, z0, z1)

# Logic operations:
#   add(part1, part2)
#   subtract(part1, part2)
#   intersect(part1, part2)
#   invert(part)

# Translation:
#   move(part, dx, dy, dz=0)

# Rotation:
#   rotate(part, angle)
#   rotate_90(part)
#   rotate_180(part)
#   rotate_270(part)
#   rotate_x(part, angle)
#   rotate_y(part, angle)
#   rotate_z(part, angle)

# Reflection:
#   reflect_x(part, x0=0)
#   reflect_y(part, y0=0)
#   reflect_z(part, z0=0)
#   reflect_xy(part)
#   reflect_xz(part)
#   reflect_yz(part)

# Scaling:
#   scale_x(part, x0, sx)
#   scale_y(part, y0, sy)
#   scale_z(part, z0, sz)
#   scale_xy(part, x0, y0, sxy)
#   scale_xyz(part, x0, y0, z0, sxyz)

# Distortion:
#   attract(part, radius=1, x0=0, y0=0, z0=0)

# Tapering:
#   taper_x_y(part, x0, y0, y1, s0, s1)
#   taper_x_z(part, x0, z0, z1, s0, s1)
#   taper_xy_z(part, x0, y0, z0, z1, s0, s1)

# Shearing:
#   shear_x_y(part, y0, y1, dx0, dx1)
#   shear_x_z(part, z0, z1, dx0, dx1)

# Color:
#   color(color,part)
#
#   Colors are implemented as an integer bit-field:
#       R = bits 0 through 7
#       G = bits 8 through 15
#       B = bits 16 through 23
#
#   The following colors are pre-defined:
#       red, green, blue, gray, white, teal, pink,
#       yellow, brown, navy, black

###############################################################################


from math_string import MathString

from math import pi, sin, cos
import re

###############################################################################
#   2D Shapes
###############################################################################
def circle(x0, y0, r):
    return MathString('(pow(X%s,2)+pow(Y%s,2) <= %g)' %
                        ('-%g' % x0 if x0 else '',
                         '-%g' % y0 if y0 else '',
                         r*r))

def rectangle(x0, x1, y0, y1):
    return MathString("((X > %g) && (X <= %g) && " % (x0, x1) +
                       "(Y > %g) && (Y <= %g))"    % (y0, y1))

def right_triangle(x, y, L):
    tri = MathString("(X <= -Y) && (X >= -{0}) && (Y >= -{0})".format(L/2.0))
    return move(tri, x + L/2.0, y + L/2.0)

def triangle(x0, y0, x1, y1, x2, y2): # points in clockwise order
    line = "({dy}*(X-{x})-({dx})*(Y-{y}) >= 0)"
    return (MathString(line.format(dy=y1-y0, x=x0, dx=x1-x0, y=y0)) &
            MathString(line.format(dy=y2-y1, x=x1, dx=x2-x1, y=y1)) &
            MathString(line.format(dy=y0-y2, x=x2, dx=x0-x2, y=y2)))

def polygon(x, y, r, n):
    if n <= 2:
        return '0'
    part = circle(0, 0, r)
    cutoff = 'Y >= -%g' % (cos(pi/n) * r)
    for i in range(n):
        part &= rotate(cutoff, i*360./n)
    return move(part, x, y)


def tab(x, y, width, height, angle = 0, chamfer = 0.2):
    tab = rectangle(-width/2, width/2, 0, height)
    cutout = triangle(width/2 - chamfer*height, height,
                      width/2, height,
                      width/2, height - chamfer*height)
    cutout = add(cutout, reflect_x(cutout))
    tab = subtract(tab, cutout)

    tab = rotate(tab, angle)
    tab = move(tab, x, y)
    return tab

def slot(x, y, width, height, angle = 0, chamfer = 0.2):
    slot = rectangle(-width/2, width/2, -height, 0)
    inset = triangle(width/2, 0,
                     width/2 + height * chamfer, 0,
                     width/2, -chamfer*height)
    inset = add(inset, reflect_x(inset))
    slot = add(slot, inset)

    slot = rotate(slot, angle)
    slot = move(slot, x, y)
    return slot

###############################################################################
#   3D Shapes
###############################################################################
def extrusion(part, z0, z1):
    return MathString("((%s) && (Z >= %g) && (Z <= %g))" % (part, z0, z1))

def cylinder(x0, y0, z0, z1, r):
    return extrusion(circle(x0, y0, r), z0, z1)

def sphere(x0, y0, z0, r):
    return move("(pow(X,2) + pow(Y,2) + pow(Z,2) <= %g)" % (r * r), x0, y0, z0)

def cube(x0, x1, y0, y1, z0, z1):
    return MathString("((X >= %g) && (X <= %g) && " % (x0, x1) +
                      " (Y >= %g) && (Y <= %g) && " % (y0, y1) +
                      " (Z >= %g) && (Z <= %g))"    % (z0, z1))

def cone(x0, y0, z0, z1, r0):
    cyl = cylinder(x0, y0, z0, z1, r0)
    return taper_xy_z(cyl, x0, y0, z0, z1, 1.0, 0.0)

def pyramid(x0, x1, y0, y1, z0, z1):
   c = cube(x0, x1, y0, y1, z0, z1)
   return taper_xy_z(c, (x0+x1)/2., (y0+y1)/2., z0, z1, 1.0, 0.0)

###############################################################################
#   Logic Operations
###############################################################################
def add(part1, part2):
    return MathString("(%s) || (%s)" % (part1, part2))

def subtract(part1, part2):
    return MathString("(%s) && !(%s)" % (part1, part2))

def intersect(part1, part2):
    return MathString("(%s) && (%s)" % (part1, part2))

def invert(part):
    return MathString("!(%s)" % part)

###############################################################################
#   Translation
###############################################################################
def move(part, dx, dy, dz = 0):
    if dx == dy == dz == 0:
        return MathString(part)
    return MathString('{%s%s%s%s}' %  ('X:X-%g;' % dx if dx else '',
                                       'Y:Y-%g;' % dy if dy else '',
                                       'Z:Z-%g;' % dz if dz else '',
                                       part))


###############################################################################
#   Rotation
###############################################################################
def rotate(part, angle):
    if angle == 0:
        return MathString(part)
    elif angle == 90:
        return rotate_90(part)
    elif angle == 180:
        return rotate_180(part)
    elif angle == 270:
        return rotate_270(part)

    angle = angle*pi/180
    newX =  '{ca}*X+{sa}*Y'.format(ca=cos(angle), sa=sin(angle))
    newY = '-{sa}*X+{ca}*Y'.format(ca=cos(angle), sa=sin(angle))

    return MathString(part).map(x=newX, y=newY)


def rotate_90(part):
    return MathString(part).map(x='Y', y='-X')

def rotate_180(part):
    return MathString(part).map(x='-X', y='-Y')

def rotate_270(part):
    return MathString(part).map(x='-Y', y='X')

def rotate_x(part, angle):
    angle = angle*pi/180
    newY =  '{ca}*Y+{sa}*Z'.format(ca=cos(angle), sa=sin(angle))
    newZ = '-{sa}*Y+{ca}*Z'.format(ca=cos(angle), sa=sin(angle))
    return MathString(part).map(y=newY, z=newZ)

def rotate_y(part, angle):
    angle = angle*pi/180
    newX =  '{ca}*X+{sa}*Z'.format(ca=cos(angle), sa=sin(angle))
    newZ = '-{sa}*X+{ca}*Z'.format(ca=cos(angle), sa=sin(angle))
    return MathString(part).map(x=newX, z=newZ)

def rotate_z(part, angle):
    return rotate(part, angle)
###############################################################################
#   Reflection
###############################################################################
def reflect_x(part, x0=0):
    if x0:
        return MathString('{X:%g-X;%s}' % (2*x0, part))
    else:
        return MathString('{X:-X;%s}' % part)

def reflect_y(part, y0=0):
    if y0:
        return MathString('{Y:%g-Y;%s}' % (2*y0, part))
    else:
        return MathString('{Y:-Y;%s}' % part)

def reflect_z(part, z0=0):
    if z0:
        return MathString('{Z:%g-Z;%s}' % (2*z0, part))
    else:
        return MathString('{Z:-Z;%s}' % part)

def reflect_xy(part):
    return MathString('{X:Y;Y:X;%s}' % part)

def reflect_xz(part):
    return MathString('{X:Z;Z:X;%s}' % part)

def reflect_yz(part):
    return MathString('{Y:Z;Z:Y;%s}' % part)

###############################################################################
#   Scaling
###############################################################################
def scale_x(part, x0, sx):
    if sx == 1:
        return MathString(part)
    if x0 == 0:
        return MathString(part).map(x='X/%g' % sx)
    newX = '{x0} + (X-{x0})/{sx}'.format(x0=x0, sx=sx)
    return MathString(part).map(x=newX)

def scale_y(part, y0, sy):
    if sy == 1:
        return MathString(part)
    if y0 == 0:
        return MathString(part).map(y='Y/%g' % sy)
    newY = '{y0} + (Y-{y0})/{sy}'.format(y0=y0, sy=sy)
    return MathString(part).map(y=newY)

def scale_z(part, z0, sz):
    if sz == 1:
        return MathString(part)
    if z0 == 0:
        return MathString(part).map(z='Z/%g' % sz)
    newZ = '{z0} + (Z-{z0})/{sz}'.format(z0=z0, sz=sz)
    return MathString(part).map(z=newZ)

def scale_xy(part, x0, y0, sxy):
    newX = '{x0} + (X-{x0})/{sxy}'.format(x0=x0, sxy=sxy)
    newY = '{y0} + (Y-{y0})/{sxy}'.format(y0=y0, sxy=sxy)
    return MathString(part).map(x=newX, y=newY)


def scale_xyz(part, x0, y0, z0, sxyz):
    newX = '{x0} + (X-{x0})/{sxyz}'.format(x0=x0, sxyz=sxyz)
    newY = '{y0} + (Y-{y0})/{sxyz}'.format(y0=y0, sxyz=sxyz)
    newZ = '{z0} + (Z-{z0})/{sxyz}'.format(z0=z0, sxyz=sxyz)
    return MathString(part).map(x=newX, y=newY, z=newZ)

###############################################################################
#   Distortion:
###############################################################################

def attract(part, radius=1, x0=0, y0=0, z0=0):
    D = 'exp(-(pow(X-{x0},2)+pow(Y-{y0},2)+pow(Z-{z0},2))/{r})'.format(
        x0=x0, y0=y0, z0=z0, r=radius)

    newX = '{x0}+(X-{x0})*(1+{r}*{D})'.format(
        x0=x0, r=radius, D=D)
    newY = '{y0}+(Y-{y0})*(1+{r}*{D})'.format(
        y0=y0, r=radius, D=D)
    newZ = '{z0}+(Z-{z0})*(1+{r}*{D})'.format(
        z0=z0, r=radius, D=D)
    return MathString(part).map(x=newX, y=newY, z=newZ)


def repel(part, radius=1, x0=0, y0=0, z0=0):
    D = 'exp(-(pow(X-{x0},2)+pow(Y-{y0},2)+pow(Z-{z0},2))/{r})'.format(
        x0=x0, y0=y0, z0=z0, r=radius)

    newX = '{x0}+(X-{x0})*(1-{r}*{D})'.format(
        x0=x0, r=radius, D=D)
    newY = '{y0}+(Y-{y0})*(1-{r}*{D})'.format(
        y0=y0, r=radius, D=D)
    newZ = '{z0}+(Z-{z0})*(1-{r}*{D})'.format(
        z0=z0, r=radius, D=D)
    return MathString(part).map(x=newX, y=newY, z=newZ)

###############################################################################
#   Tapering
###############################################################################
def taper_x_y(part, x0, y0, y1, s0, s1):
    newX = '{x0}+(X-{x0})*({y1}-{y0})/({s1}*(Y-{y0})+{s0}*({y1}-Y))'.format(
        x0=x0, y0=y0, y1=y1, s0=s0, s1=s1)
    return MathString(part).map(x=newX)

def taper_x_z(part, x0, z0, z1, s0, s1):
    newX = '{x0}+(X-{x0})*({z1}-{z0})/({s1}*(Z-{z0})+{s0}*({z1}-Z))'.format(
        x0=x0, z0=z0, z1=z1, s0=s0, s1=s1)
    return MathString(part).map(x=newX)

def taper_xy_z(part, x0, y0, z0, z1, s0, s1):
    newX = '{x0}+(X-{x0})*({z1}-{z0})/({s1}*(Z-{z0})+{s0}*({z1}-Z))'.format(
        x0=x0, z0=z0, z1=z1, s0=s0, s1=s1)
    newY = '{y0}+(Y-{y0})*({z1}-{z0})/({s1}*(Z-{z0})+{s0}*({z1}-Z))'.format(
        y0=y0, z0=z0, z1=z1, s0=s0, s1=s1)
    return MathString(part).map(x=newX, y=newY)

###############################################################################
#   Shearing
###############################################################################
def shear_x_y(part, y0, y1, dx0, dx1):
    newX = 'X-{dx0}-({dx1}-{dx0})*(Y-{y0})/({y1}-{y0})'.format(
        y0=y0, y1=y1, dx0=dx0, dx1=dx1)
    return MathString(part).map(x=newX)

def shear_x_z(part, z0, z1, dx0, dx1):
    newX = 'X-{dx0}-({dx1}-{dx0})*(Z-{z0})/({z1}-{z0})'.format(
        z0=z0, z1=z1, dx0=dx0, dx1=dx1)
    return MathString(part).map(x=newX)

###############################################################################
#   Color
###############################################################################
red     = (225 << 0)
green   = (225 << 8)
blue    = (225 << 16)
gray    = (128 << 16) + (128 << 8) + (128 << 0)
white   = (255 << 16) + (255 << 8) + (255 << 0)
teal    = (255 << 16) + (255 << 8)
pink    = (255 << 16) + (255 << 0)
yellow  = (255 << 8) + (255 << 0)
brown   = (45 << 16) + (82 << 8) + (145 << 0)
navy    = (128 << 16) + (0 << 8) + (0 << 0)
tan     = (60 << 16) + (90 << 8) + (125 << 0)
black   = 0

def color(color, part):
    return MathString('(%s * (%s))' % (color, part))

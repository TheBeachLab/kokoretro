TEMPLATE = '''from koko.retro.lib.shapes import *

# Render boundaries
cad.xmin = -1
cad.xmax = 1
cad.ymin = -1
cad.ymax = 1
cad.mm_per_unit = 25.4 # inch units

cad.function = circle(0, 0, 0.5)'''

PCB_TEMPLATE = '''from koko.retro.lib.shapes import color, tan
from koko.retro.shapes.pcb import Component, Wire

cad.mm_per_unit = 25.4 # inch units
cad.type = 'RGB'

traces = '0'
for k in locals().keys():
    c = eval(k)
    if isinstance(c, Component) or isinstance(c, Wire):
        traces += c
cad.function = color(tan, traces)
'''

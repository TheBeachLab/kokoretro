from datetime import datetime
import os
import Queue
import re
import StringIO
import subprocess
import sys
import threading
import traceback
import tempfile
from math import sin, cos

import wx


import  koko.retro.globals
from    koko.retro.shapes.shape_set import ShapeSet

from koko.retro.lib.math_string import MathString


class RenderTask(object):

    ''' A task representing a render job

        Requires a view and either [shapes and script] or cad structure
        (from a previous run).
    '''
    def __init__(self, view, shapes=[], script='', cad=None):

        self.view = view

        self.shapes = shapes
        self.script = script
        self.cad = cad

        self.event   = threading.Event()
        self.c_event = threading.Event()
        self.output = ''

        # Create a new thread to actually do the evaluation
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

########################################

    def run(self):
        ''' Evaluates the given file and loads the image into
            the canvas if evaluation was successful.'''
        start = datetime.now()

        # Clear markings from previous runs
        koko.retro.globals.CANVAS.border = None
        koko.retro.globals.FRAME.status = ''
        del koko.retro.globals.EDITOR.error_marker

        # Add the top-level header to the output pane
        self.output += '####       Rendering image      ####\n'

        # If we don't have a math dictionary, run cad_math
        if self.cad == None:
            if not self.cad_math():
                return

        # Push bounds to the global canvas object
        koko.retro.globals.CANVAS.bounds = (self.cad.xmin, self.cad.xmax,
                                      self.cad.ymin, self.cad.ymax)

        expression = self.spin(self.cad.function,
                               self.view['alpha'],
                               self.view['beta'])

        # Abort before rendering
        if self.event.is_set(): return

        self.math_png(expression)

        # Update the output pane
        self.output += "# #    Total time: %s s\n#" % (datetime.now() - start)

        if self.event.is_set(): return
        wx.CallAfter(koko.retro.globals.FRAME.set_output, self.output)

########################################

    def cad_math(self):
        ''' Returns a math dictionary generated from a shape set and script.

            In case of failure, updates UI accordingly.
        '''

        koko.retro.globals.FRAME.status = "Converting to math string"
        now = datetime.now()

        # Load variables from interactive geometry primitives
        # and a few standard include files
        vars = ShapeSet(self.shapes).dict
        exec('from string import *; from math import *', vars)
        vars['cad'] = cad_variables()

        self.output += '>>  Compiling to math file\n'

        if self.event.is_set(): return

        # Modify stdout to record messages
        buffer = StringIO.StringIO()
        sys.stdout = buffer

        try:
            exec(self.script, vars)
            vars['cad'].verify()
        except:
            # If we've failed, color the border(s) red
            koko.retro.globals.CANVAS.border = (255, 0, 0)
            if hasattr(koko.retro.globals, 'GLCANVAS'):
                koko.retro.globals.GLCANVAS.border = (255, 0, 0)

            # Figure out where the error occurred
            errors = traceback.format_exc()
            errors = errors[0] + ''.join(errors[3:])
            for m in re.findall(r'line (\d+)', errors):
                error_line = int(m)

            self.output += buffer.getvalue() + errors

            # Update the status line and add an error mark in the text editor
            try:
                koko.retro.globals.EDITOR.error_marker = error_line - 1
                koko.retro.globals.FRAME.status = \
                    "cad_math failed (line %i)" % error_line
            except NameError:
                koko.retro.globals.FRAME.status = "cad_math failed"

        else:
            # Get results from the evaluation
            self.cad = vars['cad']
            self.output += buffer.getvalue()

        # Put stdout back in place
        sys.stdout = sys.__stdout__

        dT = datetime.now() - now
        self.output += "#   cad_math time: %s \n\n" % dT

        if self.event.is_set(): return
        wx.CallAfter(koko.retro.globals.FRAME.set_output, self.output)

        # Return True if we succeeded, false otherwise.
        return self.cad != None

########################################

    def write_math(self, expression):
        '''Saves a .math file with modified bounds based from self.view'''

        text = '''format: %s
mm per unit: %f
dx dy dz: %f %f %f
xmin ymin zmin: %f %f %f
expression: %s''' %  (
        self.cad.type, self.cad.mm_per_unit,
        self.view['xmax'] - self.view['xmin'],
        self.view['ymax'] - self.view['ymin'],
        self.cad.dz,
        self.view['xmin'], self.view['ymin'], self.cad.zmin,
        expression)

        self.tmp = tempfile.NamedTemporaryFile(suffix='.math')
        self.tmp.write(text)
        self.tmp.flush()

########################################

    def spin(self, expression, alpha, beta):
        newX =  '{ca}*X-{sa}*Y'.format(ca=cos(alpha), sa=sin(alpha))
        newY = ' {sa}*X+{ca}*Y'.format(ca=cos(alpha), sa=sin(alpha))
        expression = MathString(expression).map(x=newX, y=newY)
        newY =  '{ca}*Y+{sa}*Z'.format(ca=cos(beta), sa=sin(beta))
        newZ = '-{sa}*Y+{ca}*Z'.format(ca=cos(beta), sa=sin(beta))
        expression = expression.map(y=newY, z=newZ)
        return expression

########################################

    def render_c(self, expression):
        ''' Renders an expression with the current view and math settings
            using the c solver (libtree)
        '''
        region = Region((self.view['xmin'],
                         self.view['ymin'],
                         self.cad.zmin),
                        (self.view['xmax'],
                         self.view['ymax'],
                         self.cad.zmax),
                         self.view['pixels/unit'])

        koko.retro.globals.FRAME.status = 'Rendering with libtree'
        self.output += ">>  Rendering image with libtree\n"

        start = datetime.now()
        img = expression.render(region, interrupt=self.c_event)
        dT = datetime.now() - start
        self.output += "#   libtree render time: %s \n\n" % dT

        koko.retro.globals.FRAME.status = ''
        if self.event.is_set(): return

        wx.CallAfter(koko.retro.globals.CANVAS.set_image, img.wximg, self.view)

########################################

    def math_png(self, expression):
        ''' Writes a .math file and invokes math_png. '''

        # Write the math file, with a  modified view
        self.write_math(expression)

        # Set the resolution to fill the window
        resolution = self.view['pixels/unit'] / self.cad.mm_per_unit

        if koko.retro.globals.BUNDLED:
            executable = koko.retro.globals.BASE_DIR + 'math_png'
        else:
            executable = 'math_png'
        command = [executable, self.tmp.name,
                   '_koko_tmp.png', str(resolution)]

        self.output += '>>  ' + ' '.join(command) + '\n'
        wx.CallAfter(koko.retro.globals.FRAME.set_output, self.output)
        koko.retro.globals.FRAME.status = "Parsing math string"

        # Run the subprocess
        if self.event.is_set(): return
        now = datetime.now()
        process = subprocess.Popen(command, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        success = self.monitor(process)

        if success:
            koko.retro.globals.CANVAS.border = None
            koko.retro.globals.FRAME.status = ''

            dT = datetime.now() - now
            self.output = self.output[:-1]
            self.output += "#   math_png time: %s \n\n" % dT

            if self.event.is_set(): return

            wx.CallAfter(koko.retro.globals.CANVAS.load_image,
                         '_koko_tmp.png', self.view)
        else:
            self.output += process.stderr.read()
            koko.retro.globals.CANVAS.border = (255, 0, 0)
            koko.retro.globals.FRAME.status = "math_png failed"
            print self.output


        wx.CallAfter(koko.retro.globals.FRAME.set_output, self.output)
        return success


########################################

    def monitor(self, process):
        ''' Monitors a subprocess, updating frame status based on
            render percentage completed.'''

        ########################################
        def enqueue_output(out, queue):
            ''' Helper function to read process's stdout without blocking.'''
            c = out.read(1)
            while c:
                queue.put(c)
                c = out.read(1)
        ########################################

        q = Queue.Queue()
        t = threading.Thread(target=enqueue_output,
                             args=(process.stdout, q))
        t.daemon = True
        t.start()

        line = ''
        while process.poll() is None:
            if self.event.is_set():
                process.terminate()
                process.wait()

            try:
                c = q.get_nowait()
            except Queue.Empty:
                continue

            if c == '\n' or c == '\r':
                if '[|' in line:
                    percent = (line.count('|') * 100) / (len(line) - 6)
                    if percent < 95:
                        koko.retro.globals.FRAME.status = "Rendering (%i%%)" % percent
                    else:
                        koko.retro.globals.FRAME.status = "Writing output file"
                else:
                    self.output += line+'\n'
                line = ''
            else:
                line = line + c

        # We should be happy if the process either terminated normally
        # or was killed by SIGTERM (which gives return code of -15)
        return process.returncode == 0 or process.returncode == -15

################################################################################

class cad_variables(object):
    ''' Container class to hold cad variables.'''
    def __init__(self):
        self.xmin = self.ymin = -1
        self.xmax = self.ymax = 1
        self.zmin = self.zmax = 0
        self.function = 0
        self.shapes   = []
        self.mm_per_unit = 25.4
        self.type = 'Boolean'

    def verify(self):
        ''' Attempts to coerce variables into the correct types. '''
        for i in ['xmin','xmax','ymin','ymax','zmin','zmax']:
            t = type(getattr(self, i))
            try:
                setattr(self, i, float(getattr(self, i)))
            except ValueError:
                raise TypeError('cad.%s needs to be a number, not %s'
                                % (i, t))
        self.function = MathString(self.function)
        if type(self.type) is not str:
            self.type = str(self.type)
        self.dx = self.xmax - self.xmin
        self.dy = self.ymax - self.ymin
        self.dz = self.zmax - self.zmin

    def write(self, filename):
        '''Saves a .math file.'''

        text = '''format: %s
mm per unit: %f
dx dy dz: %f %f %f
xmin ymin zmin: %f %f %f
expression: %s''' %  (
        self.type,
        self.mm_per_unit,
        self.dx, self.dy, self.dz,
        self.xmin, self.ymin, self.zmin,
        self.function)

        with open(filename,'w') as f:
            f.write(text)

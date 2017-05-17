import Queue
import shutil
import subprocess
import tempfile
import threading
import time
import os

import wx

import koko.retro.globals
import koko.retro.dialogs as dialogs

from   koko.retro.fab.path import Path

class ExportProgress(wx.Frame):
    def __init__(self, title, event):
        self.event = event
        wx.Frame.__init__(self, parent=koko.retro.globals.FRAME, title=title)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.gauge = wx.Gauge(self, wx.ID_ANY, size=(200, 20))
        hbox.Add(self.gauge, flag=wx.ALL, border=10)

        cancel = wx.Button(self, label='Cancel')
        self.Bind(wx.EVT_BUTTON, self.cancel)
        hbox.Add(cancel, flag=wx.ALL, border=10)

        self.SetSizerAndFit(hbox)
        self.Show()

    def cancel(self, event):
        self.event.set()

################################################################################

class ExportTask(object):
    ''' A task representing an export task.

        Requires a filename, cad structure, and resolution (None if irrelevant)
    '''

    def __init__(self, filename, cad, resolution=None):

        self.filename = filename
        self.extension = self.filename.split('.')[-1]
        self.cad = cad
        self.resolution = resolution

        self.event   = threading.Event()

        self.window = ExportProgress('Exporting to %s' % self.extension,
                                     self.event)

        # Create a new thread to actually do the evaluation
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()


    def run(self):
        self.cad.write('_export_tmp.math')
        if self.extension == 'math':
            shutil.move('_export_tmp.math', self.filename)
            return

        # Find the executable
        if koko.retro.globals.BUNDLED:
            executable = koko.retro.globals.BASE_DIR + 'math_' + self.extension
        else:
            executable = 'math_' + self.extension
        command = [executable, '_export_tmp.math', self.filename]
        if self.resolution is not None:
            command += [str(self.resolution)]

        # Start a subprocess
        process = subprocess.Popen(command, stdout=subprocess.PIPE)

        # And monitor the subprocess
        self.monitor(process)

        # Close the exit window
        wx.CallAfter(self.window.Destroy)

        if process.returncode == 0:
            wx.CallAfter(koko.retro.globals.FRAME.set_status, 'Export complete')
        elif process.returncode == -15:
            wx.CallAfter(koko.retro.globals.FRAME.set_status, 'Export cancelled')
        else:
            wx.CallAfter(dialogs.warning,
                         'Export failed with exit code %i' %
                          process.returncode)
        shutil.os.remove('_export_tmp.math')

    def monitor(self, process):

        def enqueue_output(out, queue):
            ''' Helper function to read process's stdout without blocking.'''
            c = out.read(1)
            while c:
                queue.put(c)
                c = out.read(1)

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
                print line
                if '[|' in line:
                    percent = (line.count('|') * 100) / (len(line) - 6)
                    wx.CallAfter(self.window.gauge.SetValue, percent)
                line = ''
            else:
                line += c

################################################################################

class FabTask(subprocess.Popen):
    def __init__(self, cad):
        self.file = tempfile.NamedTemporaryFile(suffix='.math')
        self.write_math(cad)
        self.ptime = 0
        subprocess.Popen.__init__(self, ['fab', self.file.name])

    def write_math(self, cad):
        text = '''format: %s
mm per unit: %f
dx dy dz: %f %f %f
xmin ymin zmin: %f %f %f
expression: %s''' %  (
        cad.type, cad.mm_per_unit,
        cad.dx, cad.dy, cad.dz,
        cad.xmin, cad.ymin, cad.zmin,
        cad.function)

        self.file.write(text)
        self.file.flush()

    def update(self, cad):
        self.file.seek(0)
        self.file.truncate(0)
        self.write_math(cad)

    def load_path(self):
        pname = 'fab_mod_'+os.path.basename(self.file.name).replace('.math','.path')
        if os.path.exists(pname):
            if os.path.getmtime(pname) > self.ptime:
                self.ptime = os.path.getmtime(pname)
                return Path.load(pname)
        return None

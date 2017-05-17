import cPickle as pickle
import os
import Queue
import random
import sys
import threading
import weakref

import wx

import koko.retro.globals

if '.app' in sys.argv[0]:
    koko.retro.globals.BUNDLED = True
    koko.retro.globals.BASE_DIR = os.path.abspath(os.getcwd())+'/'
    sys.path.append('')
    os.chdir(koko.retro.globals.BASE_DIR+'../../..')
else:
    koko.retro.globals.BUNDLED = False

if len(sys.argv) >= 2 and sys.argv[1] == '--video':
    koko.retro.globals.VIDEO_MODE = True
    sys.argv = [sys.argv[0]] + sys.argv[2:]
else:
    koko.retro.globals.VIDEO_MODE = False

from   koko.retro.frame import MainFrame
from   koko.retro.about import AboutBox, NAME
from   koko.retro.threadbot import ThreadBot
import koko.retro.dialogs as dialogs
import koko.retro.template


class App(wx.App):
    def OnInit(self):

        koko.retro.globals.APP = weakref.proxy(self)

        callbacks = {
            'New':               self.onNew,
            'New PCB':           self.onNewPCB,
            'Save':              self.onSave,
            'Save As':           self.onSaveAs,
            'Reload':            self.onReload,
            'Open':              self.onOpen,
            'Exit':              self.onExit,
            'About':             AboutBox,
            'Show output':       self.show_output,
            'Show script':       self.show_script,
            'Snap to bounds':    self.snap_bounds,
            'Show bounds':       self.show_bounds,
            'Re-render':         self.onTextChange,
            'saved':             lambda e=None: self.savePoint(True),
            'unsaved':           lambda e=None: self.savePoint(False),
            'text':              self.onTextChange,
            'view':              self.onViewChange,
            'idle':              self.idle,

            '.math':             self.export,
            '.png':              self.export,
            '.svg':              self.export,
            '.stl':              self.export,
            '.dot':              self.export,
            '.asdf':             self.export,
            'Start fab modules': self.start_fab,

            'koko.retro.lib.shapes':   self.show_library,
            'koko.retro.lib.text':     self.show_library,
        }
        for a in ['+x','-x','+y','-y','+z','-z']:
            callbacks[a] = self.snap_axis

        self.threadbot = ThreadBot()

        # Edit the system path to find things in the lib folder
        sys.path.append(os.path.join(sys.path[0], 'koko'))

        # Open a file from the command line
        if len(sys.argv) > 1:
            d, self.filename = os.path.split(sys.argv[1])
            self.directory = os.path.abspath(d)
        else:
            self.filename = ''
            self.directory = os.getcwd()

        # Create frame
        self.frame = MainFrame(callbacks)
        koko.retro.globals.FRAME = weakref.proxy(self.frame)

        if self.filename:
            self.load()

        # Update the window title
        self.savePoint(True)

        self.reeval_required = True
        self.render_required = True

        # first_render causes the snaps the view to the cad file bounds.
        self.first_render = True

        # Show the application!
        self.frame.Show()
        self.frame.canvas.SetFocus()

        # Render for the first time
        self.onTextChange()

        return True

    @property
    def directory(self):
        return self._directory
    @directory.setter
    def directory(self, value):
        try:
            sys.path.remove(self._directory)
        except (AttributeError, ValueError):
            pass
        self._directory = value
        if self.directory != '':
            os.chdir(self.directory)
            sys.path.append(self.directory)

################################################################################

    def savePoint(self, value):
        '''Callback when a save point is reached in the editor.'''

        self.saved = value and not self.frame.canvas.unsaved

        s = '%s:  ' % NAME
        if self.filename:
            s += self.filename
        else:
            s += '[Untitled]'

        if not self.saved:
            s += '*'

        self.frame.SetTitle(s)


################################################################################

    def onNew(self, evt=None):
        '''Creates a new file from the default template.'''
        if self.saved or dialogs.warn_changes():
            self.filename = ''
            self.threadbot.reset()

            koko.retro.globals.EDITOR.text = koko.retro.template.TEMPLATE

            if koko.retro.globals.CANVAS.edit_panel:
                koko.retro.globals.CANVAS.close_edit_panel()

            koko.retro.globals.SHAPES.clear()

            self.first_render = True

################################################################################

    def onNewPCB(self, evt=None):
        '''Creates a new file from the PCB template.'''
        if self.saved or dialogs.warn_changes():
            self.filename = ''

            koko.retro.globals.EDITOR.text = koko.retro.template.PCB_TEMPLATE

            if koko.retro.globals.CANVAS.edit_panel:
                koko.retro.globals.CANVAS.close_edit_panel()

            koko.retro.globals.SHAPES.clear()

            self.first_render = True

################################################################################

    def onSave(self, evt=None):
        '''Save callback from main menu.'''

        # If we don't have a filename, perform Save As instead
        if self.filename == '':
            self.onSaveAs()
        elif '.ko' in self.filename:
            dialogs.warning('''The .ko file extension is deprecated.
The file should be saved as a .cad file.
Please pick a new filename''')
            self.onSaveAs()
            return
        else:
            # Write out the file
            path = os.path.join(self.directory, self.filename)

            text = self.frame.editor.text
            if self.frame.canvas.shape_set.reconstructor() != []:
                text = ('''##    Geometry header    ##
import koko
reconstructor = %s
ss = koko.retro.shapes.shape_set.ShapeSet()
koko.retro.globals.SHAPES = ss
ss.reconstruct(reconstructor)
locals().update(ss.dict)
##    End of geometry header    ##

''' % self.frame.canvas.shape_set.to_script()) + text

            with open(path, 'w') as f:
                f.write(text)

            # Tell the canvas and editor that we've saved
            # (this invokes the callback to change title text)
            self.frame.canvas.unsaved = False
            self.frame.editor.SetSavePoint()

            # Update the status box.
            self.frame.status = 'Saved file %s' % self.filename

################################################################################

    def onSaveAs(self, evt=None):
        '''Save As callback from main menu.'''

        # Open a file dialog to get target
        df = dialogs.save_as(self.directory, extension='.cad')

        if df[1] != '':
            self.directory, self.filename = df
            self.onSave()

################################################################################

    def onReload(self, evt=None):
        '''Reloads the current file, warning if necessary.'''
        if self.filename != ''  and (self.saved or dialogs.warn_changes()):
            self.load()
            self.first_render = False

################################################################################

    def load(self):
        '''Loads text from the current file.'''

        # Forget the old math file
        self.threadbot.reset()

        path = os.path.join(self.directory, self.filename)

        self.frame.canvas.shape_set.clear()
        if self.frame.canvas.edit_panel:
            self.frame.canvas.close_edit_panel()
        self.frame.canvas.Refresh()

        # Try to load a pickled .ko file
        try:
            with open(path, 'rb') as f:
                data = pickle.load(f)
        # Otherwise, open it as a .cad file
        except:
            with open(path, 'r') as f:
                text = f.read()
            if text.split('\n')[0] == '##    Geometry header    ##':
                reconstructor = eval(text.split('\n')[2][16:])
                text = '\n'.join(text.split('\n')[9:])
                koko.retro.globals.SHAPES.reconstruct(reconstructor)
            self.frame.editor.text = text
            self.frame.status = 'Loaded .cad file'
        # Reconstruct the pickled file
        else:
            self.frame.editor.text = data['text']
            koko.retro.globals.SHAPES.reconstruct(data['shapes'])
            self.frame.status = 'Loaded .ko file'

        self.frame.canvas.unsaved = False
        self.first_render = True


################################################################################

    def onOpen(self, evt=None):
        ''' Open callback from main menu.'''
        # Open a file dialog to get target
        if self.saved or dialogs.warn_changes():
            df = dialogs.open_file(self.directory)
            if df[1] != '':
                self.directory, self.filename = df
                self.load()

################################################################################

    def onExit(self, evt=None):
        '''Exits after warning of unsaved changes.'''
        if self.saved or dialogs.warn_changes():
            self.frame.Destroy()

################################################################################

    def show_output(self, evt):
        if evt.Checked():
            self.frame.show_output()
        else:
            self.frame.hide_output()

################################################################################

    def show_script(self, evt):
        if evt.Checked():
            self.frame.show_script()
        else:
            self.frame.hide_script()

################################################################################

    def snap_bounds(self, evt=None):
        self.frame.canvas.snap_bounds(self.threadbot.cached_cad)

    def show_bounds(self, evt=None):
        self.frame.canvas.show_bounds = evt.Checked()
        self.frame.canvas.Refresh()

    def snap_axis(self, evt=None):
        item = self.frame.GetMenuBar().FindItemById(evt.GetId())
        self.frame.canvas.snap_axis(item.GetLabel())

################################################################################

    def onTextChange(self, evt=None):
        # Mark that we need to run cad_math again
        self.reeval_required = True

        # Set a syntax hint in the frame
        self.frame.hint = self.frame.editor.syntax_helper()

    def onViewChange(self):
        self.render_required = True

################################################################################

    def idle(self, evt=None):

        # Check the threads and clear out any that are dead
        self.threadbot.join_threads()

        # Re-evaluate the geometry if necessary.  This may lead to
        # a full expression re-eval.
        if koko.retro.globals.SHAPES.reeval_required:
            self.reeval_required = True
            koko.retro.globals.SHAPES.reeval_required = False

        # Snap the bounds to the math file if this was the first render.
        if self.threadbot.cached_cad and self.first_render:
            self.frame.canvas.snap_bounds(self.threadbot.cached_cad)
            self.first_render = False
            self.reeval_required = True

        # We can't render until we have a valid math file
        if self.render_required and not self.threadbot.cached_cad:
            self.render_required = False
            self.reeval_required = True

        # Recalculate math file then render
        if self.reeval_required:
            self.reeval_required = False
            self.render_required = False
            self.reeval()

        # Render given valid math file
        if self.render_required:
            self.render_required = False
            self.render()


################################################################################

    def render(self):
        ''' Render the image, given the existing math file.'''

        # Start up a new thread to render and load the image.
        if koko.retro.globals.CANVAS.IsShown():
            self.threadbot.render(koko.retro.globals.CANVAS.view)

    def reeval(self):
        ''' Render the image, calculating a new math file.'''

        if koko.retro.globals.CANVAS.IsShown():
            self.threadbot.render(koko.retro.globals.CANVAS.view,
                                  shapes=koko.retro.globals.SHAPES.reconstructor(),
                                  script=koko.retro.globals.EDITOR.text)
        else:
            self.threadbot.glrender(shapes=koko.retro.globals.SHAPES.reconstructor(),
                                  script=koko.retro.globals.EDITOR.text)


################################################################################

    def export(self, event):
        ''' General-purpose export callback.  Decides which export
            command to call based on the menu item text.'''

        item = self.frame.GetMenuBar().FindItemById(event.GetId())
        filetype = item.GetLabel()

        if 'failed' in koko.retro.globals.FRAME.status:
            dialogs.warning('Design has errors!  Export failed.')
            return
        elif self.threadbot.cached_cad is None:
            dialogs.warning('Design needs to be rendered before exporting!  Export failed')
            return

        resolution = None
        if filetype in ['.png', '.svg', '.stl']:
            resolution = dialogs.resolution(10, cad=self.threadbot.cached_cad)
            if resolution is False:
                return

        df = dialogs.save_as(self.directory, extension=filetype)
        if df[1] == '':
            return
        path = os.path.join(*df)

        self.threadbot.export(path, resolution)

################################################################################

    def start_fab(self, event=None):
        ''' Starts the fab modules.'''
        self.threadbot.start_fab()

################################################################################

    def show_library(self, event):

        item = self.frame.GetMenuBar().FindItemById(event.GetId())
        name = item.GetLabel()

        if koko.retro.globals.BUNDLED:
            path = koko.retro.globals.BASE_DIR + name.split('.')[-1] + '.py'
        else:
            v = {}
            exec('import %s as module' % name.replace('koko.',''), v)
            path = v['module'].__file__.replace('.pyc','.py')

        dialogs.TextFrame(self.frame, name, path)

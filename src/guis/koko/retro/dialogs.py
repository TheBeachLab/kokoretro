import wx

import koko.retro.editor
from koko.retro.themes import DARK_THEME

def warn_changes():
    '''Check to see if the user is ok with abandoning unsaved changes.
       Returns True if we should proceed.'''
    dlg = wx.MessageDialog(None, "All unsaved changes will be lost.",
                           "Warning:",
                           wx.OK | wx.CANCEL | wx.ICON_EXCLAMATION)
    result = dlg.ShowModal()
    dlg.Destroy()
    return result == wx.ID_OK

################################################################################

def warning(text):
    '''General-purpose warning box.'''
    message(text, "Warning:", wx.ICON_WARNING)

def message(text, title, icon = 0):
    dlg = wx.MessageDialog(None, text, title, wx.OK | icon)
    dlg.ShowModal()
    dlg.Destroy()

################################################################################

def save_as(directory, filename='', extension='.*'):
    '''Prompts a Save As dialog, returning directory, filename.'''

    dlg = wx.FileDialog(None, "Choose a file",
                        directory, '', '*%s' % extension,
                        wx.FD_SAVE)

    if dlg.ShowModal() == wx.ID_OK:
        directory, filename = dlg.GetDirectory(), dlg.GetFilename()

    dlg.Destroy()
    return directory, filename

################################################################################

def open_file(directory, filename=''):
    '''Prompts an Open dialog, returning directory, filename.'''
    dlg = wx.FileDialog(None, "Choose a file", directory, style=wx.FD_OPEN)

    if dlg.ShowModal() == wx.ID_OK:
        directory, filename = dlg.GetDirectory(), dlg.GetFilename()

    dlg.Destroy()
    return directory, filename

################################################################################

class ResolutionDialog(wx.Dialog):
    def __init__(self, res, title, cad=None):
        wx.Dialog.__init__(self, parent=None, title=title)
        self.cad = cad

        self.value = wx.TextCtrl(self, -1, style=wx.TE_PROCESS_ENTER)

        self.value.Bind(wx.EVT_CHAR, self.limit_to_numbers)
        self.value.Bind(wx.EVT_TEXT, self.update_dimensions)
        self.value.Bind(wx.EVT_TEXT_ENTER, self.done)

        self.value.ChangeValue(str(res))

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.value, flag=wx.ALL, border=10)
        okButton = wx.Button(self, label='OK')
        okButton.Bind(wx.EVT_BUTTON, self.done)
        hbox.Add(okButton, flag=wx.ALL, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(wx.StaticText(self, wx.ID_ANY, 'Resolution (pixels/mm):'),
                               flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(hbox)
        self.dimensions = wx.StaticText(self, wx.ID_ANY, '')
        vbox.Add(self.dimensions, flag=wx.LEFT | wx.BOTTOM, border=10)

        self.update_dimensions()
        self.SetSizerAndFit(vbox)


    def limit_to_numbers(self, event=None):
        valid = '0123456789'
        if not '.' in self.value.GetValue():
            valid += '.'

        keycode = event.GetKeyCode()
        if keycode < 32 or keycode >= 127 or chr(keycode) in valid:
            event.Skip()

    def update_dimensions(self, event=None):
        if self.cad:
            try:
                scale = float(self.value.GetValue()) * self.cad.mm_per_unit
            except ValueError:
                label = '0 x 0 x 0'
            else:
                label = '%i x %i x %i' % (max(1, self.cad.dx*scale),
                                          max(1, self.cad.dy*scale, 1),
                                          max(1, self.cad.dz*scale, 1))
            self.dimensions.SetLabel(label)

    def done(self, event):
        self.result = self.value.GetValue()
        try:
            float(self.result)
        except ValueError:
            self.EndModal(wx.ID_CANCEL)
        else:
            self.EndModal(wx.ID_OK)


def resolution(resolution, title='Export', cad=None):
    '''Create a resolution dialog and return the result.'''
    dlg = ResolutionDialog(resolution, title, cad)
    if dlg.ShowModal() == wx.ID_OK:
        resolution = dlg.result
    else:
        resolution = False
    dlg.Destroy()
    return resolution

################################################################################

class TextFrame(wx.Frame):
    '''A simple text frame to display the contents of a file
       or software-defined text.'''
    def __init__(self, parent, title, filename=None):
        wx.Frame.__init__(self, parent, title=title)

        # Create text pane.
        self.txt = koko.retro.editor.Editor(self, margins=False, style=wx.NO_BORDER,
                                 size=(600, 400))
        self.txt.SetCaretLineVisible(0)
        self.txt.SetReadOnly(True)

        if filename is not None:
            with open(filename, 'r') as f:
                self.txt.text = f.read()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.txt, 1, wx.EXPAND | wx.ALL, border=5)
        self.SetSizerAndFit(sizer)

        DARK_THEME.apply(self)
        self.Show()

    @property
    def text(self):
        return self.txt.text
    @text.setter
    def text(self, value):
        self.txt.text = value

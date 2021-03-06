""" Module containing various wxPython dialogs. """
import  wx

import  koko
import  koko.editor
from    koko.themes import DARK_THEME

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

def error(text):
    '''General-purpose warning box.'''
    message(text, "Error:", wx.ICON_ERROR)

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
    ''' Dialog box that allows users to set resolution

        Also includes an extra checked box with caller-defined
        label. '''
    def __init__(self, res, title, cad, checkbox=''):
        wx.Dialog.__init__(self, parent=None, title=title)

        if cad is not None:
            self.dx = cad.dx if cad.dx else 0
            self.dy = cad.dy if cad.dy else 0
            self.dz = cad.dz if cad.dz else 0
            self.mm_per_unit = cad.mm_per_unit

        self.value = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_PROCESS_ENTER)

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

        if checkbox:
            self.check = wx.CheckBox(self, wx.ID_ANY, checkbox)
            self.check.SetValue(True)
            vbox.Add(self.check, flag=wx.LEFT | wx.BOTTOM, border=10)
        else:
            self.check = None

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
        if self.mm_per_unit:
            try:
                scale = float(self.value.GetValue()) * self.mm_per_unit
            except ValueError:
                label = '0 x 0 x 0'
            else:
                label = '%i x %i x %i' % (max(1, self.dx*scale),
                                          max(1, self.dy*scale),
                                          max(1, self.dz*scale))
            self.dimensions.SetLabel(label)

    def done(self, event):
        # Get results from UI elements
        self.result = self.value.GetValue()

        if self.check is not None:  self.checked = self.check.IsChecked()
        else:                       self.checked = None

        # Make sure that the result is a valid float
        try:                float(self.result)
        except ValueError:  self.EndModal(wx.ID_CANCEL)
        else:               self.EndModal(wx.ID_OK)

################################################################################

class RescaleDialog(wx.Dialog):
    ''' Dialog box that allows users to rescale an image or asdf '''
    def __init__(self, title, source):
        wx.Dialog.__init__(self, parent=None, title=title)

        for a in ('dx','dy','dz'):
            setattr(self, a, getattr(source, a))

        self.value = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_PROCESS_ENTER)

        self.value.Bind(wx.EVT_CHAR, self.limit_to_numbers)
        self.value.Bind(wx.EVT_TEXT, self.update_dimensions)
        self.value.Bind(wx.EVT_TEXT_ENTER, self.done)

        self.value.ChangeValue('1')

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.value, flag=wx.ALL, border=10)
        okButton = wx.Button(self, label='OK')
        okButton.Bind(wx.EVT_BUTTON, self.done)
        hbox.Add(okButton, flag=wx.ALL, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(wx.StaticText(self, wx.ID_ANY, 'Scale factor:'),
                               flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(hbox)

        self.dimensions = wx.StaticText(self, wx.ID_ANY, '\n')
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
        try:
            scale = float(self.value.GetValue())
        except ValueError:
            label = '? x ? x ?'
        else:
            label = '%.1f x %.1f x %.1f mm\n%.1f x %.1f x %.1f"' % (
                self.dx*scale, self.dy*scale, self.dz*scale,
                self.dx*scale/25.4, self.dy*scale/25.4, self.dz*scale/25.4,
            )
        self.dimensions.SetLabel(label)

    def done(self, event):
        # Get results from UI elements
        self.result = self.value.GetValue()

        # Make sure that the result is a valid float
        try:                float(self.result)
        except ValueError:  self.EndModal(wx.ID_CANCEL)
        else:               self.EndModal(wx.ID_OK)

################################################################################

class CheckDialog(wx.Dialog):
    ''' Dialog box with a single check box. '''
    def __init__(self, title, label):
        wx.Dialog.__init__(self, parent=None, title=title)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.check = wx.CheckBox(self, wx.ID_ANY, label)
        hbox.Add(self.check, flag=wx.ALL, border=10)
        okButton = wx.Button(self, label='OK')
        okButton.Bind(wx.EVT_BUTTON, self.done)
        hbox.Add(okButton, flag=wx.ALL, border=10)

        self.SetSizerAndFit(hbox)

    def done(self, event):
        # Dummy results for self.result
        self.result = None
        self.checked = self.check.IsChecked()
        self.EndModal(wx.ID_OK)

################################################################################

class TextFrame(wx.Frame):
    '''A simple text frame to display the contents of a file
       or software-defined text.'''
    def __init__(self, title, filename=None):
        wx.Frame.__init__(self, koko.FRAME, title=title)

        # Create text pane.
        self.txt = koko.editor.Editor(self, style=wx.NO_BORDER, size=(600, 400))
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


class MessageFrame(wx.Frame):
    def __init__(self, title, message):
        wx.Frame.__init__(self, koko.FRAME, title=title)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.txt = wx.StaticText(self, wx.ID_ANY, message)
        sizer.Add(self.txt, flag=wx.ALL, border=20)
        self.SetSizerAndFit(sizer)
        DARK_THEME.apply(self)

        self.Show()

def display_message(title, message):
    return MessageFrame(title, message)

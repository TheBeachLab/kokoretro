import wx
import inspect

from koko.retro.themes import DARK_THEME

class EditPanel(wx.Panel):
    '''Magic panel, created automatically based on parameters
       of the target object's constructor.
    '''
    def __init__(self, canvas, target):
        # Save a link upstream
        self.canvas = canvas

        # Figure out constructor arguments for target object
        argspec = inspect.getargspec(target.__class__.__init__)
        args = argspec.args[1:]

        # Extract properties from this object
        props = [p for p,t in vars(target.__class__).iteritems()
                 if type(t) == property and p[0] != '_' and p not in args]
        props = sorted(props)


        # Filter out hidden arguments and properties
        hidden = target.__class__.HIDDEN_PROPERTIES
        args  = filter(lambda a: a not in hidden, args)
        props = filter(lambda p: p not in hidden, props)

        # Start creating the panel
        wx.Panel.__init__(self, canvas)

        # Create a sizer of the appropriate size
        sizer = wx.FlexGridSizer(rows=len(args)+len(props)+1, cols=2)

        # Add the text 'type'
        txt = wx.StaticText(self, label='type', size=(-1, 25),
                            style=wx.ALIGN_RIGHT|wx.ST_NO_AUTORESIZE)
        sizer.Add(txt, border=3, flag=wx.BOTTOM|wx.TOP|wx.RIGHT|wx.EXPAND)

        # Add this panel's class
        classTxt =  wx.StaticText(self, size=(-1, 25),
                                  label=target.__class__.__name__)
        classTxt.SetFont(wx.Font(14, family=wx.FONTFAMILY_DEFAULT,
                                 style=wx.ITALIC, weight=wx.BOLD))
        sizer.Add(classTxt, border=1, flag=wx.BOTTOM|wx.TOP|wx.LEFT|wx.EXPAND)


        ######################################################################

        self.inputs = {}
        self.outputs = {}
        while args:
            input = self.add_row(sizer, args[0])
            input.Bind(wx.EVT_CHAR, self.char)
            input.Bind(wx.EVT_TEXT, self.changed)
            input.Bind(wx.EVT_TEXT_ENTER, self.canvas.close_edit_panel)
            self.inputs[args[0]] = input
            args = args[1:]

        while props:
            output = self.add_row(sizer, '   '+props[0], enabled=False)
            self.outputs[props[0]] = output
            props = props[1:]

        outer = wx.BoxSizer()
        outer.Add(sizer, border=10, flag=wx.ALL)
        self.SetSizerAndFit(outer)

        self.target = target
        target.selected = True

        # When this panel is closed, invoke a callback.
        canvas.Bind(wx.EVT_WINDOW_DESTROY, canvas.edit_panel_closed, self)

        DARK_THEME.apply(self)
        print outer
        canvas.Refresh()


######################################################################

    def add_row(self, sizer, label, enabled=True):
        ''' Helper function to add a row to a sizer.

            Returns a TextCtrl with extra field 'label'.
        '''

        # Create label
        labelTxt = wx.StaticText(self, label=label,
                                 style=wx.ALIGN_RIGHT|wx.ST_NO_AUTORESIZE,
                                 size=(-1, 25))
        sizer.Add(labelTxt, border=3,
                  flag=wx.BOTTOM|wx.TOP|wx.RIGHT|wx.EXPAND)

        # Create input box
        inputBox = wx.TextCtrl(self, size=(150, 25),
                               style=wx.NO_BORDER|wx.TE_PROCESS_ENTER)
        sizer.Add(inputBox, border=3,
                  flag=wx.BOTTOM|wx.TOP|wx.LEFT|wx.EXPAND)

        # Add extra field to input box
        inputBox.label = label

        # Silly hack to avoid selecting all of the text when
        # this row gets focus.
        def focus(event):
            txt = event.GetEventObject()
            txt.SetSelection(0,0)
            try:
                txt.SetInsertionPoint(txt.lastInsertionPoint)
                del txt.lastInsertionPoint
            except AttributeError:
                return
        def lost_focus(event):
            txt = event.GetEventObject()
            txt.lastInsertionPoint = txt.GetInsertionPoint()

        if enabled:
            inputBox.Bind(wx.EVT_SET_FOCUS, focus)
            inputBox.Bind(wx.EVT_KILL_FOCUS, lost_focus)
        else:
            inputBox.Disable()

        return inputBox


######################################################################

    def char(self, event):
        if event.CmdDown() and event.GetKeyCode() == ord('Z'):
            if self.canvas.can_undo:
                self.canvas.undo()
        else:
            event.Skip()

########################################

    def changed(self, event):
        if not self.disable_callbacks:
            p = event.GetEventObject().label

            if p == 'name':
                self.canvas.shape_set.propagate_name_change(
                    self.target[p].expr, self.inputs[p].GetValue())
                self.target[p].expr = self.inputs[p].GetValue()
            else:
                self.target[p].expr = self.inputs[p].GetValue()
            self.canvas.Refresh()

########################################

    def update(self):
        '''Slide the point editor around to put it on the point;
           reload text boxes based on the referred object.'''

        pt = self.canvas.pos_to_pixel(self.target.x, self.target.y)
        pt = (pt[0]+4, pt[1]+4)
        self.Move(wx.Point(*pt))

        # Prevent recursive callbacks, since we'll be editing text-box
        # values in the following code.
        self.disable_callbacks = True

        for p in self.inputs:
            # Check to see if this text box is valid
            if self.target[p].valid:
                self.inputs[p].SetForegroundColour(DARK_THEME.foreground)
            else:
                self.inputs[p].SetForegroundColour(wx.Colour(255, 80, 60))

            # Get an updated string (which occurs when nodes are dragged)
            new = str(self.target[p].expr)
            if new == self.inputs[p].GetValue():
                continue

            # Save insertion point and selection range
            ipt = self.inputs[p].GetInsertionPoint()
            sel = self.inputs[p].GetSelection()

            # Get new values from the child node
            self.inputs[p].SetValue(new)

            # Reset insertion point and selection range
            self.inputs[p].SetInsertionPoint(ipt)
            self.inputs[p].SetSelection(*sel)

        for p in self.outputs:
            property = vars(self.target.__class__)[p]
            self.outputs[p].SetValue(str(property.fget(self.target)))

        self.disable_callbacks = False

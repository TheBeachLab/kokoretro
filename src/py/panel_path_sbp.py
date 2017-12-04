#
# panel_path_sbp.py
#    make .sbp from .path
#
# Neil Gershenfeld
# CBA MIT 3/23/13
#
# (c) Massachusetts Institute of Technology 2011
# Permission granted for experimental and personal use;
# license for commercial sale available from MIT.
#
# imports
#
import wx,os
#
# panel class
#
class path_sbp_panel(wx.Panel):
   def __init__(self,parent):
      self.parent = parent
      self.parent.path_file = ''
      #
      # make file
      #
      def make_file(event):
         if (self.parent.path_file == ''):
            print 'panel_path_sbp: oops -- need path file'
            return
         self.parent.sbp_file = self.parent.tmp+self.parent.rootname+'.sbp'
         if (self.conv.GetValue()):
            direction = '0'
         else:
            direction = '1'
         if (self.inches.GetValue()):
            units = '25.4'
         else:
            units = '1'
         self.parent.sbp_file = self.parent.tmp+self.parent.rootname+'.sbp'
         spindle = self.spindle.GetValue()
         speed = self.speed.GetValue()
         jog = self.jog.GetValue()
         height = self.height.GetValue()
         command = 'path_sbp '+'\"'+self.parent.path_file+'\"'+' '+'\"'+self.parent.sbp_file+'\"'+' '+direction+' '+spindle+' '+speed+' '+speed+' '+jog+' '+jog+' '+height+' '+units
         print command
         os.system(command)
         self.button.SetMaxSize((self.parent.xsize,self.parent.ysize))
         self.button.SetMinSize((self.parent.xsize,self.parent.ysize))
         self.button.Show()
         self.parent.Layout()
         self.parent.Fit()
      #
      # send
      #
      def fab_send(event):
         command = 'fab_send '+'\"'+self.parent.sbp_file+'\"'
         print command
         os.system(command)
      #
      # panel
      #
      wx.Panel.__init__(self,parent)
      self.sizer = wx.GridBagSizer(10,10)
      self.SetSizer(self.sizer)
      #
      # label
      #
      label = wx.StaticText(self,label='to: sbp')
      bold_font = wx.Font(10,wx.DEFAULT,wx.NORMAL,wx.BOLD)
      label.SetFont(bold_font)
      self.sizer.Add(label,(0,0),span=(1,2),flag=wx.ALIGN_CENTER_HORIZONTAL)
      #
      # send
      #
      self.button = wx.Button(self,label='send it!')
      self.button.Bind(wx.EVT_BUTTON,fab_send)
      self.button.SetFont(bold_font)
      self.sizer.Add(self.button,(1,0),span=(1,2),flag=(wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL))
      self.button.Hide()
      #
      # controls
      #
      make = wx.Button(self,label='make .sbp')
      make.Bind(wx.EVT_BUTTON,make_file)
      self.sizer.Add(make,(2,0),span=(1,2),flag=wx.ALIGN_CENTER_HORIZONTAL)
      #
      units_panel = wx.Panel(self)
      units_sizer = wx.GridBagSizer(10,10)
      units_panel.SetSizer(units_sizer)
      units_sizer.Add(wx.StaticText(units_panel,label='file units:'),(0,0),flag=(wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT))
      self.inches = wx.RadioButton(units_panel,label='inches',style=wx.RB_GROUP)
      units_sizer.Add(self.inches,(0,1))
      self.mm = wx.RadioButton(units_panel,label='mm')
      units_sizer.Add(self.mm,(0,2))
      self.sizer.Add(units_panel,(3,0),span=(1,2),flag=wx.ALIGN_CENTER_HORIZONTAL)
      #
      dir_panel = wx.Panel(self)
      dir_sizer = wx.GridBagSizer(10,10)
      dir_panel.SetSizer(dir_sizer)
      self.conv = wx.RadioButton(dir_panel,label='conventional',style=wx.RB_GROUP)
      dir_sizer.Add(self.conv,(0,0))
      self.climb = wx.RadioButton(dir_panel,label='climb')
      dir_sizer.Add(self.climb,(0,1))
      self.sizer.Add(dir_panel,(4,0),span=(1,2),flag=wx.ALIGN_CENTER_HORIZONTAL)
      #
      row4_panel = wx.Panel(self)
      row4_sizer = wx.GridBagSizer(10,10)
      row4_panel.SetSizer(row4_sizer)
      row4_sizer.Add(wx.StaticText(row4_panel,label='cut speed (mm/s)'),(0,0),flag=(wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT))
      row4_sizer.Add(wx.StaticText(row4_panel,label='jog speed (mm/s)'),(0,1),flag=(wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT))
      self.sizer.Add(row4_panel,(5,0),span=(1,2),flag=(wx.ALIGN_CENTER_HORIZONTAL))
      #
      row5_panel = wx.Panel(self)
      row5_sizer = wx.GridBagSizer(10,10)
      row5_panel.SetSizer(row5_sizer)
      self.speed = wx.TextCtrl(row5_panel,-1,'15')
      row5_sizer.Add(self.speed,(0,0))
      self.jog = wx.TextCtrl(row5_panel,-1,'75')
      row5_sizer.Add(self.jog,(0,1))
      self.sizer.Add(row5_panel,(6,0),span=(1,2),flag=(wx.ALIGN_CENTER_HORIZONTAL))
      #
      row6_panel = wx.Panel(self)
      row6_sizer = wx.GridBagSizer(10,10)
      row6_panel.SetSizer(row6_sizer)
      row6_sizer.Add(wx.StaticText(row6_panel,label='spindle speed (RPM)'),(0,0),flag=(wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT))
      row6_sizer.Add(wx.StaticText(row6_panel,label='jog height (mm)     '),(0,1),flag=(wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT))
      self.sizer.Add(row6_panel,(7,0),span=(1,2),flag=(wx.ALIGN_CENTER_HORIZONTAL))
      #
      row7_panel = wx.Panel(self)
      row7_sizer = wx.GridBagSizer(10,10)
      row7_panel.SetSizer(row7_sizer)
      self.spindle = wx.TextCtrl(row7_panel,-1,'10000')
      row7_sizer.Add(self.spindle,(0,0))
      self.height = wx.TextCtrl(row7_panel,-1,'5')
      row7_sizer.Add(self.height,(0,1))
      self.sizer.Add(row7_panel,(8,0),span=(1,2),flag=(wx.ALIGN_CENTER_HORIZONTAL))
      #
      # fit
      #
      self.Fit()

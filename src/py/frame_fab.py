#
# frame_fab.py
#    fab module frame
#
# Neil Gershenfeld
# CBA MIT 8/10/11
#
# (c) Massachusetts Institute of Technology 2011
# Permission granted for experimental and personal use;
# license for commercial sale available from MIT.
#
# imports
#
import wx,sys,os
#
# frame class
#
class fab_frame(wx.Frame):
   #
   # init
   #
   def __init__(self,title,argv):
      self.size = 400 # default panel size
      self.tmp = "fab_mod_" # default temporary file prefix
      #
      # frame
      #
      wx.Frame.__init__(self,None,title=title)
      self.sizer = wx.GridBagSizer(10,10)
      self.SetSizer(self.sizer)
      #
      # arguments
      #
      self.rootname = ""
      self.filename = ""
      self.basename = ""
      if (len(argv) > 1):
         if (argv[1] != '""'):
            self.filename = sys.argv[1]
            self.basename = os.path.basename(self.filename)
      if (len(argv) > 2):
         self.size = int(sys.argv[2])
   #
   # defaults handler
   #
   def defaults_handler(self,event):
      value = self.control_panel.defaults.GetValue()
      string = self.defaults[value]
      exec(string)

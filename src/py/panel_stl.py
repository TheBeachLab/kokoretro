#
# panel_stl.py
#    read .stl
#
# Neil Gershenfeld
# CBA MIT 3/6/11
#
# (c) Massachusetts Institute of Technology 2011
# Permission granted for experimental and personal use;
# license for commercial sale available from MIT.
#
# imports
#
import wx,string,os,sys
#
# panel class
#
class stl_panel(wx.Panel):
   def __init__(self,parent):
      self.parent = parent
      self.parent.stl_file = ''
      #
      # get stl info
      #
      def stl_info(name):
         temp_name = self.parent.tmp+'stl_info'
         command = 'stl_info '+'\"'+name+'\"'+' > '+'\"'+temp_name+'\"'
         os.system(command)
         output_file = open(temp_name,'r')
         output = output_file.read()
         print output
         if (string.find(output,'must be binary') != -1):
            sys.exit(-1)
         command = 'rm '+'\"'+temp_name+'\"'
         os.system(command)
         start = 6+string.find(output,'xmax:')
         space = string.find(output,' ',start)
         end = string.find(output,'ymin',space)-4
         self.parent.xmin = float(output[start:space])
         self.parent.xmax = float(output[1+space:end])
         start = 6+string.find(output,'ymax:')
         space = string.find(output,' ',start)
         end = string.find(output,'zmin',space)-4
         self.parent.ymin = float(output[start:space])
         self.parent.ymax = float(output[1+space:end])
         start = 6+string.find(output,'zmax:')
         space = string.find(output,' ',start)
         self.parent.zmin = float(output[start:space])
         self.parent.zmax = float(output[space+1:-1])
         return output
      #
      # load file
      #
      def load_file(event):
         if (self.parent.basename == ""):
            return
         pos = string.find(self.parent.basename,".stl")
         if (pos == -1):
            pos = string.find(self.parent.basename,".STL")
            if (pos == -1):
               print 'stl_panel: oops -- must be .stl'
               sys.exit()
         self.parent.rootname = self.parent.basename[:pos]
         self.parent.stl_file = self.parent.filename
         info = stl_info(self.parent.filename)
         self.info.SetLabel(info)
         self.parent.Layout()
         self.parent.Fit()
      #
      # select file
      #
      def select_file(event):
         dialog = wx.FileDialog(self, "Choose a file", os.getcwd(), "", "*.stl", wx.OPEN)
         if (dialog.ShowModal() == wx.ID_OK):
            self.parent.filename = dialog.GetPath()
            self.parent.basename = os.path.basename(self.parent.filename)
            pos = string.find(self.parent.basename,".stl")
            if (pos == -1):
               print 'stl_panel: oops -- must be .stl'
               sys.exit()
            else:
               self.parent.rootname = self.parent.basename[:pos]
            self.parent.stl_file = self.parent.filename
            info = stl_info(self.parent.filename)
            self.info.SetLabel(info)
            self.parent.Layout()
            self.parent.Fit()
      #
      # panel
      #
      wx.Panel.__init__(self,parent)
      self.sizer = wx.GridBagSizer(10,10)
      self.SetSizer(self.sizer)
      #
      # label 
      #
      label = wx.StaticText(self,label='from: stl')
      bold_font = wx.Font(10,wx.DEFAULT,wx.NORMAL,wx.BOLD)
      label.SetFont(bold_font)
      self.sizer.Add(label,(0,0),flag=wx.ALIGN_CENTER_HORIZONTAL)
      #
      # controls
      #
      load = wx.Button(self,label='load .stl')
      load.Bind(wx.EVT_BUTTON,select_file)
      self.sizer.Add(load,(1,0),flag=wx.ALIGN_CENTER_HORIZONTAL)
      #
      self.info = wx.StaticText(self,label="")
      self.sizer.Add(self.info,(2,0),flag=wx.ALIGN_CENTER_HORIZONTAL)
      #
      # file
      #
      load_file(0)
      #
      # fit
      #
      self.Fit()

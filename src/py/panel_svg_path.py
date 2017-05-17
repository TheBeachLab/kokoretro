#
# panel_svg_path.py
#    make .path from .svg
#
# Neil Gershenfeld
# CBA MIT 7/13/11
#
# (c) Massachusetts Institute of Technology 2011
# Permission granted for experimental and personal use;
# license for commercial sale available from MIT.
#
# imports
#
import wx,os,string
#
# panel class
#
class svg_path_panel(wx.Panel):
   def __init__(self,parent):
      self.parent = parent
      self.parent.zmin = 0
      self.parent.zmax = 0
      self.parent.units = 1
      #
      # make path
      #
      def make_path(event):
         if (self.parent.rootname == ''):
            return
         tmp_svg_file = self.parent.tmp+self.parent.rootname+'.svg'
         svg_file = open(tmp_svg_file,'w')
         svg_file.write(self.parent.svg_panel.text.GetValue())
         svg_file.close()
         self.parent.path_file = self.parent.tmp+self.parent.rootname+'.path'
         path_png = self.parent.tmp+self.parent.rootname+'.path.png'
         points = self.points.GetValue()
         resolution = self.resolution.GetValue()
         z = self.z.GetValue()
         output_name = self.parent.tmp+'path_out'
         command = 'svg_path '+'\"'+tmp_svg_file+'\"'+' '+'\"'+self.parent.path_file+'\"'+' '+points+' '+resolution+' '+z+' > '+'\"'+output_name+'\"'
         print command
         os.system(command)
         command = 'path_png '+'\"'+self.parent.path_file+'\"'+' '+'\"'+path_png+'\"'
         print command
         os.system(command)
         command = 'png_scale '+'\"'+path_png+'\"'+' '+'\"'+path_png+'\"'+' 1 0'
         print command
         os.system(command)
         output_file = open(output_name,'r')
         output = output_file.read()
         output_file.close()
         self.info.SetLabel(output)
         path_image = wx.Image(path_png)
         path_image = wx.Image.Blur(path_image,1)
         (nx,ny) = path_image.GetSize()
         ratio = float(ny)/float(nx)
         if (ratio > 1):
            self.parent.ysize = self.parent.size
            self.parent.xsize = self.parent.size/ratio
         else:
            self.parent.ysize = self.parent.size*ratio
            self.parent.xsize = self.parent.size
         wx.Image.Rescale(path_image,self.parent.xsize,self.parent.ysize,quality=wx.IMAGE_QUALITY_HIGH)
         path_bitmap = path_image.ConvertToBitmap()
         self.bitmap.SetBitmap(path_bitmap)
         self.bitmap.Show()
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
      label = wx.StaticText(self,label='to: path')
      bold_font = wx.Font(10,wx.DEFAULT,wx.NORMAL,wx.BOLD)
      label.SetFont(bold_font)
      self.sizer.Add(label,(0,0),flag=wx.ALIGN_CENTER_HORIZONTAL)
      #
      # image
      #
      image = wx.ArtProvider.GetBitmap(wx.ART_QUESTION, wx.ART_OTHER, (self.parent.size,self.parent.size))
      self.bitmap = wx.StaticBitmap(self,-1,image)
      self.sizer.Add(self.bitmap,(1,0),flag=(wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL))
      self.bitmap.Hide()
      #
      # controls
      #
      make = wx.Button(self,label='make .path')
      make.Bind(wx.EVT_BUTTON,make_path)
      self.sizer.Add(make,(2,0),flag=wx.ALIGN_CENTER_HORIZONTAL)
      #
      points_panel = wx.Panel(self)
      points_sizer = wx.GridBagSizer(10,10)
      points_panel.SetSizer(points_sizer)
      points_sizer.Add(wx.StaticText(points_panel,label='curve points:'),(0,0),flag=(wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT))
      self.points = wx.TextCtrl(points_panel,-1,'25')
      points_sizer.Add(self.points,(0,1))
      self.sizer.Add(points_panel,(3,0),flag=wx.ALIGN_CENTER_HORIZONTAL)
      #
      resolution_panel = wx.Panel(self)
      resolution_sizer = wx.GridBagSizer(10,10)
      resolution_panel.SetSizer(resolution_sizer)
      resolution_sizer.Add(wx.StaticText(resolution_panel,label='path resolution:'),(0,0),flag=(wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT))
      self.resolution = wx.TextCtrl(resolution_panel,-1,'1000')
      resolution_sizer.Add(self.resolution,(0,1))
      self.sizer.Add(resolution_panel,(4,0),flag=wx.ALIGN_CENTER_HORIZONTAL)
      #
      z_panel = wx.Panel(self)
      z_sizer = wx.GridBagSizer(10,10)
      z_panel.SetSizer(z_sizer)
      z_sizer.Add(wx.StaticText(z_panel,label='z (mm):'),(0,0),flag=(wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT))
      self.z = wx.TextCtrl(z_panel,-1,'0')
      z_sizer.Add(self.z,(0,1))
      self.sizer.Add(z_panel,(5,0),flag=wx.ALIGN_CENTER_HORIZONTAL)
      #
      self.info = wx.StaticText(self,label="")
      self.sizer.Add(self.info,(6,0),flag=wx.ALIGN_CENTER_HORIZONTAL)
      #
      # fit
      #
      self.Fit()

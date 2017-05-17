#
# panel_png_path.py
#    make .path from .png
#
# Neil Gershenfeld
# CBA MIT 3/23/13
#
# (c) Massachusetts Institute of Technology 2012
# Permission granted for experimental and personal use;
# license for commercial sale available from MIT.
#
# imports
#
import wx,os
#
# panel class
#
class png_path_panel(wx.Panel):
   def __init__(self,parent):
      self.parent = parent
      self.parent.png_file = ''
      self.parent.zmin = ''
      self.parent.zmax = ''
      self.parent.units = 1
      #
      # view path
      #
      def view_path(event):
         if (self.parent.path_file == ''):
            print "png_path: oops -- must make .path first"
            return
         self.parent.ps_file = self.parent.tmp+self.parent.rootname+'.ps'
         command = 'path_ps '+'\"'+self.parent.path_file+'\"'+' '+'\"'+self.parent.ps_file+'\"'+" 3"
         print command
         os.system(command)
         command = 'fab_send '+'\"'+self.parent.ps_file+'\"'
         print command
         os.system(command)
      #
      # make path
      #
      def make_path(event):
         if (self.parent.png_file == ''):
            print "png_path: oops -- must make .png first"
            return
         self.parent.path_file = self.parent.tmp+self.parent.rootname+'.path'
         path_png = self.parent.tmp+self.parent.rootname+'.path.png'
         error = self.error.GetValue()
         diameter = self.diameter.GetValue()
         number = self.number.GetValue()
         overlap = self.overlap.GetValue()
         threshold = self.threshold.GetValue()
         zstep = self.frame3_zstep.GetValue()
         if (self.frame3_xy.GetValue() | self.frame3_xz.GetValue() | self.frame3_yz.GetValue()):
            #
            # 3D path
            #
            if ((parent.zmin != '') & (self.frame3_zbot.GetValue() == '')):
               #self.frame3_zbot.SetValue(str(parent.units*parent.zmin))
               self.frame3_zbot.SetValue(str(parent.units*(parent.zmin-parent.zmax)))
               self.frame3_ibot.SetValue('0')
            if ((parent.zmax != '') & (self.frame3_ztop.GetValue() == '')):
               #self.frame3_ztop.SetValue(str(parent.units*parent.zmax))
               self.frame3_ztop.SetValue('0')
               self.frame3_itop.SetValue('1')
            itop = self.frame3_itop.GetValue()
            ibot = self.frame3_ibot.GetValue()
            ztop = self.frame3_ztop.GetValue()
            zbot = self.frame3_zbot.GetValue()
            if self.frame3_xz.GetValue():
               xz = "1"
            else:
               xz = "0"
            if self.frame3_yz.GetValue():
               yz = "1"
            else:
               yz = "0"
            if self.frame3_xy.GetValue():
               xy = "1"
            else:
               xy = "0"
            self.parent.zmax = float(ztop)
            self.parent.zmin = float(zbot)
            self.parent.units = 1
            #if self.frame3_flat.GetValue():
            #   tool_type = "f"
            #if self.frame3_ball.GetValue():
            #   tool_type = "b"
            #cut_depth = '0'
            #command = 'png_path '+'\"'+self.parent.png_file+'\"'+' '+'\"'+self.parent.path_file+'\"'+' '+error+' '+diameter+' '+number+' '+overlap+' '+itop+' '+ibot+' '+ztop+' '+zbot+' '+zstep+' '+xz+' '+yz+' '+xy+' '+tool_type+' '+cut_depth
            command = 'png_path '+'\"'+self.parent.png_file+'\"'+' '+'\"'+self.parent.path_file+'\"'+' '+error+' '+diameter+' '+number+' '+overlap+' '+itop+' '+ibot+' '+ztop+' '+zbot+' '+zstep+' '+xz+' '+yz+' '+xy
         else:
            #
            # 2D path
            #
            z = self.z.GetValue()
            self.parent.zmax = float(z)
            self.parent.zmin = float(z)
            self.parent.units = 1
            command = 'png_path '+'\"'+self.parent.png_file+'\"'+' '+'\"'+self.parent.path_file+'\"'+' '+error+' '+diameter+' '+number+' '+overlap+' '+threshold+' '+threshold+' '+z
         print command
         ret = os.system(command)
         if (ret == 0):
            command = 'path_png '+'\"'+self.parent.path_file+'\"'+' '+'\"'+path_png+'\"'
            print command
            os.system(command)
            command = 'png_scale '+'\"'+path_png+'\"'+' '+'\"'+path_png+'\"'+' 1 0'
            print command
            os.system(command)
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
         else:
            self.bitmap.Hide()
            self.parent.Layout()
            self.parent.Fit()
      #
      # 3D path dialog
      #
      def quit3(event):
         self.frame3.Hide()
      #
      def path3(event):
         if ((parent.zmin != '') & (self.frame3_zbot.GetValue() == '')):
            #self.frame3_zbot.SetValue(str(parent.units*parent.zmin))
            self.frame3_zbot.SetValue(str(parent.units*(parent.zmin-parent.zmax)))
            self.frame3_ibot.SetValue('0')
         if ((parent.zmax != '') & (self.frame3_ztop.GetValue() == '')):
            #self.frame3_ztop.SetValue(str(parent.units*parent.zmax))
            self.frame3_ztop.SetValue('0')
            self.frame3_itop.SetValue('1')
         self.frame3.Show()
      #
      self.frame3 = wx.Frame(None, -1, '3D settings')
      self.frame3_sizer = wx.GridBagSizer(10,10)
      self.frame3.SetSizer(self.frame3_sizer)
      #
      self.frame3_sizer.Add(wx.StaticText(self.frame3,label='top intensity (0-1):'),(0,0),flag=(wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT))
      self.frame3_itop = wx.TextCtrl(self.frame3,-1,'0.5')
      self.frame3_sizer.Add(self.frame3_itop,(0,1))
      #
      self.frame3_sizer.Add(wx.StaticText(self.frame3,label='top height (mm):'),(0,2),flag=(wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT))
      self.frame3_ztop = wx.TextCtrl(self.frame3,-1,'')
      self.frame3_sizer.Add(self.frame3_ztop,(0,3))
      #
      self.frame3_sizer.Add(wx.StaticText(self.frame3,label='bottom intensity (0-1):'),(1,0),flag=(wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT))
      self.frame3_ibot = wx.TextCtrl(self.frame3,-1,'0.5')
      self.frame3_sizer.Add(self.frame3_ibot,(1,1))
      #
      self.frame3_sizer.Add(wx.StaticText(self.frame3,label='bottom height (mm):'),(1,2),flag=(wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT))
      self.frame3_zbot = wx.TextCtrl(self.frame3,-1,'')
      self.frame3_sizer.Add(self.frame3_zbot,(1,3))
      #
      self.frame3_xy = wx.CheckBox(self.frame3,-1,'xy rough',(10,10))
      self.frame3_sizer.Add(self.frame3_xy,(2,0),span=(1,2),flag=wx.ALIGN_CENTER_HORIZONTAL)
      #
      self.frame3_sizer.Add(wx.StaticText(self.frame3,label='cut depth (mm):'),(2,2),flag=(wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT))
      self.frame3_zstep = wx.TextCtrl(self.frame3,-1,'1')
      self.frame3_sizer.Add(self.frame3_zstep,(2,3))
      #
      self.finish_panel = wx.Panel(self.frame3)
      self.finish_sizer = wx.GridBagSizer(10,10)
      self.finish_panel.SetSizer(self.finish_sizer)
      self.frame3_xz = wx.CheckBox(self.finish_panel,-1,'xz finish',(10,10))
      self.finish_sizer.Add(self.frame3_xz,(0,0),flag=wx.ALIGN_CENTER_HORIZONTAL)
      self.frame3_yz = wx.CheckBox(self.finish_panel,-1,'yz finish',(10,10))
      self.finish_sizer.Add(self.frame3_yz,(0,1),span=(1,2),flag=wx.ALIGN_CENTER_HORIZONTAL)
      self.frame3_sizer.Add(self.finish_panel,(3,0),span=(1,2),flag=(wx.ALIGN_CENTER_HORIZONTAL))
      #
      self.type_panel = wx.Panel(self.frame3)
      self.type_sizer = wx.GridBagSizer(10,10)
      self.type_panel.SetSizer(self.type_sizer)
      self.frame3_flat = wx.RadioButton(self.type_panel,label='flat end',style=wx.RB_GROUP)
      self.type_sizer.Add(self.frame3_flat,(0,0))
      #self.frame3_ball = wx.RadioButton(self.type_panel,label='ball end')
      #self.type_sizer.Add(self.frame3_ball,(0,1))
      self.frame3_sizer.Add(self.type_panel,(4,0),span=(1,2),flag=wx.ALIGN_CENTER_HORIZONTAL)
      #
      self.frame3_quit = wx.Button(self.frame3,label='close')
      self.frame3_quit.Bind(wx.EVT_BUTTON,quit3)
      self.frame3_sizer.Add(self.frame3_quit,(4,2),span=(1,2),flag=wx.ALIGN_CENTER_HORIZONTAL)
      #
      self.frame3.Layout()
      self.frame3.Fit()
      self.frame3.Hide()
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
      self.sizer.Add(label,(0,0),span=(1,2),flag=wx.ALIGN_CENTER_HORIZONTAL)
      #
      # image
      #
      image = wx.ArtProvider.GetBitmap(wx.ART_QUESTION, wx.ART_OTHER, (self.parent.size,self.parent.size))
      self.bitmap = wx.StaticBitmap(self,-1,image)
      self.sizer.Add(self.bitmap,(1,0),span=(1,2),flag=(wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL))
      self.bitmap.Hide()
      #
      # controls
      #
      row2_panel = wx.Panel(self)
      row2_sizer = wx.GridBagSizer(10,10)
      row2_panel.SetSizer(row2_sizer)
      make = wx.Button(row2_panel,label='make .path')
      make.Bind(wx.EVT_BUTTON,make_path)
      row2_sizer.Add(make,(0,0),flag=wx.ALIGN_CENTER_HORIZONTAL)
      view = wx.Button(row2_panel,label='view .path')
      view.Bind(wx.EVT_BUTTON,view_path)
      row2_sizer.Add(view,(0,1),flag=wx.ALIGN_CENTER_HORIZONTAL)
      self.sizer.Add(row2_panel,(2,0),span=(1,2),flag=(wx.ALIGN_CENTER_HORIZONTAL))
      #
      row3_panel = wx.Panel(self)
      row3_sizer = wx.GridBagSizer(10,10)
      row3_panel.SetSizer(row3_sizer)
      row3_sizer.Add(wx.StaticText(row3_panel,label='  diameter (mm)'),(0,0),flag=(wx.ALIGN_RIGHT))
      row3_sizer.Add(wx.StaticText(row3_panel,label='offsets (-1 to fill)'),(0,1),flag=(wx.ALIGN_LEFT))
      self.sizer.Add(row3_panel,(3,0),span=(1,2),flag=(wx.ALIGN_CENTER_HORIZONTAL))
      #
      row4_panel = wx.Panel(self)
      row4_sizer = wx.GridBagSizer(10,10)
      row4_panel.SetSizer(row4_sizer)
      self.diameter = wx.TextCtrl(row4_panel,-1,'0.25')
      row4_sizer.Add(self.diameter,(0,0),flag=(wx.ALIGN_RIGHT))
      self.number = wx.TextCtrl(row4_panel,-1,'1')
      row4_sizer.Add(self.number,(0,1),flag=(wx.ALIGN_LEFT))
      self.sizer.Add(row4_panel,(4,0),span=(1,2),flag=(wx.ALIGN_CENTER_HORIZONTAL))
      #
      row5_panel = wx.Panel(self)
      row5_sizer = wx.GridBagSizer(10,10)
      row5_panel.SetSizer(row5_sizer)
      row5_sizer.Add(wx.StaticText(row5_panel,label='         overlap (0-1)'),(0,0),flag=(wx.ALIGN_RIGHT))
      row5_sizer.Add(wx.StaticText(row5_panel,label='2D threshold (0-1)'),(0,1),flag=(wx.ALIGN_LEFT))
      self.sizer.Add(row5_panel,(5,0),span=(1,2),flag=(wx.ALIGN_CENTER_HORIZONTAL))
      #
      row6_panel = wx.Panel(self)
      row6_sizer = wx.GridBagSizer(10,10)
      row6_panel.SetSizer(row6_sizer)
      self.overlap = wx.TextCtrl(row6_panel,-1,'0.5')
      row6_sizer.Add(self.overlap,(0,0),flag=(wx.ALIGN_RIGHT))
      self.threshold = wx.TextCtrl(row6_panel,-1,'0.5')
      row6_sizer.Add(self.threshold,(0,1),flag=(wx.ALIGN_LEFT))
      self.sizer.Add(row6_panel,(6,0),span=(1,2),flag=(wx.ALIGN_CENTER_HORIZONTAL))
      #
      row7_panel = wx.Panel(self)
      row7_sizer = wx.GridBagSizer(10,10)
      row7_panel.SetSizer(row7_sizer)
      row7_sizer.Add(wx.StaticText(row7_panel,label='     error (pixels)'),(0,0),flag=(wx.ALIGN_RIGHT))
      row7_sizer.Add(wx.StaticText(row7_panel,label=' 2D z (mm)        '),(0,1),flag=(wx.ALIGN_LEFT))
      self.sizer.Add(row7_panel,(7,0),span=(1,2),flag=(wx.ALIGN_CENTER_HORIZONTAL))
      #
      row8_panel = wx.Panel(self)
      row8_sizer = wx.GridBagSizer(10,10)
      row8_panel.SetSizer(row8_sizer)
      self.error = wx.TextCtrl(row8_panel,-1,'1.1')
      row8_sizer.Add(self.error,(0,0),flag=(wx.ALIGN_RIGHT))
      self.z = wx.TextCtrl(row8_panel,-1,'0')
      row8_sizer.Add(self.z,(0,1),flag=(wx.ALIGN_LEFT))
      self.sizer.Add(row8_panel,(8,0),span=(1,2),flag=(wx.ALIGN_CENTER_HORIZONTAL))
      #
      set3 = wx.Button(self,label='3D settings')
      set3.Bind(wx.EVT_BUTTON,path3)
      self.sizer.Add(set3,(9,0),span=(1,2),flag=wx.ALIGN_CENTER_HORIZONTAL)
      #
      # fit
      #
      self.Fit()

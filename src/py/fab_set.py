#
# fab_set.py
#    fab modules frame and set workflow defaults
#
# Neil Gershenfeld
# CBA MIT 9/18/11
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
   # set .png .epi defaults
   #
   def set_png_epi(self):
      self.defaults = {}
      self.control_panel.defaults.Append('cardboard')
      self.defaults["cardboard"]\
      = "self.path_panel.diameter.SetValue('0.25');\
         self.path_panel.error.SetValue('1.5');\
         self.epi_panel.power.SetValue('25');\
         self.epi_panel.speed.SetValue('75');"
      self.control_panel.defaults.Append('acrylic')
      self.defaults["acrylic"]\
      = "self.path_panel.diameter.SetValue('0.25');\
         self.path_panel.error.SetValue('1.5');\
         self.epi_panel.power.SetValue('75');\
         self.epi_panel.speed.SetValue('25');"
   #
   # set .png .epi halftone defaults
   #
   def set_png_epi_halftone(self):
      self.defaults = {}
      self.control_panel.defaults.Append('cardboard')
      self.defaults["cardboard"]\
      = "self.epi_panel.power.SetValue('25');\
         self.epi_panel.speed.SetValue('75');"
      self.control_panel.defaults.Append('acrylic')
      self.defaults["acrylic"]\
      = "self.epi_panel.power.SetValue('75');\
         self.epi_panel.speed.SetValue('25');"
   #
   # set .cad .epi defaults
   #
   def set_cad_epi(self):
      self.defaults = {}
      self.control_panel.defaults.Append('cardboard')
      self.defaults["cardboard"]\
      = "self.png_panel.resolution.SetValue('10');\
         self.path_panel.diameter.SetValue('0.25');\
         self.path_panel.error.SetValue('1.5');\
         self.epi_panel.power.SetValue('25');\
         self.epi_panel.speed.SetValue('75');"
      self.control_panel.defaults.Append('acrylic')
      self.defaults["acrylic"]\
      = "self.png_panel.resolution.SetValue('10');\
         self.path_panel.diameter.SetValue('0.25');\
         self.path_panel.error.SetValue('1.5');\
         self.epi_panel.power.SetValue('75');\
         self.epi_panel.speed.SetValue('25');"
   #
   # set .math .epi defaults
   #
   def set_math_epi(self):
      self.defaults = {}
      self.control_panel.defaults.Append('cardboard')
      self.defaults["cardboard"]\
      = "self.png_panel.resolution.SetValue('10');\
         self.path_panel.diameter.SetValue('0.25');\
         self.path_panel.error.SetValue('1.5');\
         self.epi_panel.power.SetValue('25');\
         self.epi_panel.speed.SetValue('75');"
      self.control_panel.defaults.Append('acrylic')
      self.defaults["acrylic"]\
      = "self.png_panel.resolution.SetValue('10');\
         self.path_panel.diameter.SetValue('0.25');\
         self.path_panel.error.SetValue('1.5');\
         self.epi_panel.power.SetValue('75');\
         self.epi_panel.speed.SetValue('25');"
   #
   # set .svg .epi defaults
   #
   def set_svg_epi(self):
      self.defaults = {}
      self.control_panel.defaults.Append('cardboard')
      self.defaults["cardboard"]\
      = "self.epi_panel.power.SetValue('25');\
         self.epi_panel.speed.SetValue('75');"
      self.control_panel.defaults.Append('acrylic')
      self.defaults["acrylic"]\
      = "self.epi_panel.power.SetValue('75');\
         self.epi_panel.speed.SetValue('25');"
   #
   # set .png .uni defaults
   #
   def set_png_uni(self):
      self.defaults = {}
      self.control_panel.defaults.Append('cardboard')
      self.defaults["cardboard"]\
      = "self.path_panel.diameter.SetValue('0.25');\
         self.path_panel.error.SetValue('1.5');\
         self.uni_panel.power.SetValue('25');\
         self.uni_panel.speed.SetValue('75');"
      self.control_panel.defaults.Append('acrylic')
      self.defaults["acrylic"]\
      = "self.path_panel.diameter.SetValue('0.25');\
         self.path_panel.error.SetValue('1.5');\
         self.uni_panel.power.SetValue('75');\
         self.uni_panel.speed.SetValue('25');"
   #
   # set .png .uni halftone defaults
   #
   def set_png_uni_halftone(self):
      self.defaults = {}
      self.control_panel.defaults.Append('cardboard')
      self.defaults["cardboard"]\
      = "self.uni_panel.power.SetValue('25');\
         self.uni_panel.speed.SetValue('75');"
      self.control_panel.defaults.Append('acrylic')
      self.defaults["acrylic"]\
      = "self.uni_panel.power.SetValue('75');\
         self.uni_panel.speed.SetValue('25');"
   #
   # set .cad .uni defaults
   #
   def set_cad_uni(self):
      self.defaults = {}
      self.control_panel.defaults.Append('cardboard')
      self.defaults["cardboard"]\
      = "self.png_panel.resolution.SetValue('10');\
         self.path_panel.diameter.SetValue('0.25');\
         self.path_panel.error.SetValue('1.5');\
         self.uni_panel.power.SetValue('25');\
         self.uni_panel.speed.SetValue('75');"
      self.control_panel.defaults.Append('acrylic')
      self.defaults["acrylic"]\
      = "self.png_panel.resolution.SetValue('10');\
         self.path_panel.diameter.SetValue('0.25');\
         self.path_panel.error.SetValue('1.5');\
         self.uni_panel.power.SetValue('75');\
         self.uni_panel.speed.SetValue('25');"
   #
   # set .math .uni defaults
   #
   def set_math_uni(self):
      self.defaults = {}
      self.control_panel.defaults.Append('cardboard')
      self.defaults["cardboard"]\
      = "self.png_panel.resolution.SetValue('10');\
         self.path_panel.diameter.SetValue('0.25');\
         self.path_panel.error.SetValue('1.5');\
         self.uni_panel.power.SetValue('25');\
         self.uni_panel.speed.SetValue('75');"
      self.control_panel.defaults.Append('acrylic')
      self.defaults["acrylic"]\
      = "self.png_panel.resolution.SetValue('10');\
         self.path_panel.diameter.SetValue('0.25');\
         self.path_panel.error.SetValue('1.5');\
         self.uni_panel.power.SetValue('75');\
         self.uni_panel.speed.SetValue('25');"
   #
   # set .svg .uni defaults
   #
   def set_svg_uni(self):
      self.defaults = {}
      self.control_panel.defaults.Append('cardboard')
      self.defaults["cardboard"]\
      = "self.uni_panel.power.SetValue('25');\
         self.uni_panel.speed.SetValue('75');"
      self.control_panel.defaults.Append('acrylic')
      self.defaults["acrylic"]\
      = "self.uni_panel.power.SetValue('75');\
         self.uni_panel.speed.SetValue('25');"
   #
   # set .png .rml defaults
   #
   def set_png_rml(self):
      self.defaults = {}
      self.control_panel.defaults.Append('mill traces (1/64)')
      self.defaults["mill traces (1/64)"]\
      = "self.path_panel.diameter.SetValue('0.4');\
         self.path_panel.number.SetValue('4');\
         self.path_panel.z.SetValue('-0.1');\
         self.path_panel.frame3_ztop.SetValue('');\
         self.path_panel.frame3_zbot.SetValue('');\
         self.path_panel.frame3_zstep.SetValue('');\
         self.path_panel.frame3_xy.SetValue(False);\
         self.path_panel.frame3_xz.SetValue(False);\
         self.path_panel.frame3_yz.SetValue(False);\
         self.rml_panel.speed.SetValue('4');\
         self.rml_panel.zjog.SetValue('1.0');"
      self.control_panel.defaults.Append('mill traces (0.010)')
      self.defaults["mill traces (0.010)"]\
      = "self.path_panel.diameter.SetValue('0.254');\
         self.path_panel.number.SetValue('1');\
         self.path_panel.z.SetValue('-0.1');\
         self.path_panel.frame3_ztop.SetValue('');\
         self.path_panel.frame3_zbot.SetValue('');\
         self.path_panel.frame3_zstep.SetValue('');\
         self.path_panel.frame3_xy.SetValue(False);\
         self.path_panel.frame3_xz.SetValue(False);\
         self.path_panel.frame3_yz.SetValue(False);\
         self.rml_panel.speed.SetValue('2');\
         self.rml_panel.zjog.SetValue('1.0');"
      self.control_panel.defaults.Append('cut out board (1/32)')
      self.defaults["cut out board (1/32)"]\
      = "self.path_panel.diameter.SetValue('0.79');\
         self.path_panel.number.SetValue('1');\
         self.path_panel.frame3_itop.SetValue('0.5');\
         self.path_panel.frame3_ibot.SetValue('0.5');\
         self.path_panel.frame3_ztop.SetValue('-0.5');\
         self.path_panel.frame3_zbot.SetValue('-1.7');\
         self.path_panel.frame3_zstep.SetValue('0.5');\
         self.path_panel.frame3_xy.SetValue(True);\
         self.path_panel.frame3_xz.SetValue(False);\
         self.path_panel.frame3_yz.SetValue(False);\
         self.rml_panel.speed.SetValue('4');\
         self.rml_panel.zjog.SetValue('1.0');"
      self.control_panel.defaults.Append('wax rough cut (1/8)')
      self.defaults["wax rough cut (1/8)"]\
      = "self.path_panel.diameter.SetValue('3.175');\
         self.path_panel.number.SetValue('-1');\
         self.path_panel.overlap.SetValue('0.25');\
         self.path_panel.error.SetValue('1.5');\
         self.path_panel.frame3_xy.SetValue(True);\
         self.path_panel.frame3_xz.SetValue(False);\
         self.path_panel.frame3_yz.SetValue(False);\
         self.path_panel.frame3_zstep.SetValue('0.5');\
         self.path_panel.frame3_ibot.SetValue('0');\
         self.path_panel.frame3_itop.SetValue('1');\
         self.rml_panel.speed.SetValue('20');"
      self.control_panel.defaults.Append('wax finish cut (1/8)')
      self.defaults["wax finish cut (1/8)"]\
      = "self.path_panel.diameter.SetValue('3.175');\
         self.path_panel.number.SetValue('1');\
         self.path_panel.overlap.SetValue('0.5');\
         self.path_panel.error.SetValue('1.5');\
         self.path_panel.frame3_xy.SetValue(False);\
         self.path_panel.frame3_xz.SetValue(True);\
         self.path_panel.frame3_yz.SetValue(True);\
         self.path_panel.frame3_ibot.SetValue('0');\
         self.path_panel.frame3_itop.SetValue('1');\
         self.rml_panel.speed.SetValue('20');"
   #
   # set .cad .rml defaults
   #
   def set_cad_rml(self):
      self.defaults = {}
      self.control_panel.defaults.Append('mill traces (1/64)')
      self.defaults["mill traces (1/64)"]\
      = "self.png_panel.resolution.SetValue('50');\
         self.path_panel.diameter.SetValue('0.4');\
         self.path_panel.number.SetValue('4');\
         self.path_panel.z.SetValue('-0.1');\
         self.path_panel.frame3_ztop.SetValue('');\
         self.path_panel.frame3_zbot.SetValue('');\
         self.path_panel.frame3_zstep.SetValue('');\
         self.path_panel.frame3_xy.SetValue(False);\
         self.path_panel.frame3_xz.SetValue(False);\
         self.path_panel.frame3_yz.SetValue(False);\
         self.rml_panel.speed.SetValue('4');\
         self.rml_panel.zjog.SetValue('1.0');"
      self.control_panel.defaults.Append('mill traces (0.010)')
      self.defaults["mill traces (0.010)"]\
      = "self.png_panel.resolution.SetValue('50');\
         self.path_panel.diameter.SetValue('0.254');\
         self.path_panel.number.SetValue('1');\
         self.path_panel.z.SetValue('-0.1');\
         self.path_panel.frame3_ztop.SetValue('');\
         self.path_panel.frame3_zbot.SetValue('');\
         self.path_panel.frame3_zstep.SetValue('');\
         self.path_panel.frame3_xy.SetValue(False);\
         self.path_panel.frame3_xz.SetValue(False);\
         self.path_panel.frame3_yz.SetValue(False);\
         self.rml_panel.speed.SetValue('2');\
         self.rml_panel.zjog.SetValue('1.0');"
      self.control_panel.defaults.Append('cut out board (1/32)')
      self.defaults["cut out board (1/32)"]\
      = "self.png_panel.resolution.SetValue('50');\
         self.path_panel.diameter.SetValue('0.79');\
         self.path_panel.number.SetValue('1');\
         self.path_panel.frame3_itop.SetValue('0.5');\
         self.path_panel.frame3_ibot.SetValue('0.5');\
         self.path_panel.frame3_ztop.SetValue('-0.5');\
         self.path_panel.frame3_zbot.SetValue('-1.7');\
         self.path_panel.frame3_zstep.SetValue('0.5');\
         self.path_panel.frame3_xy.SetValue(True);\
         self.path_panel.frame3_xz.SetValue(False);\
         self.path_panel.frame3_yz.SetValue(False);\
         self.rml_panel.speed.SetValue('4');\
         self.rml_panel.zjog.SetValue('1.0');"
      self.control_panel.defaults.Append('wax rough cut (1/8)')
      self.defaults["wax rough cut (1/8)"]\
      = "self.png_panel.resolution.SetValue('25');\
         self.path_panel.diameter.SetValue('3.175');\
         self.path_panel.number.SetValue('-1');\
         self.path_panel.overlap.SetValue('0.25');\
         self.path_panel.error.SetValue('1.5');\
         self.path_panel.frame3_xy.SetValue(True);\
         self.path_panel.frame3_xz.SetValue(False);\
         self.path_panel.frame3_yz.SetValue(False);\
         self.path_panel.frame3_zstep.SetValue('0.5');\
         self.rml_panel.speed.SetValue('20');"
      self.control_panel.defaults.Append('wax finish cut (1/8)')
      self.defaults["wax finish cut (1/8)"]\
      = "self.png_panel.resolution.SetValue('25');\
         self.path_panel.diameter.SetValue('3.175');\
         self.path_panel.number.SetValue('1');\
         self.path_panel.overlap.SetValue('0.5');\
         self.path_panel.error.SetValue('1.5');\
         self.path_panel.frame3_xy.SetValue(False);\
         self.path_panel.frame3_xz.SetValue(True);\
         self.path_panel.frame3_yz.SetValue(True);\
         self.rml_panel.speed.SetValue('20');"
   #
   # set .math .rml defaults
   #
   def set_math_rml(self):
      self.defaults = {}
      self.control_panel.defaults.Append('mill traces (1/64)')
      self.defaults["mill traces (1/64)"]\
      = "self.png_panel.resolution.SetValue('50');\
         self.path_panel.diameter.SetValue('0.4');\
         self.path_panel.number.SetValue('4');\
         self.path_panel.z.SetValue('-0.1');\
         self.path_panel.frame3_ztop.SetValue('');\
         self.path_panel.frame3_zbot.SetValue('');\
         self.path_panel.frame3_zstep.SetValue('');\
         self.path_panel.frame3_xy.SetValue(False);\
         self.path_panel.frame3_xz.SetValue(False);\
         self.path_panel.frame3_yz.SetValue(False);\
         self.rml_panel.speed.SetValue('4');\
         self.rml_panel.zjog.SetValue('1.0');"
      self.control_panel.defaults.Append('mill traces (0.010)')
      self.defaults["mill traces (0.010)"]\
      = "self.path_panel.diameter.SetValue('0.254');\
         self.path_panel.number.SetValue('1');\
         self.path_panel.z.SetValue('-0.1');\
         self.path_panel.frame3_ztop.SetValue('');\
         self.path_panel.frame3_zbot.SetValue('');\
         self.path_panel.frame3_zstep.SetValue('');\
         self.path_panel.frame3_xy.SetValue(False);\
         self.path_panel.frame3_xz.SetValue(False);\
         self.path_panel.frame3_yz.SetValue(False);\
         self.rml_panel.speed.SetValue('2');\
         self.rml_panel.zjog.SetValue('1.0');"
      self.control_panel.defaults.Append('cut out board (1/32)')
      self.defaults["cut out board (1/32)"]\
      = "self.png_panel.resolution.SetValue('50');\
         self.path_panel.diameter.SetValue('0.79');\
         self.path_panel.number.SetValue('1');\
         self.path_panel.frame3_itop.SetValue('0.5');\
         self.path_panel.frame3_ibot.SetValue('0.5');\
         self.path_panel.frame3_ztop.SetValue('-0.5');\
         self.path_panel.frame3_zbot.SetValue('-1.7');\
         self.path_panel.frame3_zstep.SetValue('0.5');\
         self.path_panel.frame3_xy.SetValue(True);\
         self.path_panel.frame3_xz.SetValue(False);\
         self.path_panel.frame3_yz.SetValue(False);\
         self.rml_panel.speed.SetValue('4');\
         self.rml_panel.zjog.SetValue('1.0');"
      self.control_panel.defaults.Append('wax rough cut (1/8)')
      self.defaults["wax rough cut (1/8)"]\
      = "self.png_panel.resolution.SetValue('25');\
         self.path_panel.diameter.SetValue('3.175');\
         self.path_panel.number.SetValue('-1');\
         self.path_panel.overlap.SetValue('0.25');\
         self.path_panel.error.SetValue('1.5');\
         self.path_panel.frame3_xy.SetValue(True);\
         self.path_panel.frame3_xz.SetValue(False);\
         self.path_panel.frame3_yz.SetValue(False);\
         self.path_panel.frame3_zstep.SetValue('0.5');\
         self.rml_panel.speed.SetValue('20');"
      self.control_panel.defaults.Append('wax finish cut (1/8)')
      self.defaults["wax finish cut (1/8)"]\
      = "self.png_panel.resolution.SetValue('25');\
         self.path_panel.diameter.SetValue('3.175');\
         self.path_panel.number.SetValue('1');\
         self.path_panel.overlap.SetValue('0.5');\
         self.path_panel.error.SetValue('1.5');\
         self.path_panel.frame3_xy.SetValue(False);\
         self.path_panel.frame3_xz.SetValue(True);\
         self.path_panel.frame3_yz.SetValue(True);\
         self.rml_panel.speed.SetValue('20');"
   #
   # set .stl .rml defaults
   #
   def set_stl_rml(self):
      self.defaults = {}
      self.control_panel.defaults.Append('inches, 1/8, wax, rough')
      self.defaults["inches, 1/8, wax, rough"]\
      = "self.path_panel.diameter.SetValue('3.175');\
         self.path_panel.number.SetValue('-1');\
         self.path_panel.overlap.SetValue('0.25');\
         self.path_panel.error.SetValue('1.5');\
         self.path_panel.frame3_xy.SetValue(True);\
         self.path_panel.frame3_xz.SetValue(False);\
         self.path_panel.frame3_yz.SetValue(False);\
         self.path_panel.frame3_zstep.SetValue('0.75');\
         self.stl_png_panel.units.SetValue('25.4');\
         self.stl_png_panel.resolution.SetValue('25');\
         self.rml_panel.speed.SetValue('20');"
      self.control_panel.defaults.Append('inches, 1/8, wax, finish')
      self.defaults["inches, 1/8, wax, finish"]\
      = "self.path_panel.diameter.SetValue('3.175');\
         self.path_panel.number.SetValue('1');\
         self.path_panel.overlap.SetValue('0.5');\
         self.path_panel.error.SetValue('1.5');\
         self.path_panel.frame3_xy.SetValue(False);\
         self.path_panel.frame3_xz.SetValue(True);\
         self.path_panel.frame3_yz.SetValue(True);\
         self.stl_png_panel.units.SetValue('25.4');\
         self.stl_png_panel.resolution.SetValue('25');\
         self.rml_panel.speed.SetValue('20');"
      self.control_panel.defaults.Append('mm, 1/8, wax, rough')
      self.defaults["mm, 1/8, wax, rough"]\
      = "self.path_panel.diameter.SetValue('3.175');\
         self.path_panel.number.SetValue('-1');\
         self.path_panel.overlap.SetValue('0.25');\
         self.path_panel.error.SetValue('1.5');\
         self.path_panel.frame3_xy.SetValue(True);\
         self.path_panel.frame3_xz.SetValue(False);\
         self.path_panel.frame3_yz.SetValue(False);\
         self.path_panel.frame3_zstep.SetValue('0.75');\
         self.stl_png_panel.units.SetValue('1');\
         self.stl_png_panel.resolution.SetValue('25');\
         self.rml_panel.speed.SetValue('20');"
      self.control_panel.defaults.Append('mm, 1/8, wax, finish')
      self.defaults["mm, 1/8, wax, finish"]\
      = "self.path_panel.diameter.SetValue('3.175');\
         self.path_panel.number.SetValue('1');\
         self.path_panel.overlap.SetValue('0.5');\
         self.path_panel.error.SetValue('1.5');\
         self.path_panel.frame3_xy.SetValue(False);\
         self.path_panel.frame3_xz.SetValue(True);\
         self.path_panel.frame3_yz.SetValue(True);\
         self.stl_png_panel.units.SetValue('1');\
         self.stl_png_panel.resolution.SetValue('25');\
         self.rml_panel.speed.SetValue('20');"
   #
   # set .svg .rml defaults
   #
   def set_svg_rml(self):
      self.defaults = {}
      self.control_panel.defaults.Append('mill traces')
      self.defaults["mill traces"]\
      = "self.rml_panel.speed.SetValue('4');"
      self.control_panel.defaults.Append('cut out board')
      self.defaults["cut out board"]\
      = "self.rml_panel.speed.SetValue('0.5');"
      self.control_panel.defaults.Append('wax')
      self.defaults["wax"]\
      = "self.rml_panel.speed.SetValue('20');"
   #
   # set .png .sbp defaults
   #
   def set_png_sbp(self):
      self.defaults = {}
      self.control_panel.defaults.Append('wax rough cut (1/8)')
      self.defaults["wax rough cut (1/8)"]\
      = "self.path_panel.diameter.SetValue('3.175');\
         self.path_panel.number.SetValue('-1');\
         self.path_panel.overlap.SetValue('0.25');\
         self.path_panel.error.SetValue('1.5');\
         self.path_panel.frame3_xy.SetValue(True);\
         self.path_panel.frame3_xz.SetValue(False);\
         self.path_panel.frame3_yz.SetValue(False);\
         self.path_panel.frame3_zstep.SetValue('0.5');\
         self.path_panel.frame3_ibot.SetValue('0');\
         self.path_panel.frame3_itop.SetValue('1');\
         self.sbp_panel.speed.SetValue('20');"
      self.control_panel.defaults.Append('wax finish cut (1/8)')
      self.defaults["wax finish cut (1/8)"]\
      = "self.path_panel.diameter.SetValue('3.175');\
         self.path_panel.number.SetValue('1');\
         self.path_panel.overlap.SetValue('0.5');\
         self.path_panel.error.SetValue('1.5');\
         self.path_panel.frame3_xy.SetValue(False);\
         self.path_panel.frame3_xz.SetValue(True);\
         self.path_panel.frame3_yz.SetValue(True);\
         self.path_panel.frame3_ibot.SetValue('0');\
         self.path_panel.frame3_itop.SetValue('1');\
         self.sbp_panel.speed.SetValue('20');"
         
   #
   # set .png .plt defaults
   #  
   def set_png_plt(self):
      self.defaults = {}
   #
   # set .cad .sbp defaults
   #
   def set_cad_sbp(self):
      self.defaults = {}
      self.control_panel.defaults.Append('wax rough cut (1/8)')
      self.defaults["wax rough cut (1/8)"]\
      = "self.png_panel.resolution.SetValue('10');\
         self.path_panel.diameter.SetValue('3.175');\
         self.path_panel.number.SetValue('-1');\
         self.path_panel.overlap.SetValue('0.25');\
         self.path_panel.error.SetValue('1.5');\
         self.path_panel.frame3_xy.SetValue(True);\
         self.path_panel.frame3_xz.SetValue(False);\
         self.path_panel.frame3_yz.SetValue(False);\
         self.path_panel.frame3_zstep.SetValue('0.5');\
         self.path_panel.frame3_ibot.SetValue('0');\
         self.path_panel.frame3_itop.SetValue('1');\
         self.sbp_panel.speed.SetValue('20');"
      self.control_panel.defaults.Append('wax finish cut (1/8)')
      self.defaults["wax finish cut (1/8)"]\
      = "self.png_panel.resolution.SetValue('10');\
         self.path_panel.diameter.SetValue('3.175');\
         self.path_panel.number.SetValue('1');\
         self.path_panel.overlap.SetValue('0.5');\
         self.path_panel.error.SetValue('1.5');\
         self.path_panel.frame3_xy.SetValue(False);\
         self.path_panel.frame3_xz.SetValue(True);\
         self.path_panel.frame3_yz.SetValue(True);\
         self.path_panel.frame3_ibot.SetValue('0');\
         self.path_panel.frame3_itop.SetValue('1');\
         self.sbp_panel.speed.SetValue('20');"
   #
   # set .math .sbp defaults
   #
   def set_math_sbp(self):
      self.defaults = {}
      self.control_panel.defaults.Append('wax rough cut (1/8)')
      self.defaults["wax rough cut (1/8)"]\
      = "self.png_panel.resolution.SetValue('10');\
         self.path_panel.diameter.SetValue('3.175');\
         self.path_panel.number.SetValue('-1');\
         self.path_panel.overlap.SetValue('0.25');\
         self.path_panel.error.SetValue('1.5');\
         self.path_panel.frame3_xy.SetValue(True);\
         self.path_panel.frame3_xz.SetValue(False);\
         self.path_panel.frame3_yz.SetValue(False);\
         self.path_panel.frame3_zstep.SetValue('0.5');\
         self.path_panel.frame3_ibot.SetValue('0');\
         self.path_panel.frame3_itop.SetValue('1');\
         self.sbp_panel.speed.SetValue('20');"
      self.control_panel.defaults.Append('wax finish cut (1/8)')
      self.defaults["wax finish cut (1/8)"]\
      = "self.png_panel.resolution.SetValue('10');\
         self.path_panel.diameter.SetValue('3.175');\
         self.path_panel.number.SetValue('1');\
         self.path_panel.overlap.SetValue('0.5');\
         self.path_panel.error.SetValue('1.5');\
         self.path_panel.frame3_xy.SetValue(False);\
         self.path_panel.frame3_xz.SetValue(True);\
         self.path_panel.frame3_yz.SetValue(True);\
         self.path_panel.frame3_ibot.SetValue('0');\
         self.path_panel.frame3_itop.SetValue('1');\
         self.sbp_panel.speed.SetValue('20');"
   #
   # set .stl .sbp defaults
   #
   def set_stl_sbp(self):
      self.defaults = {}
      self.control_panel.defaults.Append('inches, 1/8, wax, rough')
      self.defaults["inches, 1/8, wax, rough"]\
      = "self.path_panel.diameter.SetValue('3.175');\
         self.path_panel.number.SetValue('-1');\
         self.path_panel.overlap.SetValue('0.25');\
         self.path_panel.error.SetValue('1.5');\
         self.path_panel.frame3_xy.SetValue(True);\
         self.path_panel.frame3_xz.SetValue(False);\
         self.path_panel.frame3_yz.SetValue(False);\
         self.path_panel.frame3_zstep.SetValue('0.75');\
         self.stl_png_panel.units.SetValue('25.4');\
         self.stl_png_panel.resolution.SetValue('25');\
         self.sbp_panel.speed.SetValue('20');"
      self.control_panel.defaults.Append('inches, 1/8, wax, finish')
      self.defaults["inches, 1/8, wax, finish"]\
      = "self.path_panel.diameter.SetValue('3.175');\
         self.path_panel.number.SetValue('1');\
         self.path_panel.overlap.SetValue('0.5');\
         self.path_panel.error.SetValue('1.5');\
         self.path_panel.frame3_xy.SetValue(False);\
         self.path_panel.frame3_xz.SetValue(True);\
         self.path_panel.frame3_yz.SetValue(True);\
         self.stl_png_panel.units.SetValue('25.4');\
         self.stl_png_panel.resolution.SetValue('25');\
         self.sbp_panel.speed.SetValue('20');"
      self.control_panel.defaults.Append('mm, 1/8, wax, rough')
      self.defaults["mm, 1/8, wax, rough"]\
      = "self.path_panel.diameter.SetValue('3.175');\
         self.path_panel.number.SetValue('-1');\
         self.path_panel.overlap.SetValue('0.25');\
         self.path_panel.error.SetValue('1.5');\
         self.path_panel.frame3_xy.SetValue(True);\
         self.path_panel.frame3_xz.SetValue(False);\
         self.path_panel.frame3_yz.SetValue(False);\
         self.path_panel.frame3_zstep.SetValue('0.75');\
         self.stl_png_panel.units.SetValue('1');\
         self.stl_png_panel.resolution.SetValue('25');\
         self.sbp_panel.speed.SetValue('20');"
      self.control_panel.defaults.Append('mm, 1/8, wax, finish')
      self.defaults["mm, 1/8, wax, finish"]\
      = "self.path_panel.diameter.SetValue('3.175');\
         self.path_panel.number.SetValue('1');\
         self.path_panel.overlap.SetValue('0.5');\
         self.path_panel.error.SetValue('1.5');\
         self.path_panel.frame3_xy.SetValue(False);\
         self.path_panel.frame3_xz.SetValue(True);\
         self.path_panel.frame3_yz.SetValue(True);\
         self.stl_png_panel.units.SetValue('1');\
         self.stl_png_panel.resolution.SetValue('25');\
         self.sbp_panel.speed.SetValue('20');"
   #
   # set .svg .sbp defaults
   #
   def set_svg_sbp(self):
      self.defaults = {}
      self.control_panel.defaults.Append('mill traces')
      self.defaults["mill traces"]\
      = "self.sbp_panel.speed.SetValue('4');"
      self.control_panel.defaults.Append('cut out board')
      self.defaults["cut out board"]\
      = "self.sbp_panel.speed.SetValue('0.5');"
      self.control_panel.defaults.Append('wax')
      self.defaults["wax"]\
      = "self.sbp_panel.speed.SetValue('20');"
   #
   # set .png .g defaults
   #
   def set_png_g(self):
      self.defaults = {}
      self.control_panel.defaults.Append('mill traces (1/64)')
      self.defaults["mill traces (1/64)"]\
      = "self.path_panel.diameter.SetValue('0.4');\
         self.path_panel.number.SetValue('4');\
         self.path_panel.z.SetValue('-0.1');\
         self.path_panel.frame3_ztop.SetValue('');\
         self.path_panel.frame3_zbot.SetValue('');\
         self.path_panel.frame3_zstep.SetValue('');\
         self.path_panel.frame3_xy.SetValue(False);\
         self.path_panel.frame3_xz.SetValue(False);\
         self.path_panel.frame3_yz.SetValue(False);\
         self.g_panel.speed.SetValue('4');"
      self.control_panel.defaults.Append('cut out board (1/32)')
      self.defaults["cut out board (1/32)"]\
      = "self.path_panel.diameter.SetValue('0.79');\
         self.path_panel.number.SetValue('1');\
         self.path_panel.frame3_itop.SetValue('0.5');\
         self.path_panel.frame3_ibot.SetValue('0.5');\
         self.path_panel.frame3_ztop.SetValue('-0.5');\
         self.path_panel.frame3_zbot.SetValue('-1.7');\
         self.path_panel.frame3_zstep.SetValue('0.5');\
         self.path_panel.frame3_xy.SetValue(True);\
         self.path_panel.frame3_xz.SetValue(False);\
         self.path_panel.frame3_yz.SetValue(False);\
         self.g_panel.speed.SetValue('0.4');"
      self.control_panel.defaults.Append('wax (1/8)')
      self.defaults["wax (1/8)"]\
      = "self.path_panel.diameter.SetValue('3.175');\
         self.path_panel.number.SetValue('1');\
         self.g_panel.speed.SetValue('20');"
   #
   # set .cad .g defaults
   #
   def set_cad_g(self):
      self.defaults = {}
      self.control_panel.defaults.Append('mill traces (1/64)')
      self.defaults["mill traces (1/64)"]\
      = "self.png_panel.resolution.SetValue('50');\
         self.path_panel.diameter.SetValue('0.4');\
         self.path_panel.number.SetValue('4');\
         self.path_panel.z.SetValue('-0.1');\
         self.path_panel.frame3_ztop.SetValue('');\
         self.path_panel.frame3_zbot.SetValue('');\
         self.path_panel.frame3_zstep.SetValue('');\
         self.g_panel.speed.SetValue('4');"
      self.control_panel.defaults.Append('cut out board (1/32)')
      self.defaults["cut out board (1/32)"]\
      = "self.png_panel.resolution.SetValue('50');\
         self.path_panel.diameter.SetValue('0.79');\
         self.path_panel.number.SetValue('1');\
         self.path_panel.frame3_itop.SetValue('0.5');\
         self.path_panel.frame3_ibot.SetValue('0.5');\
         self.path_panel.frame3_ztop.SetValue('-0.5');\
         self.path_panel.frame3_zbot.SetValue('-1.7');\
         self.path_panel.frame3_zstep.SetValue('0.5');\
         self.g_panel.speed.SetValue('4');"
      self.control_panel.defaults.Append('wax (1/8)')
      self.control_panel.defaults.Append('wax rough cut (1/8)')
      self.defaults["wax rough cut (1/8)"]\
      = "self.png_panel.resolution.SetValue('25');\
         self.path_panel.diameter.SetValue('3.175');\
         self.path_panel.number.SetValue('-1');\
         self.path_panel.overlap.SetValue('0.25');\
         self.path_panel.error.SetValue('1.5');\
         self.path_panel.frame3_xy.SetValue(True);\
         self.path_panel.frame3_xz.SetValue(False);\
         self.path_panel.frame3_yz.SetValue(False);\
         self.path_panel.frame3_zstep.SetValue('0.5');\
         self.path_panel.frame3_ibot.SetValue('0');\
         self.path_panel.frame3_itop.SetValue('1');\
         self.g_panel.speed.SetValue('20');"
      self.control_panel.defaults.Append('wax finish cut (1/8)')
      self.defaults["wax finish cut (1/8)"]\
      = "self.png_panel.resolution.SetValue('25');\
         self.path_panel.diameter.SetValue('3.175');\
         self.path_panel.number.SetValue('1');\
         self.path_panel.overlap.SetValue('0.5');\
         self.path_panel.error.SetValue('1.5');\
         self.path_panel.frame3_xy.SetValue(False);\
         self.path_panel.frame3_xz.SetValue(True);\
         self.path_panel.frame3_yz.SetValue(True);\
         self.path_panel.frame3_ibot.SetValue('0');\
         self.path_panel.frame3_itop.SetValue('1');\
         self.g_panel.speed.SetValue('20');"
   #
   # set .math .g defaults
   #
   def set_math_g(self):
      self.defaults = {}
      self.control_panel.defaults.Append('mill traces (1/64)')
      self.defaults["mill traces (1/64)"]\
      = "self.png_panel.resolution.SetValue('50');\
         self.path_panel.diameter.SetValue('0.4');\
         self.path_panel.number.SetValue('4');\
         self.path_panel.z.SetValue('-0.1');\
         self.path_panel.frame3_ztop.SetValue('');\
         self.path_panel.frame3_zbot.SetValue('');\
         self.path_panel.frame3_zstep.SetValue('');\
         self.g_panel.speed.SetValue('4');"
      self.control_panel.defaults.Append('cut out board (1/32)')
      self.defaults["cut out board (1/32)"]\
      = "self.png_panel.resolution.SetValue('50');\
         self.path_panel.diameter.SetValue('0.79');\
         self.path_panel.number.SetValue('1');\
         self.path_panel.frame3_itop.SetValue('0.5');\
         self.path_panel.frame3_ibot.SetValue('0.5');\
         self.path_panel.frame3_ztop.SetValue('-0.5');\
         self.path_panel.frame3_zbot.SetValue('-1.7');\
         self.path_panel.frame3_zstep.SetValue('0.5');\
         self.g_panel.speed.SetValue('4');"
      self.control_panel.defaults.Append('wax (1/8)')
      self.control_panel.defaults.Append('wax rough cut (1/8)')
      self.defaults["wax rough cut (1/8)"]\
      = "self.png_panel.resolution.SetValue('25');\
         self.path_panel.diameter.SetValue('3.175');\
         self.path_panel.number.SetValue('-1');\
         self.path_panel.overlap.SetValue('0.25');\
         self.path_panel.error.SetValue('1.5');\
         self.path_panel.frame3_xy.SetValue(True);\
         self.path_panel.frame3_xz.SetValue(False);\
         self.path_panel.frame3_yz.SetValue(False);\
         self.path_panel.frame3_zstep.SetValue('0.5');\
         self.path_panel.frame3_ibot.SetValue('0');\
         self.path_panel.frame3_itop.SetValue('1');\
         self.g_panel.speed.SetValue('20');"
      self.control_panel.defaults.Append('wax finish cut (1/8)')
      self.defaults["wax finish cut (1/8)"]\
      = "self.png_panel.resolution.SetValue('25');\
         self.path_panel.diameter.SetValue('3.175');\
         self.path_panel.number.SetValue('1');\
         self.path_panel.overlap.SetValue('0.5');\
         self.path_panel.error.SetValue('1.5');\
         self.path_panel.frame3_xy.SetValue(False);\
         self.path_panel.frame3_xz.SetValue(True);\
         self.path_panel.frame3_yz.SetValue(True);\
         self.path_panel.frame3_ibot.SetValue('0');\
         self.path_panel.frame3_itop.SetValue('1');\
         self.g_panel.speed.SetValue('20');"
   #
   # set .stl .g defaults
   #
   def set_stl_g(self):
      self.defaults = {}
      self.control_panel.defaults.Append('inches, 1/8, wax, rough')
      self.defaults["inches, 1/8, wax, rough"]\
      = "self.path_panel.diameter.SetValue('3.175');\
         self.path_panel.number.SetValue('-1');\
         self.path_panel.overlap.SetValue('0.25');\
         self.path_panel.error.SetValue('1.5');\
         self.path_panel.frame3_xy.SetValue(True);\
         self.path_panel.frame3_xz.SetValue(False);\
         self.path_panel.frame3_yz.SetValue(False);\
         self.path_panel.frame3_zstep.SetValue('0.75');\
         self.stl_png_panel.units.SetValue('25.4');\
         self.stl_png_panel.resolution.SetValue('25');\
         self.g_panel.speed.SetValue('20');"
      self.control_panel.defaults.Append('inches, 1/8, wax, finish')
      self.defaults["inches, 1/8, wax, finish"]\
      = "self.path_panel.diameter.SetValue('3.175');\
         self.path_panel.number.SetValue('1');\
         self.path_panel.overlap.SetValue('0.5');\
         self.path_panel.error.SetValue('1.5');\
         self.path_panel.frame3_xy.SetValue(False);\
         self.path_panel.frame3_xz.SetValue(True);\
         self.path_panel.frame3_yz.SetValue(True);\
         self.stl_png_panel.units.SetValue('25.4');\
         self.stl_png_panel.resolution.SetValue('25');\
         self.g_panel.speed.SetValue('20');"
      self.control_panel.defaults.Append('mm, 1/8, wax, rough')
      self.defaults["mm, 1/8, wax, rough"]\
      = "self.path_panel.diameter.SetValue('3.175');\
         self.path_panel.number.SetValue('-1');\
         self.path_panel.overlap.SetValue('0.25');\
         self.path_panel.error.SetValue('1.5');\
         self.path_panel.frame3_xy.SetValue(True);\
         self.path_panel.frame3_xz.SetValue(False);\
         self.path_panel.frame3_yz.SetValue(False);\
         self.path_panel.frame3_zstep.SetValue('0.75');\
         self.stl_png_panel.units.SetValue('1');\
         self.stl_png_panel.resolution.SetValue('25');\
         self.g_panel.speed.SetValue('20');"
      self.control_panel.defaults.Append('mm, 1/8, wax, finish')
      self.defaults["mm, 1/8, wax, finish"]\
      = "self.path_panel.diameter.SetValue('3.175');\
         self.path_panel.number.SetValue('1');\
         self.path_panel.overlap.SetValue('0.5');\
         self.path_panel.error.SetValue('1.5');\
         self.path_panel.frame3_xy.SetValue(False);\
         self.path_panel.frame3_xz.SetValue(True);\
         self.path_panel.frame3_yz.SetValue(True);\
         self.stl_png_panel.units.SetValue('1');\
         self.stl_png_panel.resolution.SetValue('25');\
         self.g_panel.speed.SetValue('20');"
   #
   # set .svg .g defaults
   #
   def set_svg_g(self):
      self.defaults = {}
      self.control_panel.defaults.Append('mill traces')
      self.defaults["mill traces"]\
      = "self.g_panel.speed.SetValue('4');"
      self.control_panel.defaults.Append('cut out board')
      self.defaults["cut out board"]\
      = "self.g_panel.speed.SetValue('0.5');"
      self.control_panel.defaults.Append('wax')
      self.defaults["wax"]\
      = "self.g_panel.speed.SetValue('20');"
   #
   # set .png .ps defaults
   #
   def set_png_ps(self):
      self.defaults = {}
      self.control_panel.defaults.Append('outline')
      self.defaults["outline"]\
      = "self.path_panel.error.SetValue('1');\
         self.path_panel.diameter.SetValue('0');\
         self.path_panel.number.SetValue('1');"
      self.control_panel.defaults.Append('mill traces (1/64)')
      self.defaults["mill traces (1/64)"]\
      = "self.path_panel.error.SetValue('1');\
         self.path_panel.diameter.SetValue('0.4');\
         self.path_panel.number.SetValue('4');"
      self.control_panel.defaults.Append('cut out board (1/32)')
      self.defaults["cut out board (1/32)"]\
      = "self.path_panel.error.SetValue('1');\
         self.path_panel.diameter.SetValue('0.8');\
         self.path_panel.number.SetValue('1');"
   #
   # set .cad .ps defaults
   #
   def set_cad_ps(self):
      self.defaults = {}
      self.control_panel.defaults.Append('outline')
      self.defaults["outline"]\
      = "self.png_panel.resolution.SetValue('50');\
         self.path_panel.error.SetValue('1');\
         self.path_panel.diameter.SetValue('0');\
         self.path_panel.number.SetValue('1');"
      self.control_panel.defaults.Append('mill traces (1/64)')
      self.defaults["mill traces (1/64)"]\
      = "self.png_panel.resolution.SetValue('50');\
         self.path_panel.error.SetValue('1');\
         self.path_panel.diameter.SetValue('0.4');\
         self.path_panel.number.SetValue('4');"
      self.control_panel.defaults.Append('cut out board (1/32)')
      self.defaults["cut out board (1/32)"]\
      = "self.png_panel.resolution.SetValue('50');\
         self.path_panel.error.SetValue('1');\
         self.path_panel.diameter.SetValue('0.8');\
         self.path_panel.number.SetValue('1');"
   #
   # set .math .ps defaults
   #
   def set_math_ps(self):
      self.defaults = {}
      self.control_panel.defaults.Append('outline')
      self.defaults["outline"]\
      = "self.png_panel.resolution.SetValue('50');\
         self.path_panel.error.SetValue('1');\
         self.path_panel.diameter.SetValue('0');\
         self.path_panel.number.SetValue('1');"
      self.control_panel.defaults.Append('mill traces (1/64)')
      self.defaults["mill traces (1/64)"]\
      = "self.png_panel.resolution.SetValue('50');\
         self.path_panel.error.SetValue('1');\
         self.path_panel.diameter.SetValue('0.4');\
         self.path_panel.number.SetValue('4');"
      self.control_panel.defaults.Append('cut out board (1/32)')
      self.defaults["cut out board (1/32)"]\
      = "self.png_panel.resolution.SetValue('50');\
         self.path_panel.error.SetValue('1');\
         self.path_panel.diameter.SetValue('0.8');\
         self.path_panel.number.SetValue('1');"
   #
   # set .svg .ps defaults
   #
   def set_svg_ps(self):
      self.defaults = {}
      self.control_panel.defaults.Append('outline')
      self.defaults["outline"]\
      = "self.png_panel.resolution.SetValue('50');\
         self.path_panel.error.SetValue('1');\
         self.path_panel.diameter.SetValue('0');\
         self.path_panel.number.SetValue('1');"
      self.control_panel.defaults.Append('mill traces (1/64)')
      self.defaults["mill traces (1/64)"]\
      = "self.png_panel.resolution.SetValue('50');\
         self.path_panel.error.SetValue('1');\
         self.path_panel.diameter.SetValue('0.4');\
         self.path_panel.number.SetValue('4');"
      self.control_panel.defaults.Append('cut out board (1/32)')
      self.defaults["cut out board (1/32)"]\
      = "self.png_panel.resolution.SetValue('50');\
         self.path_panel.error.SetValue('1');\
         self.path_panel.diameter.SetValue('0.8');\
         self.path_panel.number.SetValue('1');"
   #
   # set .png .camm defaults
   #
   def set_png_camm(self):
      self.defaults = {}
      self.control_panel.defaults.Append('vinyl')
      self.defaults["vinyl"]\
      = "self.path_panel.error.SetValue('1.5');\
         self.path_panel.diameter.SetValue('.25');\
         self.path_panel.number.SetValue('1');\
         self.camm_panel.force.SetValue('45');\
         self.camm_panel.velocity.SetValue('5');"
      self.control_panel.defaults.Append('copper')
      self.defaults["copper"]\
      = "self.path_panel.error.SetValue('1.5');\
         self.path_panel.diameter.SetValue('.25');\
         self.path_panel.number.SetValue('1');\
         self.camm_panel.force.SetValue('55');\
         self.camm_panel.velocity.SetValue('2.5');"
      self.control_panel.defaults.Append('epoxy')
      self.defaults["epoxy"]\
      = "self.path_panel.error.SetValue('1.5');\
         self.path_panel.diameter.SetValue('.25');\
         self.path_panel.number.SetValue('1');\
         self.camm_panel.force.SetValue('90');\
         self.camm_panel.velocity.SetValue('2.5');"
   #
   # set .cad .camm defaults
   #
   def set_cad_camm(self):
      self.defaults = {}
      self.control_panel.defaults.Append('vinyl')
      self.defaults["vinyl"]\
      = "self.path_panel.error.SetValue('1.5');\
         self.path_panel.diameter.SetValue('.25');\
         self.path_panel.number.SetValue('1');\
         self.png_panel.resolution.SetValue('10');\
         self.camm_panel.force.SetValue('45');\
         self.camm_panel.velocity.SetValue('5');"
      self.control_panel.defaults.Append('copper')
      self.defaults["copper"]\
      = "self.path_panel.error.SetValue('1.5');\
         self.path_panel.diameter.SetValue('.25');\
         self.path_panel.number.SetValue('1');\
         self.png_panel.resolution.SetValue('10');\
         self.camm_panel.force.SetValue('55');\
         self.camm_panel.velocity.SetValue('2.5');"
      self.control_panel.defaults.Append('epoxy')
      self.defaults["epoxy"]\
      = "self.path_panel.error.SetValue('1.5');\
         self.path_panel.diameter.SetValue('.25');\
         self.path_panel.number.SetValue('1');\
         self.png_panel.resolution.SetValue('10');\
         self.camm_panel.force.SetValue('90');\
         self.camm_panel.velocity.SetValue('2.5');"
   #
   # set .math .camm defaults
   #
   def set_math_camm(self):
      self.defaults = {}
      self.control_panel.defaults.Append('vinyl')
      self.defaults["vinyl"]\
      = "self.path_panel.error.SetValue('1.5');\
         self.path_panel.diameter.SetValue('.25');\
         self.path_panel.number.SetValue('1');\
         self.png_panel.resolution.SetValue('10');\
         self.camm_panel.force.SetValue('45');\
         self.camm_panel.velocity.SetValue('5');"
      self.control_panel.defaults.Append('copper')
      self.defaults["copper"]\
      = "self.path_panel.error.SetValue('1.5');\
         self.path_panel.diameter.SetValue('.25');\
         self.path_panel.number.SetValue('1');\
         self.png_panel.resolution.SetValue('10');\
         self.camm_panel.force.SetValue('55');\
         self.camm_panel.velocity.SetValue('2.5');"
      self.control_panel.defaults.Append('epoxy')
      self.defaults["epoxy"]\
      = "self.path_panel.error.SetValue('1.5');\
         self.path_panel.diameter.SetValue('.25');\
         self.path_panel.number.SetValue('1');\
         self.png_panel.resolution.SetValue('10');\
         self.camm_panel.force.SetValue('90');\
         self.camm_panel.velocity.SetValue('2.5');"
   #
   # set .svg .camm defaults
   #
   def set_svg_camm(self):
      self.defaults = {}
      self.control_panel.defaults.Append('vinyl')
      self.defaults["vinyl"]\
      = "self.camm_panel.force.SetValue('45');\
         self.camm_panel.velocity.SetValue('5');"
      self.control_panel.defaults.Append('copper')
      self.defaults["copper"]\
      = "self.camm_panel.force.SetValue('55');\
         self.camm_panel.velocity.SetValue('2.5');"
      self.control_panel.defaults.Append('epoxy')
      self.defaults["epoxy"]\
      = "self.camm_panel.force.SetValue('90');\
         self.camm_panel.velocity.SetValue('2.5');"
   #
   # set .png .ord defaults
   #
   def set_png_ord(self):
      self.defaults = {}
   #
   # set .cad .ord defaults
   #
   def set_cad_ord(self):
      self.defaults = {}
   #
   # set .math .ord defaults
   #
   def set_math_ord(self):
      self.defaults = {}
   #
   # set .svg .ord defaults
   #
   def set_svg_ord(self):
      self.defaults = {}
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

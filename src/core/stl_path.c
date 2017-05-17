//
// stl_path.c
//    convert STL to path
//
// Neil Gershenfeld
// CBA MIT 11/7/10
//
// (c) Massachusetts Institute of Technology 2010
// Permission granted for experimental and personal use;
// license for commercial sale available from MIT.
//

#include "fab.h"

main(int argc, char **argv) {
   //
   // local vars
   //
   struct fab_vars v;
   init_vars(&v);
   float units,resolution,error,offset_diameter,offset_overlap,z_thickness,z_top,z_bottom;
   int offset_number;
   char axis,cmd[100];
   //
   // command line args
   //
   if (!((argc == 3) || (argc == 4) || (argc == 5) || (argc == 6) || (argc == 7) || (argc == 8) || (argc == 9) || (argc == 10) || (argc == 11) || (argc == 12))) {
      printf("command line: stl_path in.stl out.path [units [resolution [error [offset_diameter [offset_number [offset_overlap [z_thickness [z_top [z_bottom]]]]]]]]]\n");
      printf("   in.stl = input binary STL file\n");
      printf("   out.path = output path file\n");
      printf("   units = file units (optional, mm/unit, default 1)\n");
      printf("   resolution = image resolution (optional, pixels/mm, default 10)\n");
      printf("   error = allowable vector fit deviation (optional, pixels, default 1.1)\n");
      printf("   offset_diameter = diameter to offset (optional, mm, default 0)\n");
      printf("   offset_number = number of contours to offset (optional, -1 to fill all, default 1)\n");
      printf("   offset_overlap = tool offset overlap fraction (optional, 0 (no overlap) - 1 (complete overlap, default 0.5))\n");
      printf("   z_thickness = slice z thickness (optional, mm, default STL value)\n");
      printf("   z_top = top slice z value (optional, mm, default STL value)\n");
      printf("   z_bottom = bottom slice z value (optional, mm, default STL value)\n");
      exit(-1);
      }
   axis = 'z';
   units = 1;
   if (argc > 3)
      sscanf(argv[3],"%f",&units);
   resolution = 10;
   if (argc > 4) {
      sscanf(argv[4],"%f",&resolution);
      }
   error = 1.1;
   if (argc > 5)
      sscanf(argv[5],"%f",&error);
   offset_diameter = 0;
   if (argc > 6)
      sscanf(argv[6],"%f",&offset_diameter);
   offset_number = 1;
   if (argc > 7)
      sscanf(argv[7],"%d",&offset_number);
   offset_overlap = .5;
   if (argc > 8)
      sscanf(argv[8],"%f",&offset_overlap);
   //
   //  read STL
   //
   fab_read_stl(&v,argv[1]);
   //
   // draw mesh into array
   //
   fab_shade_mesh(&v,units,resolution,axis);
   //
   //  write PNG
   //
   fab_write_png_K(&v,"stl_path.png");
   //
   // call png_path
   //
   z_thickness = v.dz;
   if (argc > 9)
      sscanf(argv[9],"%f",&z_thickness);
   z_top = v.zmin + v.dz;
   if (argc > 10)
      sscanf(argv[10],"%f",&z_top);
   z_bottom = v.zmin;
   if (argc > 11)
      sscanf(argv[11],"%f",&z_bottom);
   sprintf(cmd,"png_path %s %s %f %f %d %f 1 0 %f %f %f","stl_path.png",argv[2],error,offset_diameter,offset_number,offset_overlap,z_top,z_bottom,z_thickness);
   system(cmd);
   }

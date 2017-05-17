//
// svg_path.c
//    convert SVG to path
//
// Neil Gershenfeld
// CBA MIT 5/17/13
//
// (c) Massachusetts Institute of Technology 2012
// Permission granted for experimental and personal use;
// license for commercial sale available from MIT.
//
// todo
//    g element transforms
//    path arc flags
//    compound transformations
//    unstroked elements
//

#include "fab.h"

#define SVG_MAX_FILE 1000000
   
//
// parse quoted number and units
// return scale in mm/unit
// 
void parse_number_units(char *ptr, double *number, double *scale, char *units) {
   char *start,*end;
   start = strstr(ptr,"\"");
   end = strstr(start+1,"\"");
   char c1,c2;
   c1 = *(end-1);
   c2 = *(end-2);
   if ((((c2 >= '0') && (c2 <= '9')) || (c2 == '.'))
   && (((c1 >= '0') && (c1 <= '9')) || (c1 == '.'))) {
      *number = strtod(start+1,NULL);
      strcpy(units,"px");
      }
   else {
      units[0] = *(end-2);
      units[1] = *(end-1);
      units[2] = 0;
      *(end-2) = ' ';
      *(end-1) = ' ';
      *number = strtod(start+1,NULL);
      }
   if (0 == strncmp(units,"px",2))
      *scale = 25.4*1.0/90.0; // Inkscape px default 90/inch
   else if (0 == strncmp(units,"pt",2))
      *scale = 25.4*1.0/72.0;
   else if (0 == strncmp(units,"in",2))
      *scale = 25.4;
   else if (0 == strncmp(units,"mm",2))
      *scale = 1.0;
   else if (0 == strncmp(units,"cm",2))
      *scale = 10.0;
   else {
      printf("fab.c: oops -- don't recognize unit %s\n",units);
      exit(-1);
      }
   }
//
// return next number after pointer
//
void next_number(char **ptr, double *number) {
   char haystack[] = "0123456789.-+";
   char *end;
   //
   // find start
   //
   while (1) {
      if (strchr(haystack,**ptr) != NULL)
         break;
      *ptr += 1;
      }
   //
   // find end
   //
   end = *ptr;
   while (1) {
      if (strchr(haystack,*end) == NULL)
         break;
      end += 1;
      }
   //
   // move pointer to end and return number
   //
   *number = strtod(*ptr,&end);
   *ptr = end;
   }
   
//
// return next element after pointer
//
char next_element(char **ptr, char current_element) {
   char number_haystack[] = "0123456789.-+";
   char element_haystack[] = "mMlLcCsSaAzZ\"";
   while (1) {
      if (strchr(element_haystack,**ptr) != NULL)
         return(**ptr);
      else if (strchr(number_haystack,**ptr) != NULL)
         return(current_element);
      else
         *ptr += 1;
      }
   }
   
//
// set transformation matrix for element at start
//
void set_transform(char *start, double *a, double *b, double *c, double *d, double *e, double *f) {
   char *end,*ptr;
   end = strstr(start,"/>");
   //
   // check for transform
   //
   ptr = strstr(start,"transform");
   if ((ptr != NULL) && (ptr < end)) {
      //
      // found, check for matrix
      //
      ptr = strstr(start,"matrix(");
      if ((ptr != NULL) && (ptr < end)) {
         next_number(&ptr,a);
         next_number(&ptr,b);
         next_number(&ptr,c);
         next_number(&ptr,d);
         next_number(&ptr,e);
         next_number(&ptr,f);
         }
      //
      // check for translate
      //
      ptr = strstr(start,"translate(");
      if ((ptr != NULL) && (ptr < end)) {
         *a = 1;
         *b = 0;
         *c = 0;
         *d = 1;
         next_number(&ptr,e);
         next_number(&ptr,f);
         }
      }
   else {
      //
      // not found, set unit transform
      //
      *a = 1;
      *b = 0;
      *c = 0;
      *d = 1;
      *e = 0;
      *f = 0;
      }
   }

//
// return transformed and scaled x coordinate
//
int xn_(double x, double y, double a, double c, double e, double xscale, double vxmin) {
   int xn;
   xn = xscale * ((a*x + c*y + e) - vxmin);
   return xn;
   }

//
// return transformed and scaled y coordinate
//

int yn_(double x, double y, double b, double d, double f, double yscale, double vymin) {
   int yn;
   yn = yscale * ((b*x + d*y + f) - vymin);
   return yn;
   }

void fab_read_svg(struct fab_vars *v, char *input_file_name, int points, int resolution, float z) {
   //
   // read SVG into fab_vars
   //
	FILE *input_file;
   char buf[SVG_MAX_FILE];
   char units[3];
   char current_element;
   int point,ret;
   char *ptr,*start,*endptr;
   double number,scale,xscale,yscale,vxmin,vymin,vwidth,vheight,width,height,a,b,c,d,e,f;
   double x,y,x0,y0,x1,y1,x2,y2;
   double rx,ry,t0,t1,tdiff,tsum,rotation,large_arc,sweep;
   double ax,bx,cx,ay,by,cy,xt,yt,t,r;
   double pi;
   pi = 4*atan(1.0);
   //
   // read SVG file
   //
   input_file = fopen(input_file_name, "rb");
   if (input_file == 0) {
      printf("fab.c: oops -- can't open %s\n",input_file_name);
      exit(-1);
      }
   ret = fread(buf,1,SVG_MAX_FILE,input_file);
   if (ret >= SVG_MAX_FILE) {
      printf("fab.c: oops -- exceeded SVG buffer size\n");
      exit(-1);
      }
   endptr = buf + ret;
   fclose(input_file);
   printf("read %d bytes from %s\n",ret,input_file_name);
   //
   // find SVG element
   //
   ptr = strstr(buf,"<svg");
   if (ptr == NULL) {
      printf("fab.c: oops -- no SVG element\n");
      exit(-1);
      }
   //
   // check for width and height
   //
   start = strstr(ptr,"width=");
   if (start == NULL) {
      printf("fab.c: oops -- no width\n");
      exit(-1);
      }
   parse_number_units(start,&number,&scale,units);
   printf("   width %f %s\n",number,units);
   width = number * scale;
   start = strstr(ptr,"height=");
   if (start == NULL) {
      printf("fab.c: oops -- no height\n");
      exit(-1);
      }
   parse_number_units(start,&number,&scale,units);
   printf("   height %f %s\n",number,units);
   height = number * scale;
   //
   // check for viewBox
   //
   start = strstr(ptr,"viewBox=");
   if (start != NULL) {
      next_number(&start,&vxmin);
      next_number(&start,&vymin);
      next_number(&start,&vwidth);
      next_number(&start,&vheight);
      printf("   view x min %f\n",vxmin);
      printf("   view y min %f\n",vymin);
      printf("   view width %f\n",vwidth);
      printf("   view height %f\n",vheight);
      xscale = resolution / vwidth;
      //yscale = resolution * height / (vheight*width);
      yscale = xscale;
      // assume xMidYMid meet scaling
      }
   else {
      xscale = resolution*scale/width;
      yscale = xscale*height/width;
      vxmin = 0;
      vymin = 0;
      }
   //
   // start path
   //
   fab_path_start(v,3);
   v->nx = resolution;
   v->ny = resolution * height/width;
   v->nz = 1;
   v->dx = width;
   v->dy = height;
   v->dz = 0;
   v->xmin = 0;
   v->ymin = 0;
   v->zmin = z;
   //
   // find graphic elements
   //
   ptr = buf;
   do {
      ptr += 1;
      if (strncmp(ptr,"<path",5) == 0) {
         //
         // path
         //
         set_transform(ptr,&a,&b,&c,&d,&e,&f);
         ptr = 4+strstr(ptr," d=");
         current_element = 0;
         x0 = 0;
         y0 = 0;
         do {
            current_element = next_element(&ptr, current_element);
            if (current_element == 'm') {
               //
               // relative moveto
               //
               next_number(&ptr,&x);
               next_number(&ptr,&y);
               x0 = x0 + x;
               y0 = y0 + y;
               //printf("   path m: %f %f\n",x0,y0);
               current_element = 'l';
               fab_path_segment(v);
               fab_path_point(v);
               fab_path_axis(v,xn_(x0,y0,a,c,e,xscale,vxmin));
               fab_path_axis(v,yn_(x0,y0,b,d,f,yscale,vymin));
               fab_path_axis(v,0);
               }
            else if (current_element == 'M') {
               //
               // absolute moveto
               //
               next_number(&ptr,&x0);
               next_number(&ptr,&y0);
               //printf("  path M: %f %f\n",x0,y0);
               current_element = 'L';
               fab_path_segment(v);
               fab_path_point(v);
               fab_path_axis(v,xn_(x0,y0,a,c,e,xscale,vxmin));
               fab_path_axis(v,yn_(x0,y0,b,d,f,yscale,vymin));
               fab_path_axis(v,0);
               }
            else if (current_element == 'l') {
               //
               // relative lineto
               //
               next_number(&ptr,&x);
               next_number(&ptr,&y);
               //printf("   path l: %f %f\n",x,y);
               current_element = 'l';
               fab_path_point(v);
               fab_path_axis(v,xn_(x0+x,y0+y,a,c,e,xscale,vxmin));
               fab_path_axis(v,yn_(x0+x,y0+y,b,d,f,yscale,vymin));
               fab_path_axis(v,0);
               x0 = x0+x;
               y0 = y0+y;
               }
            else if (current_element == 'L') {
               //
               // absolute lineto
               //
               next_number(&ptr,&x);
               next_number(&ptr,&y);
               //printf("   path L: %f %f\n",x,y);
               current_element = 'L';
               fab_path_point(v);
               fab_path_axis(v,xn_(x,y,a,c,e,xscale,vxmin));
               fab_path_axis(v,yn_(x,y,b,d,f,yscale,vymin));
               fab_path_axis(v,0);
               x0 = x;
               y0 = y;
               }
            else if (current_element == 'c') {
               //
               // relative curveto
               //
               next_number(&ptr,&x1);
               x1 += x0;
               next_number(&ptr,&y1);
               y1 += y0;
               next_number(&ptr,&x2);
               x2 += x0;
               next_number(&ptr,&y2);
               y2 += y0;
               next_number(&ptr,&x);
               x += x0;
               next_number(&ptr,&y);
               y += y0;
               //printf("   path c: %f %f %f %f %f %f\n",x1,y1,x2,y2,x,y);
               current_element = 'c';
               cx = 3 * (x1 - x0);
               bx = 3 * (x2 - x1) - cx;
               ax = x - x0 - cx - bx;
               cy = 3 * (y1 - y0);
               by = 3 * (y2 - y1) - cy;
               ay = y - y0 - cy - by;
               for (point = 0; point < points; ++point) {
                  t = point / (points - 1.0);
                  xt = ax*t*t*t + bx*t*t + cx*t + x0;
                  yt = ay*t*t*t + by*t*t + cy*t + y0;
                  fab_path_point(v);
                  fab_path_axis(v,xn_(xt,yt,a,c,e,xscale,vxmin));
                  fab_path_axis(v,yn_(xt,yt,b,d,f,yscale,vymin));
                  fab_path_axis(v,0);
                  }
               x0 = x;
               y0 = y;
               }
            else if (current_element == 'C') {
               //
               // absolute curveto
               //
               next_number(&ptr,&x1);
               next_number(&ptr,&y1);
               next_number(&ptr,&x2);
               next_number(&ptr,&y2);
               next_number(&ptr,&x);
               next_number(&ptr,&y);
               //printf(" path C: %f %f %f %f %f %f\n",x1,y1,x2,y2,x,y);
               current_element = 'C';
               cx = 3 * (x1 - x0);
               bx = 3 * (x2 - x1) - cx;
               ax = x - x0 - cx - bx;
               cy = 3 * (y1 - y0);
               by = 3 * (y2 - y1) - cy;
               ay = y - y0 - cy - by;
               for (point = 0; point < points; ++point) {
                  t = point / (points - 1.0);
                  xt = ax*t*t*t + bx*t*t + cx*t + x0;
                  yt = ay*t*t*t + by*t*t + cy*t + y0;
                  fab_path_point(v);
                  fab_path_axis(v,xn_(xt,yt,a,c,e,xscale,vxmin));
                  fab_path_axis(v,yn_(xt,yt,b,d,f,yscale,vymin));
                  fab_path_axis(v,0);
                  }
               x0 = x;
               y0 = y;
               }
            else if (current_element == 's') {
               //
               // relative smooth curveto
               //
               printf("   svg_path: path s not yet implemented\n");
               current_element = 's';
               }
            else if (current_element == 'S') {
               //
               // absolute smooth curveto
               //
               printf("   svg_path: path S not yet implemented\n");
               current_element = 'S';
               }
            else if (current_element == 'a') {
               //
               // relative arc
               //
               next_number(&ptr,&rx);
               next_number(&ptr,&ry);
               next_number(&ptr,&rotation);
               next_number(&ptr,&large_arc);
               next_number(&ptr,&sweep);
               next_number(&ptr,&x);
               x += x0;
               next_number(&ptr,&y);
               y += y0;
               //printf("   path a: %f %f %f %f %f %f %f\n",rx,ry,rotation,large_arc,sweep,x,y);
               current_element = 'a';
               tdiff = 1-((x-x0)*(x-x0)/(rx*rx) + (y-y0)*(y-y0)/(ry*ry))/2;
               if (tdiff > 1)
                  tdiff = 1;
               if (tdiff < -1)
                  tdiff = -1;
               tdiff = acos(tdiff);
               tsum = (x-x0)/(-2*rx*sin(tdiff/2));
               if (tsum > 1)
                  tsum = 1;
               if (tsum < -1)
                  tsum = -1;
               tsum = 2*asin(tsum);
               t1 = (tsum+tdiff)/2;
               t0 = tsum-t1;
               cx = x0 - rx*cos(t0);
               cy = y0 - ry*sin(t0);
               for (point = 0; point < points; ++point) {
                  t = t0 + (t1-t0) * point / (points - 1.0);
                  xt = cx + rx*cos(t);
                  yt = cy + ry*sin(t);
                  fab_path_point(v);
                  fab_path_axis(v,xn_(xt,yt,a,c,e,xscale,vxmin));
                  fab_path_axis(v,yn_(xt,yt,b,d,f,yscale,vymin));
                  fab_path_axis(v,0);
                  }
               x0 = x;
               y0 = y;
               }
            else if (current_element == 'A') {
               //
               // absolute arc
               //
               printf("   svg_path: path A not yet implemented\n");
               current_element = 'A';
               }
            else if ((current_element == 'z') || (current_element == 'Z')) {
               //
               // closepath
               //
               //printf("   path zZ\n");
               fab_path_point(v);
               fab_path_axis(v,v->path->segment->first->first->value);
               fab_path_axis(v,v->path->segment->first->first->next->value);
               fab_path_axis(v,0);
               current_element = 0;
               ptr += 1;
               }
            } while (*ptr != '\"');
         }
      else if (strncmp(ptr,"<rect",5) == 0) {
         //
         // rectangle
         //
         set_transform(ptr,&a,&b,&c,&d,&e,&f);
         start = strstr(ptr,"width=");
         next_number(&start,&width);
         start = strstr(ptr,"height=");
         next_number(&start,&height);
         start = strstr(ptr,"x=");
         next_number(&start,&x);
         start = strstr(ptr,"y=");
         next_number(&start,&y);
         //printf("   rect: %f %f %f %f\n",width,height,x,y);
         fab_path_segment(v);
            fab_path_point(v);
               fab_path_axis(v,xn_(x,y,a,c,e,xscale,vxmin));
               fab_path_axis(v,yn_(x,y,b,d,f,yscale,vymin));
               fab_path_axis(v,0);
            fab_path_point(v);
               fab_path_axis(v,xn_(x,y+height,a,c,e,xscale,vxmin));
               fab_path_axis(v,yn_(x,y+height,b,d,f,yscale,vymin));
               fab_path_axis(v,0);
            fab_path_point(v);
               fab_path_axis(v,xn_(x+width,y+height,a,c,e,xscale,vxmin));
               fab_path_axis(v,yn_(x+width,y+height,b,d,f,yscale,vymin));
               fab_path_axis(v,0);
            fab_path_point(v);
               fab_path_axis(v,xn_(x+width,y,a,c,e,xscale,vxmin));
               fab_path_axis(v,yn_(x+width,y,b,d,f,yscale,vymin));
               fab_path_axis(v,0);
            fab_path_point(v);
               fab_path_axis(v,xn_(x,y,a,c,e,xscale,vxmin));
               fab_path_axis(v,yn_(x,y,b,d,f,yscale,vymin));
               fab_path_axis(v,0);
         }
      else if (strncmp(ptr,"<circle",7) == 0) {
         //
         // circle 
         //
         set_transform(ptr,&a,&b,&c,&d,&e,&f);
         start = strstr(ptr,"cx=");
         next_number(&start,&cx);
         start = strstr(ptr,"cy=");
         next_number(&start,&cy);
         start = strstr(ptr,"r=");
         next_number(&start,&r);
         //printf("   circle: %f %f %f\n",cx,cy,r);
         fab_path_segment(v);
         for (point = 0; point < points; ++point) {
            fab_path_point(v);
            x = cx + r*cos(point*2*pi/(points-1.0));
            y = cy + r*sin(point*2*pi/(points-1.0));
            fab_path_axis(v,xn_(x,y,a,c,e,xscale,vxmin));
            fab_path_axis(v,yn_(x,y,b,d,f,yscale,vymin));
            fab_path_axis(v,0);
            }
         }
      else if (strncmp(ptr,"<ellipse",8) == 0) {
         //
         // ellipse 
         //
         set_transform(ptr,&a,&b,&c,&d,&e,&f);
         printf("   svg_path: ellipse not yet implemented\n");
         }
      else if (strncmp(ptr,"<line",5) == 0) {
         //
         // line
         //
         set_transform(ptr,&a,&b,&c,&d,&e,&f);
         printf("   svg_path: line not yet implemented\n");
         }
      else if (strncmp(ptr,"<polyline",9) == 0) {
         //
         // polyline
         //
         set_transform(ptr,&a,&b,&c,&d,&e,&f);
         printf("   svg_path: polyline not yet implemented\n");
         }
      else if (strncmp(ptr,"<polygon",8) == 0) {
         //
         // polygon
         //
         set_transform(ptr,&a,&b,&c,&d,&e,&f);
         printf("   svg_path: polygon not yet implemented\n");
         }
      else if (strncmp(ptr,"<text",5) == 0) {
         //
         // text 
         //
         set_transform(ptr,&a,&b,&c,&d,&e,&f);
         printf("   svg_path: text not yet implemented\n");
         }
      } while ((endptr-ptr) > 1);
   }

int main(int argc, char **argv) {
   //
   // local vars
   //
   struct fab_vars v;
   init_vars(&v);
   int points, resolution;
   float z;
   //
   // command line args
   //
   if ((argc != 3) && (argc != 4) && (argc != 5) && (argc != 6)) {
      printf("command line: svg_path in.svg out.path [points [resolution [z]]]\n");
      printf("   in.svg = input binary SVG file\n");
      printf("   out.path = output path file\n");
      printf("   points = points per curve segment (optional, default 25)\n");
      printf("   resolution = path resolution (optional, default 1000)\n");
      printf("   z = path depth (optional, mm, default 0)\n");
      exit(-1);
      }
   if (argc == 3) {
      points = 25;
      resolution = 1000;
      z = 0;
      }
   else if (argc == 4) {
      sscanf(argv[3],"%d",&points);
      resolution = 1000;
      z = 0;
      }
   else if (argc == 5) {
      sscanf(argv[3],"%d",&points);
      sscanf(argv[4],"%d",&resolution);
      z = 0;
      }
   else if (argc == 6) {
      sscanf(argv[3],"%d",&points);
      sscanf(argv[4],"%d",&resolution);
      sscanf(argv[5],"%f",&z);
      }
   //
   //  read SVG
   //
   fab_read_svg(&v,argv[1],points,resolution,z);
   //
   // write path
   //
   fab_write_path(&v,argv[2]);
   //
   // return
   //
   return(0);
   }

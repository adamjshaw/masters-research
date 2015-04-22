#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define cine_depth 452
#define x_size 384
#define frame_width 384
#define frame_length 384
#define display_frame_start 8
#define display_frame_end 393
#define bottom_clip 80
#define ul_top 4000
#define ul_gamma 2.0
#define scale 0.584

#define W 18
#define z_sign 1
#define front_top 15.8/2.54
#define front_bottom 36.6/2.54
#define back_top 22.3/2.54
#define back_bottom 49.6/2.54

#define f 55.0
#define pix_size 28*pow(10,-3)

double transform(double x) {
    return (x * x_size / 2) + (x_size / 2);
}

double x_func(double x, double y, double z, double x_x, double x_y, double x_z, double x_xy, double x_xz) {
    return transform(x_x*x + x_y*y + x_z*z + x_xy*x*y + x_xz*x*z);
}

double y_func(double x, double y, double z, double y_y, double y_x, double y_z, double y_xy, double y_yz) {
    return transform(y_x*x + y_y*y + y_z*z + y_xy*x*y + y_yz*y*z);
}

double z_func(double x, double y, double z, double z_z, double z_x, double z_y, double z_xz, double z_yz) {
    return transform(z_z*z + z_y*y + z_x*x + z_yz*y*z + z_xz*x*z);
}


int main(int argc, char **argv) {
    double a = x_size * scale / 2;
    double a_in = a / 25.4;
    double h1 = back_top - front_top;
    double h2 = back_bottom - front_bottom;
    double theta_1 = atan(h1 / W);
    double theta_2 = atan(h2 / W);
    
    
    double L = ((pix_size + scale) / (pix_size) * f) / a;
    
    double mt = h1 / W;
    double mb = h2 / W;
    
    double x_x  = 1;
    double x_y  = 0;
    double x_z  = 0;
    double x_xy = 0;
    double x_xz = -1 / L;
    double y_y  = 1;
    double y_x  = 0;
    double y_z  = 0 ;
    double y_xy = 0;
    double y_yz = -1 / L;
    double z_z  = 1;
    double z_y  = -1./2 * (mt + mb);
    double z_x  = 0;
    double z_yz = 1./2 * (mb - mt);
    double z_xz = 0;
    //double x = -0.5381066879274397;
    //double y = 0.0015416539228692017;
    //double z = 0.8173732705677059;
    /*if (argc > 1) {
        x = (atof(argv[1]) - x_size/2)/(x_size/2);
        y = (atof(argv[2]) - x_size/2)/(x_size/2);
        z = (atof(argv[3]) - x_size/2)/(x_size/2);
    }*/
    char buf[256];
    while (fgets (buf, sizeof(buf), stdin)) {
        double x,y,z;
        int zero;
        strtok(buf, "\n"); 
        //printf("%s\n", buf);
        sscanf(buf, "%lf %lf %lf %d", &x, &y, &z, &zero);           
        //printf("%lf %lf %lf\n", x, y, z);
        x = (x - x_size/2)/(x_size/2);
        y = (y - x_size/2)/(x_size/2);
        z = (z - x_size/2)/(x_size/2);
        printf("%lf %lf %lf\n", x_func(x, y, z, x_x, x_y, x_z, x_xy, x_xz), y_func(x, y, z, y_y, y_x, y_z, y_xy, y_yz), z_func(x, y, z, z_z, z_x, z_y, z_xz, z_yz) );
    }
}

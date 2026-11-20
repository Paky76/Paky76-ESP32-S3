// Studio volumetrico Rev.B; usare show_shell=false per vedere i sottosistemi.
show_shell=true;
$fn=36;
module softbox(size,r) {
  minkowski() {
    cube([for(v=size) v-2*r],center=true);
    sphere(r);
  }
}
module head() {
  difference() {
    translate([0,0,64]) softbox([66,48,58],15);
    translate([0,0,64]) softbox([60,42,52],12);
    translate([0,-25,64]) softbox([26,18,26],2.2);
  }
}
module torso() {
  difference() {
    translate([0,0,24]) softbox([78,60,48],12);
    translate([0,0,24]) softbox([72,54,42],9);
    for(x=[-10:5:10],z=[15:5:30])
      if(x*x+(z-22.5)*(z-22.5)<150)
        translate([x,-29,z]) rotate([90,0,0]) cylinder(d=2.3,h=12,center=true);
    translate([0,29,10]) softbox([15,10,7],1.8);
    translate([20,29,10]) softbox([15,10,7],1.8);
    translate([-22,29,17]) softbox([13,10,3.4],1.1);
  }
}
if(show_shell) {
  color("#eeebdb",0.58) { head(); torso(); }
  for(x=[-24,24]) color("#167f78") translate([x,-9,4]) softbox([24,42,8],3.5);
}
// Scheda, modulo display, membrana speaker, modem e zona antenna.
color("#287a58") translate([0,0,8]) cube([58,42,1.6],center=true);
color("#101d28") translate([0,-13,64]) cube([31,4,45],center=true);
color("#101d28") translate([0,-19,64]) softbox([24,9,24],1.4);
color("#79efdb") {
  for(x=[-5,5]) translate([x,-24,67]) softbox([4,1.5,4],0.6);
  translate([0,-24,60]) softbox([8,1.5,2],0.6);
}
color("#103f45") translate([0,-23,22]) rotate([90,0,0]) cylinder(d=28,h=8,center=true);
color("#c1cbd0") translate([17,7,13]) cube([23.6,19.9,2.4],center=true);
color("#dba858") translate([36,6,30]) cube([1.2,31,13],center=true);

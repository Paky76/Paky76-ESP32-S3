// Paky76 revisione meccanica D1 — printable enclosure around 66 x 42 mm placement PCB.
// All dimensions in mm. Front is -Y, upright is +Z.
part="assembly"; // [assembly,front,chassis,display_clip,control_carrier]
$fn=48;
back=30;
front=-27;
wall=2.8;
panel=3;
gap=.35;
display_z=68;
display_w=31;
display_h=45;
speaker_z=27;
key_pitch=8;
key_z=38;
key_x=23;
key_hole=5.4;
cam_x=23;
cam_z=86;
cam_hole=8;
mic_x=-19;
mic_z=71;
led_x=19;
led_z=71;
sd_x=-24;
sd_z=29;
power_x=22;
power_z=23;

pcb_y=-2.5;
pcb_z=9;
usb_x=13;
usb_z=pcb_z+3.15;
screw_sites=[[-37,9],[37,9],[-29,45],[29,45]];

module rounded(w,h,r) { offset(r=r) square([w-2*r,h-2*r],center=true); }
module silhouette() {
  hull() {
    translate([0,23]) rounded(82,46,10);
    translate([0,36]) rounded(70,20,8);
  }
  translate([0,66]) rounded(68,58,15);
}
module section(y,depth) {
  translate([0,y,0]) rotate([90,0,0]) linear_extrude(height=depth) children();
}
module through(x,z,y,depth,diameter) {
  section(y,depth) translate([x,z]) circle(d=diameter);
}
module key_sites() {
  for (p=[[0,0],[-1,0],[1,0],[0,-1],[0,1]])
    translate([key_x+p[0]*key_pitch,key_z+p[1]*key_pitch]) children();
}
module face() {
  difference() {
    union() {
      section(front+panel,panel) silhouette();
      // Narrow guides register the display mounting envelope. Tape secures
      // the measured module to these guides without relying on hole spacing.
      for (s=[-1,1])
        translate([s*(display_w/2+.8)-.65,front+panel-.1,display_z-18])
          cube([1.3,3.2,36]);
      for (s=[-1,1])
        translate([-10,front+panel-.1,display_z+s*(display_h/2+.5)-.65])
          cube([20,3.2,1.3]);
      for (x=[-21,21], z=[display_z-13,display_z+13])
        through(x,z,front+panel+5.2,5.3,5.6);
      // Slots in rearward tabs accept a narrow strap over the speaker frame.
      for (x=[-17,17])
        translate([x-2.4,front+panel-.10,speaker_z-5])
          cube([4.8,9.1,10]);
      // Front rim behind the loudspeaker, sized for a nominal 28 mm frame.
      difference() {
        through(0,speaker_z,front+panel+2.2,2.35,31.4);
        through(0,speaker_z,front+panel+2.3,2.55,28.7);
      }
    }
    section(front+panel+.2,panel+.5) translate([0,display_z]) rounded(24.8,24.8,1.4);
    section(front+.65,.9) translate([0,display_z]) rounded(26.2,26.2,1.8);
    for (x=[-9:4.5:9], z=[-9:4.5:9])
      if(x*x+z*z<=125) through(x,speaker_z+z,front+panel+.1,panel+.3,2.5);
    section(front+panel+.2,panel+.5) translate([usb_x,usb_z]) rounded(16,9,1.8);
    for (x=[-21,21], z=[display_z-13,display_z+13])
      through(x,z,front+panel+5.35,4.2,1.65);
    for (x=[-17,17])
      translate([x-2.6,front+panel+4,speaker_z-2])
        cube([5.2,2.1,4]);
    section(front+panel+.2,panel+.5) key_sites() circle(d=key_hole);
    through(cam_x,cam_z,front+panel+.2,panel+.5,cam_hole);
    through(mic_x,mic_z,front+panel+.2,panel+.5,2.3);
    through(led_x,led_z,front+panel+.2,panel+.5,3.2);
    for (s=screw_sites) through(s[0],s[1],front+panel+.2,panel+.5,3.2);
  }
}
module pcb_support() {
  // Shelf on PCB long edges. The PCB is inserted horizontally from front.
  for (side=[-1,1]) {
    translate([side*33-1.3,pcb_y-21.1,pcb_z-2.6]) cube([2.6,41.9,2.6]);
    translate([side*(33+gap+.55)-.55,pcb_y-21.1,pcb_z-2.6])
      cube([1.1,41.9,4.8]);
  }
  for(x=[-30,30])
    translate([x-2,pcb_y+21+.35,1]) cube([4,2.1,pcb_z+1.2]);
  // Ribs from the floor to the shelves, outside the PCB's populated region.
  for (x=[-33,33],y=[-17,-3,13])
    translate([x-1.3,y-2.5,1]) cube([2.6,5,pcb_z-3.4]);
}
module chassis() {
  difference() {
    union() {
      difference() {
        section(back,back-front-panel) silhouette();
        section(back-wall,back-wall-front-panel+.15) offset(delta=-wall) silhouette();
      }
      pcb_support();
      for (s=screw_sites) {
        through(s[0],s[1],front+panel+10,10.1,7.2);
        // Connect the screw bosses to the case wall.
        section(front+panel+10,10) intersection() {
          silhouette();
          hull() {
            translate(s) circle(d=5.8);
            translate([s[0]<0?-44:44,s[1]]) circle(d=3.2);
          }
        }
      }
    }
    for (s=screw_sites) through(s[0],s[1],front+panel+8.5,8.8,2.5);
    // Clearance holes sized as starting points for measured external modules.
    section(back+.2,wall+.55) translate([sd_x,sd_z]) rounded(17,5.5,.9);
    section(back+.2,wall+.55) translate([power_x,power_z]) rounded(13,8,1);
    // Exit for an external LTE evaluation board harness.
    section(back+.2,wall+.55) translate([-21,18]) rounded(13,6,1.1);
    for (x=[-19:5:19])
      section(back+.2,wall+.5) translate([x,42]) rounded(2.7,10,1.2);
  }
}
module display_clip() {
  difference() {
    linear_extrude(height=2.2) rounded(13,7,1.4);
    translate([-2.7,0,-.05]) cylinder(h=2.3,d=2.2);
  }
}
module control_carrier() {
  difference() {
    linear_extrude(height=2.2) rounded(30,27,2);
    for (p=[[0,0],[-1,0],[1,0],[0,-1],[0,1]])
      translate([p[0]*key_pitch,p[1]*key_pitch,-.1]) cylinder(h=2.4,d=6.3);
    for (x=[-12,12]) translate([x,0,-.1]) cylinder(h=2.4,d=2.2);
  }
}
if(part=="control_carrier") control_carrier();
else if(part=="display_clip") display_clip();
else if(part=="front") translate([0,0,-front]) rotate([90,0,0]) face();
else if(part=="chassis") translate([0,0,back]) rotate([-90,0,0]) chassis();
else { color("#cedfd6") chassis(); color("#3b5f66") face(); }

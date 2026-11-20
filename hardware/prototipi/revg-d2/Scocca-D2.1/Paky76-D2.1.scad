// Paky76 revisione meccanica D2.1 — printable enclosure around 83.25 x 42 mm placement PCB.
// All dimensions in mm. Front is -Y, upright is +Z.
part="assembly"; // [assembly,front,chassis,key_arrow,key_ok]
$fn=48;
back=30;
front=-27;
wall=2.8;
panel=3;
gap=.35;
display_z=75;
// Waveshare 15867 PCB rotated into portrait, holes 26 x 40 apart.
display_mount_dx=13;
display_mount_dz=20;
display_standoff=3;
speaker_z=27;
speaker_x=-13;
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
led_z=76;
// PCB (KiCad x,y) -> case (x,y) = (x-125,121.5-y).
sd_y=5.925;  // Middle of J9 card mouth projected onto right wall
sd_z=7.5;    // Card/actuator access below the PCB seating plane
antenna_tip_y=24.5;
assert(back-wall-antenna_tip_y>=2.5);
key_switch_height=1.50; // C115351 (ALPS SKQGABE010)
key_boss_height=3.7;
key_flange=.8;
key_rest_gap=.35;
key_nose=key_boss_height-key_switch_height-key_flange-key_rest_gap;
power_x=31;
power_z=26;

pcb_y=-2.5;
pcb_z=9;
usb_x=13;
usb_z=pcb_z+1.8;
screw_sites=[[-35,9],[54,9],[-28,45],[47,44]];
key_mount=[[key_x-14,key_z+2],[key_x+14,key_z+2]];

module rounded(w,h,r) { offset(r=r) square([w-2*r,h-2*r],center=true); }
module silhouette() {
  hull() {
    translate([8.625,26]) rounded(101,52,10);
    translate([8.625,40]) rounded(95,22,8);
  }
  translate([0,71]) rounded(72,66,15);
}
module section(y,depth) {
  translate([0,y,0]) rotate([90,0,0]) linear_extrude(height=depth) children();
}
module through(x,z,y,depth,diameter) {
  section(y,depth) translate([x,z]) circle(d=diameter);
}
module indexed_key(d,flat) {
  intersection() {
    circle(d=d);
    translate([-d,-d]) square([d+flat,2*d]);
  }
}
module key_sites() {
  // Flat follows the arrow; +Z is up on the finished front.
  for (p=[[0,0,0],[-1,0,90],[1,0,-90],[0,-1,180],[0,1,0]])
    translate([key_x+p[0]*key_pitch,key_z+p[1]*key_pitch])
      rotate(p[2]) indexed_key(key_hole,1.99);
}
module face() {
  difference() {
    union() {
      section(front+panel,panel) silhouette();
      for (m=key_mount) through(m[0],m[1],front+panel+key_boss_height,key_boss_height+.1,5.2);
      for (x=[-display_mount_dx,display_mount_dx], z=[display_z-display_mount_dz,display_z+display_mount_dz])
        through(x,z,front+panel+display_standoff,display_standoff+.12,4.7);
      // Slots in rearward tabs accept a narrow strap over the speaker frame.
      for (x=[speaker_x-17,speaker_x+17])
        translate([x-2.4,front+panel-.10,speaker_z-5])
          cube([4.8,9.1,10]);
      // Front rim behind the loudspeaker, sized for a nominal 28 mm frame.
      difference() {
        through(speaker_x,speaker_z,front+panel+2.2,2.35,31.4);
        through(speaker_x,speaker_z,front+panel+2.3,2.55,28.7);
      }
    }
    section(front+panel+.2,panel+.5) translate([0,display_z]) rounded(24.8,24.8,1.35);
    hull() {
      section(front-.05,.15) translate([0,display_z]) rounded(28.2,28.2,2.3);
      section(front+1.45,.12) translate([0,display_z]) rounded(24.8,24.8,1.35);
    }
    for (x=[-9:4.5:9], z=[-9:4.5:9])
      if(x*x+z*z<=125) through(speaker_x+x,speaker_z+z,front+panel+.1,panel+.3,2.5);
    section(front+panel+.2,panel+.5) translate([usb_x,usb_z]) rounded(16,9,1.8);
    for (x=[-display_mount_dx,display_mount_dx], z=[display_z-display_mount_dz,display_z+display_mount_dz])
      through(x,z,front+panel+display_standoff+.1,display_standoff-.35,1.65);
    for (x=[speaker_x-17,speaker_x+17])
      translate([x-2.6,front+panel+4,speaker_z-2])
        cube([5.2,2.1,4]);
    section(front+panel+.2,panel+.5) key_sites();
    through(cam_x,cam_z,front+panel+.2,panel+.5,cam_hole);
    through(mic_x,mic_z,front+panel+.2,panel+.5,2.3);
    through(led_x,led_z,front+panel+.2,panel+.5,5.25);
    for (m=key_mount) through(m[0],m[1],front+panel+3.8,3.4,1.65);
    for (s=screw_sites) through(s[0],s[1],front+panel+.2,panel+.5,3.2);
  }
}
module pcb_support() {
  // Shelf on PCB long edges. The PCB is inserted horizontally from front.
  for (sx=[-33,50.25]) {
    translate([sx-1.3,pcb_y-21.1,pcb_z-2.6]) cube([2.6,41.9,2.6]);
    translate([sx+(sx<0?-1:1)*(gap+.55)-.55,pcb_y-21.1,pcb_z-2.6])
      cube([1.1,41.9,4.8]);
  }
  for(x=[-30,47.25])
    translate([x-2,pcb_y+21+.35,1]) cube([4,2.1,pcb_z+1.2]);
  // Ribs from the floor to the shelves, outside the PCB's populated region.
  for (x=[-33,50.25],y=[-17,-3,13])
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
            translate([s[0]<0?-46:67,s[1]]) circle(d=3.2);
          }
        }
      }
    }
    for (s=screw_sites) through(s[0],s[1],front+panel+8.5,8.8,2.5);
    // Clearance holes sized as starting points for measured external modules.
    // Continuous passage from the socket to the side, plus a finger recess.
    translate([48.4,sd_y-7.5,sd_z-2.1]) cube([15,15,4.2]);
    translate([55.4,sd_y,sd_z]) rotate([0,90,0])
      linear_extrude(height=9) rounded(7.2,19,2.3);
    through(power_x,power_z,back+.15,wall+.4,6.65);
    // Exit for an external LTE evaluation board harness.
    section(back+.2,wall+.55) translate([-21,18]) rounded(13,6,1.1);
    for (x=[-19:5:19])
      section(back+.2,wall+.5) translate([x,42]) rounded(2.7,10,1.2);
  }
}
module key_cap(ok=false) {
  difference() {
    union() {
      cylinder(h=key_nose+.12,d=2.5);
      translate([0,0,key_nose]) cylinder(h=key_flange,d=6.4);
      translate([0,0,key_nose+key_flange-.05])
        linear_extrude(height=4.15) indexed_key(5.05,1.8);
    }
    translate([0,0,key_nose+key_flange+3.68]) linear_extrude(height=.6) {
      if(ok) difference() {circle(d=2.9); circle(d=1.65);}
      else polygon([[-1.45,-.7],[0,1.3],[1.45,-.7],[.51,-.7],
                    [.51,-1.38],[-.51,-1.38],[-.51,-.7]]);
    }
  }
}
if(part=="key_arrow") key_cap();
else if(part=="key_ok") key_cap(true);
else if(part=="front") translate([0,0,-front]) rotate([90,0,0]) face();
else if(part=="chassis") translate([0,0,back]) rotate([-90,0,0]) chassis();
else { color("#cedfd6") chassis(); color("#3b5f66") face(); }

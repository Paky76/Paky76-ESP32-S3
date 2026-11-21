// Quote in mm. Prova di ingombro Paky76 Mini A4.
part = "assembly"; // [assembly,tray,bezel,main_gauge,front_gauge,cell_gauge,switch_gauge]
$fn = 40;
body = [48, 47];
wall = 2;
tray_h = 22;
front_h = 8;
main = [32, 39];
front = [43, 42];
cell = [37, 21, 6];
// MFS201N-Z, vista esterna lato sinistro: asola 9,5 x 5; fori Ø2,5 a 19.
switch_y = 0;
switch_z = 9.8;
switch_slot = [9.5,5];
switch_pitch = 19;
switch_hole = 2.5;
main_holes = [[-12,-15],[12,-15],[-12,15],[12,15]];
front_holes = [[-19,-18],[19,-18],[-19,18],[19,18]];

module rounded(w, h, r, z) {
    linear_extrude(z)
        offset(r=r)
            square([w-2*r,h-2*r],center=true);
}
module block(w,h,z) {
    translate([-w/2,-h/2,0]) cube([w,h,z]);
}
module holes(points, z, d) {
    for (p=points) translate([p.x,p.y,-0.1]) cylinder(h=z+0.2,d=d);
}
module pcb_gauge(size, points) {
    difference() {
        block(size.x,size.y,1.6);
        holes(points,1.6,2.2);
    }
}
module tray() {
    difference() {
        union() {
            difference() {
                rounded(body.x,body.y,4,tray_h);
                translate([0,0,wall]) rounded(body.x-2*wall,body.y-2*wall,2,tray_h);
            }
            hull() {
                translate([0,22.5,0]) cylinder(d=6,h=4);
                translate([0,27,0]) cylinder(d=8,h=4);
            }
            for (p=main_holes)
                translate([p.x,p.y,1.8]) cylinder(h=2,d=5);
            for (p=front_holes)
                translate([p.x,p.y,1.8]) cylinder(h=tray_h-1.8,d=4.5);
        }
        translate([0,27,-0.1]) cylinder(d=4,h=4.2);
        translate([0,0,2]) holes(main_holes,2,1.65);
        translate([0,0,tray_h-4]) holes(front_holes,5,1.65);
        translate([-body.x/2-0.1,switch_y-switch_slot.x/2,switch_z-switch_slot.y/2])
            cube([wall+0.2,switch_slot.x,switch_slot.y]);
        for (dy=[-switch_pitch/2,switch_pitch/2])
            translate([-body.x/2-0.1,switch_y+dy,switch_z])
                rotate([0,90,0]) cylinder(d=switch_hole,h=wall+0.2);
        // Apertura USB-C da adattare al footprint e al cavo effettivi.
        translate([-7,-body.y/2-0.1,4.7]) cube([14,6.5,6.8]);
    }
}
module bezel() {
    difference() {
        rounded(body.x,body.y,4,front_h);
        translate([0,0,-0.1]) rounded(44,43,2,6.2);
        translate([0,1,-0.1]) rounded(31,16,1,front_h+0.2);
        holes(front_holes,front_h,2.2);
        for (x=[-body.x/2,body.x/2])
            translate([x,0,2]) rotate([0,90,0]) cylinder(d=3.4,h=8,center=true);
    }
}
module assembly() {
    color("DimGray") tray();
    color("DarkGreen") translate([0,0,3.8]) pcb_gauge(main,main_holes);
    color("Gold") translate([0,9,14.2]) block(cell.x,cell.y,cell.z);
    color("SlateGray") translate([0,-8.55,5.4]) block(17.8,21,2.5);
    // Volumi di riferimento, incluso spazio per terminali isolati.
    color("Gray") translate([-body.x/2-0.5,switch_y-11.6,switch_z-3.6])
        cube([0.5,23.2,7.2]);
    color("DarkSlateGray") translate([-body.x/2+wall,switch_y-7.75,switch_z-3.6])
        cube([10,15.5,7.2]);
    color("Teal") translate([0,0,tray_h]) pcb_gauge(front,front_holes);
    color("LightGray") translate([0,0,tray_h]) bezel();
}
if (part == "assembly") assembly();
if (part == "tray") tray();
if (part == "bezel") bezel();
if (part == "main_gauge") pcb_gauge(main,main_holes);
if (part == "front_gauge") pcb_gauge(front,front_holes);
if (part == "cell_gauge") block(cell.x,cell.y,cell.z);

if (part == "switch_gauge") {
    difference() {
        block(26, 10, wall);
        translate([-switch_slot.x/2, -switch_slot.y/2, -0.1])
            cube([switch_slot.x, switch_slot.y, wall+0.2]);
        holes([[-switch_pitch/2,0],[switch_pitch/2,0]],wall,switch_hole);
    }
}

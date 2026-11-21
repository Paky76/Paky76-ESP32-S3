// Quote in mm. Prova di ingombro Paky76 Mini A5, OLED SH1107 da 1,5 pollici.
part = "assembly"; // [assembly,tray,bezel,button,oled_gauge,fit_check]
$fn = 40;
body = [49, 54];
wall = 2;
tray_h = 23.6;
front_seat_z = tray_h - 1.6;
front_h = 18;
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
                translate([0,body.y/2-1,0]) cylinder(d=6,h=4);
                translate([0,body.y/2+3.5,0]) cylinder(d=8,h=4);
            }
            // Ripiano posteriore: usare una fascetta morbida rimovibile.
            translate([-20,0,12.6]) cube([40,26,1.6]);
            for (p=main_holes)
                translate([p.x,p.y,1.8]) cylinder(h=2,d=5);
            for (p=front_holes)
                translate([p.x,p.y,1.8]) cylinder(h=front_seat_z-1.8,d=4.5);
        }
        translate([0,body.y/2+3.5,-0.1]) cylinder(d=4,h=4.2);
        translate([0,0,2]) holes(main_holes,1.8,1.65);
        translate([0,0,front_seat_z-4]) holes(front_holes,4.2,1.65);
        translate([-body.x/2-0.1,switch_y-switch_slot.x/2,switch_z-switch_slot.y/2])
            cube([wall+0.2,switch_slot.x,switch_slot.y]);
        for (dy=[-switch_pitch/2,switch_pitch/2])
            translate([-body.x/2-0.1,switch_y+dy,switch_z])
                rotate([0,90,0]) cylinder(d=switch_hole,h=wall+0.2);
        for (x=[-12,12]) translate([x-2,5,12.5]) cube([4,12,1.8]);
        // Apertura USB-C da adattare al footprint e al cavo effettivi.
        translate([-7,-body.y/2-0.1,4.7]) cube([14,8.8,6.8]);
    }
}
// OLED: PCB 34 x 47, fori nominali 29 x 42, lato connettore verso USB.
oled_mounts = [[-14.5,-21],[14.5,-21],[-14.5,21],[14.5,21]];
oled_window_y = -3;
oled_window = 30.4;
roof = 2;
oled_face_to_pcb = 2.1;
oled_post_h = 2.7;
oled_pcb_z = front_h-roof-oled_post_h;
button_z = 2.5;
button_length = 2.65;
button_tip = 1.7;

module button_axis(side) {
    translate([side*body.x/2,0,button_z])
        rotate([0,side*90,0]) children();
}

module bezel() {
    difference() {
        union() {
            difference() {
                rounded(body.x,body.y,4,front_h);
                translate([0,0,-0.1])
                    rounded(body.x-2*wall,body.y-2*wall,2,front_h-roof+0.1);
            }
            for (p=front_holes)
                translate([p.x,p.y,0]) cylinder(d=3.8,h=front_h);
            for (p=oled_mounts)
                translate([p.x,p.y,oled_pcb_z]) cylinder(d=3.8,h=oled_post_h+0.25);
        }
        translate([0,oled_window_y,front_h-roof-0.1])
            rounded(oled_window,oled_window,0.8,roof+0.2);
        holes(front_holes,front_h,2.25);
        for (p=front_holes)
            translate([p.x,p.y,front_h-2.3]) cylinder(d=4.2,h=2.4);
        translate([0,0,oled_pcb_z-0.1]) holes(oled_mounts,oled_post_h,1.65);
        for (side=[-1,1]) button_axis(side)
            translate([0,0,-wall-0.1]) cylinder(d=3.35,h=wall+0.2);
    }
}

module button() {
    union() {
        cylinder(d=4.1,h=0.65);
        translate([0,0,0.6]) cylinder(d=3.0,h=button_length+button_tip-0.6);
    }
}

module oled_gauge() {
    scale([1,1,0.75]) pcb_gauge([34,47],oled_mounts);
}

module assembly() {
    color("SlateGray") tray();
    color("SeaGreen") translate([0,0,3.8]) pcb_gauge(main,main_holes);
    color("Gold") translate([0,10.8,14.2]) block(cell.x,cell.y,cell.z);
    color("CadetBlue") translate([0,0,front_seat_z]) pcb_gauge(front,front_holes);
    translate([0,0,tray_h]) {
        color("RoyalBlue") translate([0,0,oled_pcb_z-1.2]) oled_gauge();
        color("Black") translate([0,oled_window_y,oled_pcb_z]) block(33.9,37.3,oled_face_to_pcb);
        color("LightGray",0.65) bezel();
        for (side=[-1,1]) color("Orange") button_axis(side)
            translate([0,0,-button_length]) button();
    }
}

// Provino con asola per verificare scorrimento del copritasto e tolleranze.
module fit_check() {
    difference() {
        block(12,12,wall);
        translate([0,0,-0.1]) cylinder(d=3.35,h=wall+0.2);
    }
}

if (part=="assembly") assembly();
if (part=="tray") tray();
if (part=="bezel") bezel();
if (part=="button") button();
if (part=="oled_gauge") oled_gauge();
if (part=="fit_check") fit_check();

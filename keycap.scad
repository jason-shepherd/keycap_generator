module create_keycap(height=10, stem_height=6, wall_thickness=3, u_width=1, u_height=1) {
    //keycap shell
    difference() {
        cube([18*u_width, 18*u_height, height], center = true);
        translate([0, 0, -wall_thickness/2])
        cube([18*u_width-wall_thickness, 18*u_height-wall_thickness, height-wall_thickness], center = true);
    }
    
    //cherrymx stem
    translate([0, 0, -height/2])
    linear_extrude(height=stem_height)
        difference() {
            circle(d=5.5, $fn=100, center=true);
            square([1.35, 4.02], center=true);
            square([4.02, 1.35], center=true);
        }
}

module create_legends(legends=["w"]) {
    for(i=[0:len(legends)-1]) {
        if(i < 2) {
            translate([-6, 6 + (-12 * i), 4])
            linear_extrude(height=1)
            text(legends[i], size=4, halign="center", valign="center");
        } else if(i < 4) {
            translate([6, 6 + (-12 * (i-2)), 4])
            linear_extrude(height=1)
            text(legends[i], size=4, halign="center", valign="center");
        }
    }
}

create_keycap();

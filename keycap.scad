module create_keycap(height=10, stem_height=6, wall_thickness=3) {
    //keycap shell
    difference() {
        cube([18, 18, height], center = true);
        cube([18-wall_thickness, 18-wall_thickness, height-wall_thickness], center = true);
    }
    
    //cherrymx stem
    linear_extrude(height=stem_height)
        difference() {
            circle(d=5.5, $fn=100, center=true);
            square([1.35, 4.02], center=true);
            square([4.02, 1.35], center=true);
        }
}

create_keycap();

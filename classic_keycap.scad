module create_keycap(height=10, stem_height=6, wall_thickness=3) {
    //keycap shell
    difference() {
        linear_extrude(height = height, scale = 12.6/18)
            square([18, 18], center = true);
        linear_extrude(height = stem_height, scale = 12.6/18)
            square([18-wall_thickness, 18-wall_thickness], center = true);
    }
    
    //cherrymx stem
    linear_extrude(height=stem_height)
        difference() {
            circle(d=5.5, $fn=100, center=true);
            square([1.34, 4.02], center=true);
            square([4.02, 1.34], center=true);
        }
}

create_keycap();

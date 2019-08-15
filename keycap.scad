module create_keycap(key_width=18, height=10, stem_height=6, wall_thickness=3, u_width=1, u_height=1, legends=["W"]) {
    //keycap shell
    difference() {
        cube([key_width*u_width, key_width*u_height, height], center = true);
        translate([0, 0, -wall_thickness/2])
        cube([key_width*u_width-wall_thickness, key_width*u_height-wall_thickness, height-wall_thickness], center = true);
        create_legends(legends=legends, u_width=u_width, u_height=u_height, key_width=key_width);
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

module create_legends(legends=["w", "a", "s", "d"], key_width=18, key_height=10, u_width=1, u_height=1) {
    for(i=[0:len(legends)-1]) {
        xpos = key_width/2 * u_width - 1.5;
        ypos = key_width/2 * u_height - 3.5;
        if(i < 2) {
            translate([-xpos, ypos + (-ypos * 2 * i), key_height/2-1])
            linear_extrude(height=1)
                text(legends[i], size=4, halign="left", valign="center");
        } else if(i < 4) {
            translate([xpos, ypos + (-ypos* 2 * (i-2)), key_height/2-1])
            linear_extrude(height=1)
            text(legends[i], size=4, halign="right", valign="center");
        }
    }
}

//create_keycap(legends=["W", "A", "S", "D"]);
//create_legends(u_width=2);

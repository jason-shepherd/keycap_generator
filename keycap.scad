module create_keycap(bottom=18, top=12.6, key_height=10, u_width=1, u_height=1, legends=["W"]) {
    union() {
        difference() {
            hull() {
                cube([bottom*u_width, bottom*u_height, 0.0001],  center=true);
                translate([0, 0, key_height])
                    cube([bottom*u_width-(bottom-top), bottom*u_height-(bottom-top), 0.0001], center=true);
            }
            hull() {
                cube([bottom*u_width-3, bottom*u_height-3, 0.0001],  center=true);
                translate([0, 0, 6])
                    cube([bottom*u_width-(bottom-top)-3, bottom*u_height-(bottom-top)-3, 0.0001], center=true);
            }
            create_legends(legends=legends, u_width=u_width, u_height=u_height, key_width=top);
        }
        //create_legends(legends);
        create_stem(stem_height=10);
        if(u_width >= 2) {
            translate([bottom*floor(u_width)/2-bottom/2+6.6/2, 0, 0])
            create_stem();
            translate([-(bottom*floor(u_width)/2-bottom/2+6.6/2), 0, 0])
            create_stem();
        }
        if(u_height >= 2) {
            translate([0, bottom*floor(u_height)/2-bottom/2, 0])
            create_stem();
            translate([0, -(bottom*floor(u_height)/2-bottom/2), 0])
            create_stem();
        }
    }
}

module create_stem(stem_height=10) {
    translate([0, 0, 0])
    linear_extrude(height=stem_height)
        difference() {
            circle(d=5.5, $fn=100, center=true);
            square([1.35, 4.02], center=true);
            square([4.02, 1.35], center=true);
        }
}

module create_legends(legends=["w"], bottom=18, top=12.6, key_height=10, u_width=1, u_height=1) {
    for(i=[0:len(legends)-1]) {
        xpos = (bottom*u_width-(bottom-top))/2 - 1.5;
        ypos = (bottom*u_height-(bottom-top))/2 - 3.5;
        if(i < 2) {
            translate([-xpos, ypos + (-ypos * 2 * i), key_height-1])
            linear_extrude(height=1)
                text(legends[i], size=4, halign="left", valign="center");
        } else if(i < 4) {
            translate([xpos, ypos + (-ypos* 2 * (i-2)), key_height-1])
            linear_extrude(height=1)
            text(legends[i], size=4, halign="right", valign="center");
        }
    }
}

//rotate([0, 180, 0])
//create_keycap(u_width=1, legends=["w", "a", "s", "d"]);
//create_stem();
//create_legends(u_width=2);
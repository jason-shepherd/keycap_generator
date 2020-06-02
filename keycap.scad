module create_keycap(bottom=18, top=12.6, key_height=10, u_width=1, u_height=1, homing=false, font_size=3, legends=["W"]) {
    difference() {
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
                
            }

            if(homing) {
              translate([0, -top/2+1, key_height])
              rotate([90, 0, 90])
              cylinder(h=2.5, r=0.1, center=true);
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
        create_legends(legends=legends, size=font_size, u_width=u_width, u_height=u_height, top=top, bottom=bottom);
    }
}

module create_stem(stem_height=10) {
    translate([0, 0, 0])
    linear_extrude(height=stem_height)
        difference() {
            circle(d=5.5, $fn=100);
            square([1.35, 4.02], center=true);
            square([4.02, 1.35], center=true);
        }
}

module create_legends(legends=["w"], size=3, bottom=18, top=12.6, key_height=10, u_width=1, u_height=1) {
    for(i=[0:len(legends)-1]) {
        xpos = (bottom*u_width-(bottom-top))/2 - 1.5;
        ypos = (bottom*u_height-(bottom-top))/2 - 3.5;
        string = len(legends[i])*4 > bottom*u_width-(bottom-top) ? split_string(legends[i]) : legends[i];
        if(i < 2) {
            translate([-xpos, ypos + (-ypos * 2 * i), key_height-1+.0001])
            linear_extrude(height=1)
                better_text(string, size=size, halign="left", valign="center");
        } else if(i < 4) {
            translate([xpos, ypos + (-ypos* 2 * (i-2)), key_height-1+.0001])
            linear_extrude(height=1)
                better_text(string, size=size, halign="right", valign="center");
        }
    }
}

function string_array(string, split_char, skip=0, i=0) = (
    skip < 0 ?
        ""
    :i == len(string) - 1 ?
        string[i]
    :string[i] == split_char ?
        string_array(string, split_char, skip-1, i+1)
    :
        str(skip == 0 ? string[i] : "", string_array(string, split_char, skip, i+1))
            
);

function split_chars_amount(string, split_char, split_chars=0, i=0) = (
    i == len(string) - 1  || len(string) == 0 ? 
        split_chars
    :
        split_chars_amount(string, split_char, string[i] == split_char ? split_chars+1 : split_chars, i+1)
);

function split(string, split_char="\n", i=0) = (
    i == split_chars_amount(string, split_char) ?
        split_chars_amount(string, split_char) == 0 ?
            concat(string)
        :
            string_array(string, split_char, i)
    :
        concat(string_array(string, split_char, i), split(string, split_char, i+1))
);

module better_text(string, size=10, font="MS Sans Serif", halign="left", valign="baseline", character_spacing=1, direction="ltr", language="en", script="latin", line_spacing=125, $fn=50) {
    lines = split(string);
    for(i=[0:len(lines)-1]) {
        translate([0, -line_spacing*size/100*i, 0])
        text(lines[i], size=size, font=font, halign=halign, valign=valign, spacing=character_spacing, direction=direction, language=language, script=script, $fn=$fn);
    }
}

function split_string(string, split_char, i=0) = (
    i == len(string)-1 ?
        string[i]
        :
        str(string[i] == split_char ? "\n" : string[i], split_string(string, split_char, i+1))
);


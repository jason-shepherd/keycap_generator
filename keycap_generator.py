"""This module takes RAW KLE keyboard data and generates the appropriate keycap stls"""

#used for external openscad commands on command line
import subprocess
#used for json parsing
import json


def generate_keycaps(json_path=r'keyboard-layout.json'):
    """generates keycap stl files from KLE RAW data"""


    #opens and parses json file
    try:
        with open(json_path, 'r', encoding='utf-8') as json_file:
            keyboard_data = json.load(json_file)
            json_file.close()
    except FileNotFoundError:
        print("Invalid JSON file path")
        return

    #extracts useful key data
    for ir, keyboard_row in enumerate(keyboard_data):
        default_width = 1.00
        default_height = 1.00
        skip = False

        for i, key in enumerate(keyboard_row):
            if skip:
                skip = False
                continue
            elif isinstance(key, str):
                if '\n' in key:
                    key = key.splitlines()
                print(key, default_width, default_height)
                create_scad_keycap(legends=key, width=default_width, height=default_height, output_path=str(ir) + " " + str(i) + r' key.scad')
            elif isinstance(key, dict):
                if '\n' in keyboard_row[i+1]:
                    keyboard_row[i+1] = keyboard_row[i+1].splitlines()
                print(keyboard_row[i+1], extract_metadata(key))
                tmp_width, tmp_height = extract_metadata(key)
                create_scad_keycap(legends=keyboard_row[i+1], width=tmp_width, height=tmp_height, output_path=str(ir) + " " + str(i) + r' key.scad')
                skip = True


def extract_metadata(metadata):
    "extracts metadata from dict file"


    width = 1.00
    height = 1.00
    try:
        width = metadata['w']
    except KeyError:
        print('no new width metadata')
    try:
        height = metadata['h']
    except KeyError:
        print('no new height metadata')
    return width, height


def create_scad_keycap(legends, width=1, height=1, scad_path=r'keycap.scad', output_path=r'keycap_out.scad'):
    """Creates a keycap scad object from width and height"""


    with open(scad_path, 'r', encoding='utf-8') as scad_file:
        scad_keycap = scad_file.read()
        scad_file.close()

    scad_keycap += "difference() {\n    create_keycap(u_width=" + str(width) + ", u_height=" + str(height) + ");\n  create_legends(["
    if(isinstance(legends, list)):
        for item in legends:
            scad_keycap += r'"' + item + r'",'
    else:
        scad_keycap += r'"' + legends + r'"'

    scad_keycap += "]);\n}"
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(scad_keycap)
        output_file.close()


if __name__ == '__main__':
    generate_keycaps(r'keyboard-layout.json')
    #create_scad_keycap(scad_path=r'keycap.scad', width=1, height=1, legends="W")

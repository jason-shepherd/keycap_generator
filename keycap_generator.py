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
    for keyboard_row in keyboard_data:
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
            elif isinstance(key, dict):
                if '\n' in keyboard_row[i+1]:
                    keyboard_row[i+1] = keyboard_row[i+1].splitlines()
                print(keyboard_row[i+1], extract_metadata(key))
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


def create_scad_keycap(width=1, height=1, scad_path=r'keycap.scad'):
    """Creates a keycap scad object from width and height"""


    with open(scad_path, 'a+', encoding='utf-8') as scad_file:
        scad_file.write("\ncreate_keycap(u_width=" + str(width) + ", u_height=" + str(height) + ");")
        scad_file.close()


if __name__ == '__main__':
    #generate_keycaps(r'keyboard-layout.json')
    create_scad_keycap(width=1, height=2, scad_path=r'keycap.scad')

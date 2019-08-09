"""This module takes RAW KLE keyboard data and generates the appropriate keycap stls"""

#used for external openscad commands on command line
import subprocess
#used for json parsing
import json
#used to generate scad file
import solid


def generate_keycaps(json_path):
    """generates keycap stl files from KLE RAW data"""


    #opens and parses json file
    try:
        with open(json_path, 'r', encoding='utf-8') as json_file:
            keyboard_data = json.load(json_file)
            json_file.close()
    except FileNotFoundError:
        print("Invalid JSON file path")
        return

    #extracts keycap data from parsed json file
     for keyboard_row in keyboard_data:
         width = 1.00
         height = 1.00
         index = 0
         skip = False

         for key in keyboard_row:
             if skip == True:
                 skip = False
                 index += 1
                 continue
             if isinstance(key, str):
                 if '\n' in key:
                     key = key.splitlines()
                 print(key, width, height)
             if isinstance(key, dict):
                 if '\n' in keyboard_row[index+1]:
                     keyboard_row[index+1] = keyboard_row[index+1].splitlines()
                 print(keyboard_row[index+1], extract_metadata(key))
                 skip = True
             index += 1


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


def create_scad_keycap(width, height):
    """Creates a keycap scad object from width and height"""
    keycap = solid.difference() (
                solid.linear_extrude()
            )


if __name__ == '__main__':
    generate_keycaps(r'keyboard-layout.json')

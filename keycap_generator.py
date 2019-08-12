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

    #extracts useful key data
    for keyboard_row in keyboard_data:
        width = 1.00
        height = 1.00
        skip = False

        for i in range(0, len(keyboard_row)):
            if skip == True:
                skip = False
                continue
            if isinstance(keyboard_row[i], str):
                if '\n' in keyboard_row[i]:
                    keyboard_row[i] = keyboard_row[i].splitlines()
                print(keyboard_row[i], width, height)
            if isinstance(keyboard_row[i], dict):
                if '\n' in keyboard_row[i+1]:
                    keyboard_row[i+1] = keyboard_row[i+1].splitlines()
                print(keyboard_row[i+1], extract_metadata(keyboard_row[i]))
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


def create_scad_keycap(width, height):
    """Creates a keycap scad object from width and height"""
    keycap = solid.difference() (
                solid.linear_extrude()
            )


if __name__ == '__main__':
    generate_keycaps(r'keyboard-layout.json')

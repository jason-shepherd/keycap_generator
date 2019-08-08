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
    width = 1.00
    height = 1.00
    for keyboard_rows in keyboard_data:
        for key_data in keyboard_rows:
            if isinstance(key_data, str):
                if "\n" in key_data:
                    key_data = key_data.splitlines()
                print(key_data, width, height)
            elif isinstance(key_data, dict):
                try:
                    width = key_data['w']
                except KeyError:
                    print("No new width found in metadata")
                try:
                    height = key_data['h']
                except KeyError:
                    print("No new height found in metadata")


def create_scad_keycap(width, height):
    """Creates a keycap scad object from width and height"""
    keycap = solid.difference() (
                solid.linear_extrude()
            )


if __name__ == '__main__':
    generate_keycaps(r'keyboard-layout.json')

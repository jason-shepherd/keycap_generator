"""This module takes RAW KLE keyboard data and generates the appropriate keycap stls"""

# used for external openscad commands on command line
import subprocess
# used for json parsing
import json
# for command line arg parsing 
import argparse
# pip install argparse to use


class KeycapGenerator:
    """Generates keycap"""

    def __init__(self, json_path='keyboard-layout.json', keycap_path='keycap.scad',
                 openscad_path='C:\\Program Files\\OpenSCAD\\openscad'):
        """init keycap generator"""

        self.json_path = json_path
        self.openscad_path = openscad_path
        self.keycap_path = keycap_path
        self.scad_keycap = None
        self.scad_file = None

    def generate_keycaps(self):
        """generates keycap stl files from KLE RAW data"""

        # opens and parses json file
        try:
            with open(self.json_path, 'r', encoding='utf-8') as json_file:
                keyboard_data = json.load(json_file)
                json_file.close()
        except FileNotFoundError:
            print("Invalid JSON file path")
            return

        #open scad template file
        try:
            self.scad_file = open(self.keycap_path, 'r+', encoding='utf-8')
            self.scad_keycap = self.scad_file.read()
        except FileNotFoundError:
            print("Invalid SCAD file path")
            return

        # extracts useful key data
        font_size = 3
        for ir, keyboard_row in enumerate(keyboard_data):
            keyboard_row = iter(keyboard_row)
            for i, key in enumerate(keyboard_row):
                width = 1
                height = 1
                homing = False
                legends = key

                if isinstance(key, dict):
                    width = key.get('w', 1)
                    height = key.get('h', 1)
                    homing = key.get('n', 1)
                    font_size = key.get('f', font_size)
                    legends = next(keyboard_row)

                if '\n' in legends:
                    legends = legends.splitlines()

                print(legends, width, height)
                self.create_scad_keycap(raw(legends), width, height, homing,
                                        font_size)
                self.scad_to_stl(self.keycap_path, "{} {} keycap.stl".format(ir, i))

        #rewrite original file data
        self.scad_file.truncate(0)
        self.scad_file.seek(0)
        self.scad_file.write(self.scad_keycap)
        self.scad_file.close()

    def create_scad_keycap(self, legends, width, height, homing, font_size):
        """Creates a keycap scad object from width and height"""

        keycap_call = """create_keycap(u_width={}, u_height={}, homing={},
                       font_size={}, legends=[""".format(width, height,
                               str(homing).lower(), font_size)

        if isinstance(legends, list):
            for item in legends:
                keycap_call += r'"' + item + r'",'
        else:
            keycap_call += r'"' + legends + r'"'

        keycap_call += "]);"
        self.scad_file.truncate(0)
        self.scad_file.seek(0)
        self.scad_file.write(self.scad_keycap + keycap_call)
        self.scad_file.flush()

    def scad_to_stl(self, scad_path, output_path):
        """Use openscad command line to create stl file from scad file"""

        openscad_process = subprocess.Popen([self.openscad_path, r'-o', output_path, scad_path],
                                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            shell=True)
        stdout, stderr = openscad_process.communicate()
        print(stdout, stderr)


def raw(text):
    """Returns a raw string representation of text"""


    new_text = None
    escape_dict = {'\a': r'\a', '\b': r'\b', '\c': r'\c', '\f': r'\f', '\n': r'\n', '\r': r'\r',
                   '\t': r'\t', '\v': r'\v', '\'': r'\'', '\"': r'\"', '\0': r'\0', '\1': r'\1',
                   '\2': r'\2', '\3': r'\3', '\4': r'\4', '\5': r'\5', '\6': r'\6', '\7': r'\7',
                   '\8': r'\8', '\9': r'\9', '\\' : r'\\\\'}

    if isinstance(text, str):
        new_text = ''
        for char in text:
            try:
                new_text += escape_dict[char]
            except KeyError:
                new_text += char
    elif isinstance(text, list):
        new_text = []
        for item in text:
            for char in item:
                new_string = ''
                try:
                    new_string += escape_dict[char]
                except KeyError:
                    new_string += char
                new_text.append(new_string)
    return new_text


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Generate your custom keycaps. REQUIRES OPENSCAD INSTALL!!')
    parser.add_argument('-j', '--json_path', default = 'keyboard-layout.json', type = str, dest = 'json_path', help = 'Path to KLE RAW json data')
    parser.add_argument('-k', '--keycap_path', default = 'keycap.scad', type = str, dest = 'keycap_path', help = 'Path to keycap scad file')
    parser.add_argument('-s', '--openscad_path', type = str, dest = 'openscad_path', help = 'Path to openscad executable install', required = True)
    args = parser.parse_args()

    generator = KeycapGenerator(args.json_path, args.keycap_path, args.openscad_path)
    generator.generate_keycaps()

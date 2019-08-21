"""This module takes RAW KLE keyboard data and generates the appropriate keycap stls"""

# used for external openscad commands on command line
import subprocess
# used for json parsing
import json


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
        #print(self.scad_keycap)

        # extracts useful key data
        for ir, keyboard_row in enumerate(keyboard_data):
            keyboard_row = iter(keyboard_row)
            for i, key in enumerate(keyboard_row):
                width = 1.00
                height = 1.00
                legends = key

                if isinstance(key, dict):
                    width, height = self.extract_metadata(key)
                    legends = next(keyboard_row)
                if '\n' in legends:
                    legends = legends.splitlines()
                print(legends, width, height)
                self.create_scad_keycap(legends, width, height)
                self.scad_to_stl(self.keycap_path, "{} {} keycap.stl".format(ir, i))
        self.scad_file.truncate(0)
        self.scad_file.seek(0)
        self.scad_file.write(self.scad_keycap)
        self.scad_file.close()

    def extract_metadata(self, metadata):
        "extracts metadata from dict file"

        return metadata.get('w', 1.00), metadata.get('h', 1.00)

    def create_scad_keycap(self, legends, width=1, height=1):
        """Creates a keycap scad object from width and height"""

        keycap_call = "\ncreate_keycap(u_width={}, u_height={}, legends=[".format(width, height)

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

    escape_dict = {'\a': r'\a', '\b': r'\b', '\c': r'\c', '\f': r'\f', '\n': r'\n', '\r': r'\r',
                   '\t': r'\t', '\v': r'\v', '\'': r'\'', '\"': r'\"', '\0': r'\0', '\1': r'\1',
                   '\2': r'\2', '\3': r'\3', '\4': r'\4', '\5': r'\5', '\6': r'\6', '\7': r'\7',
                   '\8': r'\8', '\9': r'\9'}
    if isinstance(text, str):
        new_string = ''
        for char in text:
            try:
                new_string += escape_dict[char]
            except KeyError:
                new_string += char
        return new_string
    elif isinstance(text, list):
        new_list = []
        for item in text:
            for char in item:
                new_string = ''
                try:
                    new_string += escape_dict[char]
                except KeyError:
                    new_string += char
                new_list.append(new_string)
            return new_list


if __name__ == '__main__':
    generator = KeycapGenerator()
    generator.generate_keycaps()

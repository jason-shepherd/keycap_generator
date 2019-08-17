"""This module takes RAW KLE keyboard data and generates the appropriate keycap stls"""

#used for external openscad commands on command line
import subprocess
#used for json parsing
import json

class KeycapGenerator:
    """Generates keycap"""


    def __init__(self, json_path='keyboard-layout.json', openscad_path='C:\\Program Files\\OpenSCAD\\openscad'):
        """init keycap generator"""


        self.json_path = json_path
        self.openscad_path = openscad_path


    def generate_keycaps(self):
        """generates keycap stl files from KLE RAW data"""
    
    
        #opens and parses json file
        try:
            with open(self.json_path, 'r', encoding='utf-8') as json_file:
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
                    self.create_scad_keycap(legends=raw(key), width=default_width, height=default_height, output_path=str(ir) + " " + str(i) + ' key.scad')
                    self.scad_to_stl(str(ir) + " " + str(i) + ' key.scad', str(ir) + " " + str(i) + ' key.stl')
                elif isinstance(key, dict):
                    if '\n' in keyboard_row[i+1]:
                        keyboard_row[i+1] = keyboard_row[i+1].splitlines()
                    tmp_width, tmp_height = self.extract_metadata(key)
                    print(keyboard_row[i+1], tmp_width, tmp_height)
                    self.create_scad_keycap(legends=raw(keyboard_row[i+1]), width=tmp_width, height=tmp_height, output_path=str(ir) + " " + str(i) + ' key.scad')
                    self.scad_to_stl(str(ir) + " " + str(i) + ' key.scad', str(ir) + " " + str(i) + ' key.stl')
                    skip = True
    
    
    def extract_metadata(self, metadata):
        "extracts metadata from dict file"
    
    
        return metadata.get('w', 1.00), metadata.get('h', 1.00) 
    
    
    def create_scad_keycap(self, legends, width=1, height=1, scad_path=r'keycap.scad', output_path=r'keycap_out.scad'):
        """Creates a keycap scad object from width and height"""
    
    
        with open(scad_path, 'r', encoding='utf-8') as scad_file:
            scad_keycap = scad_file.read()
            scad_file.close()
    
        scad_keycap += "\ncreate_keycap(u_width=" + str(width) + ", u_height=" + str(height) + ", legends=["
        if(isinstance(legends, list)):
            for item in legends:
                scad_keycap += r'"' + item + r'",'
        else:
            scad_keycap += r'"' + legends + r'"'
    
        scad_keycap += "]);"
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(scad_keycap)
            output_file.close()
    
    
    def scad_to_stl(self, scad_path, output_path):
        """Use openscad command line to create stl file from scad file"""
    
    
        openscad_process = subprocess.Popen([self.openscad_path, r'-o', output_path, scad_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = openscad_process.communicate()
        print(stdout, stderr)
    
    
def raw(text):
    """Returns a raw string representation of text"""
	
	
    escape_dict={'\a':r'\a','\b':r'\b','\c':r'\c','\f':r'\f','\n':r'\n','\r':r'\r','\t':r'\t','\v':r'\v','\'':r'\'',
                 '\"':r'\"','\0':r'\0','\1':r'\1','\2':r'\2','\3':r'\3','\4':r'\4','\5':r'\5','\6':r'\6','\7':r'\7','\8':r'\8','\9':r'\9'}
    if isinstance(text, str):
        new_string=''
        for char in text:
            try:
                new_string += escape_dict[char]
            except KeyError:
                new_string+=char
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

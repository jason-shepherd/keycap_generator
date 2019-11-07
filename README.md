# keycap_generator
Generates a keycap based on RAW Keyboard Layout Editor

# Use
To  use keycap_generator you must have OpenSCAD installed. keycap_generator use a json file from Keyboard Layout Editor to generate the keycaps. In order to generate keycaps simply enter the following command:  
```python keycap_generator.py -j <KLE json path> -s <openscad.exe path>```  
Optionally you can use a different SCAD file with the -k parameter, but make sure the function in it has the same parameters and name as the default keycap.scad.

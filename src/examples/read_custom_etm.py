import os, sys
from example_common import get_input_filepath

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from etm_reader import read_metadata_file
from etm_interpreter import EtmInterpreter
from etm_interpreter_filters import AssetFilter, FileFilter

'''
This example allows a user to place a custom metadata file into the
"examples/inputs" directory and will print out what it finds in that file.

Any errors or warnings are also printed.

The file placed in the "examples/inputs" directory should be named:
   "custom_metadata.json"
'''

if __name__ == '__main__':
    filepath = get_input_filepath('custom_metadata')
    if not os.path.exists(filepath):
        print('No custom metadata found. To use this example, place a file called \"custom_metadata.json\" into the examples/inputs directory')
    else:
        etm = read_metadata_file(filepath)
        etm_interpreter = EtmInterpreter(etm)
        if etm_interpreter.is_valid:
            assets = etm_interpreter.get_assets()
            if len(assets) > 0:
                print(f'Printing all assets...\n')
                for attribute_index in range(len(assets)):
                    assets[attribute_index].printout()

            attributes = etm_interpreter.get_attributes()
            if len(attributes) > 0:
                print(f'Printing all attributes...\n')
                for attribute_index in range(len(attributes)):
                    attributes[attribute_index].printout()

            print('')
            etm_interpreter.print_issues()
            print('')
        

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
        etm_handler = EtmInterpreter(etm)
        if etm_handler.is_valid:
            assets = etm_handler.get_assets()
            print(f'Printing all assets...\n')
            for asset_index in range(len(assets)):
                assets[asset_index].printout()

            print('')
            etm_handler.print_issues()
            print('')
        

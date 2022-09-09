import os, sys
from example_common import get_input_filepath

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from etm_reader import read_metadata_file
from etm_interpreter import EtmInterpreter

'''
This example shows how to read data from a metadata.json and print out
the data that is stored in the 'etm' hierarchy.

The file in this example has several errors and a warning which is
also printed.
'''

if __name__ == '__main__':
    filenames = ['multiple_assets', 'multiple_files', 'bad_metadata']
    
    for fn in filenames:
        filepath = get_input_filepath(fn)
        etm = read_metadata_file(filepath)
        
        if etm.issue_handler.has_errors() or etm.issue_handler.has_warnings():
            print(f'{fn}.json has errors:')
            etm.issue_handler.printout()
        else:
            print(f'{fn}.json is valid!')
        

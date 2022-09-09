import os, sys
from example_common import get_input_filepath

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from etm_reader import read_metadata_file

'''
This example shows how to read data from a metadata.json and print out
the data that is stored in the 'etm' hierarchy.

The file in this example has several errors and a warning which is
also printed.
'''

if __name__ == '__main__':
    filepath = get_input_filepath('bad_metadata')
    etm = read_metadata_file(filepath)

    etm.printout()
    print('')
    etm.issue_handler.printout()
    print('')
        

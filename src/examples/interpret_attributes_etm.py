import os, sys
from example_common import get_input_filepath

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from etm_reader import read_metadata_file
from etm_interpreter import EtmInterpreter
from etm_interpreter_filters import AttributeFilter

'''
This example demonstrates the asset and file filtering and handling functions
provided by the EtmHandler class.
'''

if __name__ == '__main__':
    filepath = get_input_filepath('attributes')
    etm = read_metadata_file(filepath)
    etm_handler = EtmInterpreter(etm)
    
    attributes = etm_handler.get_attributes()
    print(f'There are {len(attributes)} attributes.')

    print(f'\nAll data for the first attribute:')
    attributes[0].printout(indent_base_level=1)

    filtered_attributes = etm_handler.get_attributes(AttributeFilter(trait_type='Eyes'))
    print(f'\nAttribute with a \'trait_type\' of \"Eyes\":')
    filtered_attributes[0].printout(indent_base_level=1)

    filtered_attributes = etm_handler.get_attributes(AttributeFilter(value_type='number'))
    print(f'\nAttributes with a \'value_type\' of \"number\":')
    for a in filtered_attributes:
        a.printout(indent_base_level=1)
    
    print('')
    etm_handler.print_issues()
    print('')
        

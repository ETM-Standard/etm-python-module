import os, json
from urllib.request import urlopen

from standard_modules.standard_module_base import BaseStandardName, get_extension_module, InvalidStandardModule

def get_metadata_standard_name(metadata_dict):
    return metadata_dict.get('metadata_standard')

def is_etm(metadata_dict):
    metadata_standard = get_metadata_standard_name(metadata_dict)
    if metadata_standard == None: return False
    return BaseStandardName(metadata_standard).is_valid

def read_metadata_file(filepath):
    with open(filepath) as json_file:
        return read_metadata_dict(json.load(json_file))

def read_metadata_url(url):
    with urlopen(url) as json_response:
        return read_metadata_dict(json.loads(json_response.read()))

def read_metadata_dict(metadata_dict):
    if not is_etm(metadata_dict):
        print(f'ERROR: JSON does not follow the ETM standard (invalid \'metadata_standard\' entry)')
        return InvalidStandardModule().from_dict(metadata_dict).validate()
    try:
        return get_extension_module(get_metadata_standard_name(metadata_dict)).from_dict(metadata_dict).validate()
    except Exception as e:
        print(e)
    return None

if __name__ == '__main__':
    source_dir = os.path.join(os.path.dirname(__file__), 'examples', 'inputs')
    def get_files_of_type(directory, file_extension): return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.split('.')[-1] == file_extension]
    
    for file in get_files_of_type(source_dir, 'json'): #get all metadata example filenames
        filepath = os.path.join(source_dir, file)
        etm = read_metadata_file(filepath)
        if etm != None:
            etm.printout()
            print('')
            etm.issue_handler.printout()
            print('\n')
        

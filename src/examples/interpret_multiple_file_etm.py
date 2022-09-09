import os, sys
from example_common import get_input_filepath

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from etm_reader import read_metadata_file
from etm_interpreter import EtmInterpreter
from etm_interpreter_filters import AssetFilter, FileFilter

'''
This example demonstrates the asset and file filtering and handling functions
provided by the EtmHandler class.
'''

if __name__ == '__main__':
    filepath = get_input_filepath('multiple_files')
    etm = read_metadata_file(filepath)
    etm_handler = EtmInterpreter(etm)
    
    assets = etm_handler.get_assets()
    print(f'There is {len(assets)} asset and that asset has {len(assets[0].files)} files.')
    print(f'The name of the asset is "{assets[0].name}"')
    print(f'The names of the files are: {[f.name for f in etm_handler.get_files()]}')

    print(f'\nAll data for the first file:')
    assets[0].files[0].printout(indent_base_level=1)

    print(f'\nAll assets that are avatars: {etm_handler.get_assets(AssetFilter(asset_type="avatar"))}')
    print(f'All files that are models: {etm_handler.get_files(FileFilter(media_type="model"))}')
    print(f'All files from assets with a \'model\' mediaType: {etm_handler.get_files(FileFilter(asset_filter=AssetFilter(media_type="model")))}')

    print('')
    etm_handler.print_issues()
    print('')
        

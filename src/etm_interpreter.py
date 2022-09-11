import os, requests

from standard_modules.standard_module_base import InvalidStandardModule
from etm_reader import read_metadata_file
from etm_interpreter_filters import AssetFilter, FileFilter, AttributeFilter

class EtmInterpreter:
    def __init__(self, etm):
        self.etm = etm
        self.is_valid = not isinstance(etm, InvalidStandardModule)
    def get_assets(self, asset_filter=AssetFilter()):
        etm_multiasset = self.etm.try_get_extension('ETM_MULTIASSET') if self.is_valid else None
        if etm_multiasset == None: return []
        return asset_filter.filter(etm_multiasset.assets)
    def get_files(self, file_filter=FileFilter()):
        files = [f for a in self.get_assets() for f in a.files]
        return file_filter.filter(files)
    def get_attributes(self, attribute_filter=AttributeFilter()):
        etm_attributes = self.etm.try_get_extension('ETM_ATTRIBUTES') if self.is_valid else None
        if etm_attributes == None: return []
        return attribute_filter.filter(etm_attributes.attributes)
    def _get_unique_filepath(self, dirpath, file_basename, file_extension):
        filepath = os.path.join(dirpath, f'{file_basename}.{file_extension}')
        index = 1
        while os.path.exists(filepath):
            filepath = os.path.join(dirpath, f'{file_basename} ({index}).{file_extension}')
            index += 1
        return filepath
    def download_files(self, download_dirpath, file_filter=FileFilter()):
        files = self.get_files(file_filter)
        filepaths = []
        for file in files:
            filepaths.append(self._get_unique_filepath(download_dirpath, file.name, file.file_extension))
            open(filepaths[-1], 'wb').write(requests.get(file.url).content)
        return files, filepaths
    def print_issues(self):
        self.etm.issue_handler.printout()


if __name__ == '__main__':
    source_dir = os.path.join(os.path.dirname(__file__), 'examples', 'inputs')
    def get_files_of_type(directory, file_extension): return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.split('.')[-1] == file_extension]

    for file in get_files_of_type(source_dir, 'json'): #get all metadata example filenames
        filepath = os.path.join(source_dir, file)
        etm = read_metadata_file(filepath)
        
        etm_handler = EtmInterpreter(etm)
        assets = etm_handler.get_assets()
        print(f'All assets: {assets}')
        if len(assets) > 0: print(f'All files for first asset: {etm_handler.get_files(assets[0])}')
        print(f'All files (for all assets): {etm_handler.get_files()}')

        if len(assets) > 0: etm_handler.get_files(assets[0])[0].printout()
        etm.issue_handler.printout()

        print('\n')
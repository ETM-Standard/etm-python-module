from standard_modules.standard_module_base import JsonObject
from standard_modules.etm_multiasset_file import File
from standard_modules.etm_multiasset_common import VALID_MEDIA_TYPES

NAME_KEY = 'name'
DESCRIPTION_KEY = 'description'
MEDIA_TYPE_KEY = 'media_type'
ASSET_TYPE_KEY = 'asset_type'
FILES_KEY = 'files'

class Asset(JsonObject):
    def __init__(self, parent):
        JsonObject.__init__(self, parent)
        self.asset_index = -1
    def from_values(self, media_type, name=None, description=None, asset_type=None):
        self.name = name
        self.description = description
        self.media_type = media_type
        self.asset_type = asset_type
        self.files = []
        return self
    def from_dict(self, asset_dict, fallback_name, fallback_description):
        self.name = asset_dict.get(NAME_KEY, fallback_name)
        self.description = asset_dict.get(DESCRIPTION_KEY, fallback_description)
        self.media_type = asset_dict.get(MEDIA_TYPE_KEY)
        self.asset_type = asset_dict.get(ASSET_TYPE_KEY)
        file_dicts = asset_dict.get(FILES_KEY)
        if file_dicts == None: self.files = None
        else:
            self.files = []
            for file_dict in file_dicts:
                file = File(self).from_dict(file_dict, fallback_name, fallback_description)
                self.add_file(file)
        return self
    def to_dict(self, asset_dict_list):
        asset_dict = {}
        if self.name != None: asset_dict[NAME_KEY] = self.name
        if self.description != None: asset_dict[DESCRIPTION_KEY] = self.description
        asset_dict[MEDIA_TYPE_KEY] = self.media_type
        if self.asset_type != None: asset_dict[ASSET_TYPE_KEY] = self.asset_type
        asset_dict[FILES_KEY] = []
        for file in self.files:
            file.to_dict(asset_dict[FILES_KEY])
        asset_dict_list.append(asset_dict)
    def add_file(self, file):
        if self.files == None: return
        file.file_index = len(self.files)
        self.files.append(file)
    def _log_error(self, message): #helper function
        self.issue_handler.log_error(self.parent.standard_name.get_full_name(), f'Asset[{self.asset_index}]', message)
    def validate(self):
        if self.media_type == None: self._log_error(f'\'asset\' JSON must contain an \"{MEDIA_TYPE_KEY}\" key')
        elif self.media_type not in VALID_MEDIA_TYPES: self._log_error(f'\'asset\' has an invalid \'mediaType\': {self.media_type}')
        if self.files == None: self._log_error(f'\'asset\' JSON must contain a \"{FILES_KEY}\" key')
        elif self.media_type not in [f.file_type.split('/')[0] for f in self.files if f.file_type != None]:
            self._log_error(f'a file must have a \'fileType\' that matches the asset\'s \'mediaType\': {self.media_type}')
        if self.files != None:
            for file in self.files:
                file.validate()
        return self
    def printout(self, indent_base_level=0):
        self.print_indented(f'ASSET {self.asset_index}:', indent_base_level)
        self.print_entry(NAME_KEY, self.name, indent_level=indent_base_level+1)
        self.print_entry(DESCRIPTION_KEY, self.description, indent_level=indent_base_level+1)
        self.print_entry(MEDIA_TYPE_KEY, self.media_type, indent_level=indent_base_level+1)
        self.print_entry(ASSET_TYPE_KEY, self.asset_type, indent_level=indent_base_level+1)
        for file in self.files:
            file.printout(indent_base_level+1)
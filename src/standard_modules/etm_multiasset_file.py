from standard_modules.standard_module_base import JsonObject
from standard_modules.etm_multiasset_common import VALID_MEDIA_TYPES

NAME_KEY = 'name'
DESCRIPTION_KEY = 'description'
URL_KEY = 'url'
FILE_TYPE_KEY = 'file_type'

class File(JsonObject):
    def __init__(self, parent):
        JsonObject.__init__(self, parent)
        self.file_index = -1
    def from_values(self, url, file_type, name=None, description=None):
        self.name = name
        self.description = description
        self.url = url
        self.file_type = file_type
        return self
    def _set_file_type(self, file_type):
        self.file_type = file_type
        if self.file_type != None:
            self.media_type = self.file_type.split('/')[0]
            self.file_extension = self.file_type.split('/')[1] if len(self.file_type.split('/')) == 2 else 'invalid'
    def from_dict(self, file_dict, fallback_name, fallback_description):
        self.name = file_dict.get(NAME_KEY, fallback_name)
        self.description = file_dict.get(DESCRIPTION_KEY, fallback_description)
        self.url = file_dict.get(URL_KEY)
        self._set_file_type(file_dict.get(FILE_TYPE_KEY))
        return self
    def to_dict(self, file_dict_list):
        file_dict = {}
        if self.name != None: file_dict[NAME_KEY] = self.name
        if self.description != None: file_dict[DESCRIPTION_KEY] = self.description
        file_dict[URL_KEY] = self.url
        file_dict[FILE_TYPE_KEY] = self.file_type
        file_dict_list.append(file_dict)
    def _log_error(self, message):
        self.issue_handler.log_error(self.parent.parent.standard_name.get_full_name(), f'Asset[{self.parent.asset_index}].File[{self.file_index}]', message)
    def validate(self):
        if self.url == None: self._log_error(f'\'file\' JSON must contain an \"{URL_KEY}\" key')
        if self.file_type == None: self._log_error(f'\'file\' JSON must contain a \"{FILE_TYPE_KEY}\" key')
        else:
            if len(self.file_type.split('/')) != 2: self._log_error(f'\'file\' has an invalid \'fileType\' MIME format: {self.file_type}')
            elif self.file_type.split('/')[1].startswith('.'): self._log_error(f'\'fileType\' file extension must not include \'.\': {self.file_type}')
            if self.file_type.split('/')[0] not in VALID_MEDIA_TYPES: self._log_error(f'\'fileType\' has an invalid \'mediaType\': {self.file_type}')
        return self
    def printout(self, indent_base_level=0):
        self.print_indented(f'FILE {self.file_index}:', indent_base_level)
        self.print_entry(NAME_KEY, self.name, indent_level=indent_base_level+1)
        self.print_entry(DESCRIPTION_KEY, self.description, indent_level=indent_base_level+1)
        self.print_entry(URL_KEY, self.url, indent_level=indent_base_level+1)
        self.print_entry(FILE_TYPE_KEY, self.file_type, indent_level=indent_base_level+1)
from standard_modules import issue_handler
from standard_modules.standard_module_base import ExtensionName, JsonObject, StandardModule, get_extension_module

NAME_KEY = 'name'
DESCRIPTION_KEY = 'description'
IMAGE_KEY = 'image'
METADATA_STANDARD_KEY = 'metadata_standard'
EXTENSIONS_KEY = 'extensions'

class ETM_v1_0_0(StandardModule):
    def __init__(self, parent=None):
        StandardModule.__init__(self, None)
    def from_values(self, name, description=None, image=None):
        self.name = name
        self.description = description
        self.image = image
        self.metadata_standard = self._get_standard_name()
        self.extensions = []
        return self
    def from_dict(self, metadata_dict):
        self.name = metadata_dict.get(NAME_KEY)
        self.description = metadata_dict.get(DESCRIPTION_KEY)
        self.image = metadata_dict.get(IMAGE_KEY)
        self.metadata_standard = metadata_dict.get(METADATA_STANDARD_KEY)
        extension_names = metadata_dict.get(EXTENSIONS_KEY)
        if extension_names == None: self.extensions = None
        else:
            self.extensions = []
            for extension_name in extension_names:
                if not ExtensionName(extension_name).is_valid:
                    self._log_error(f'extension \"{extension_name}\" has an invalid name') #TODO
                    continue
                extension = get_extension_module(extension_name, self).from_dict(metadata_dict)
                self.extend(extension)
        return self
    def to_dict(self):
        metadata_dict = {}
        metadata_dict[NAME_KEY] = self.name
        if self.description != None: metadata_dict[DESCRIPTION_KEY] = self.description
        if self.image != None: metadata_dict[IMAGE_KEY] = self.image
        metadata_dict[METADATA_STANDARD_KEY] = self.metadata_standard
        metadata_dict[EXTENSIONS_KEY] = [ext.standard_name.get_full_name() for ext in self.extensions]
        for extension in self.extensions:
            extension.to_dict(metadata_dict)
        return metadata_dict
    def extend(self, extension):
        self.extensions.append(extension)
    def _log_error(self, message): #helper function
        self.issue_handler.log_error(self.standard_name.get_full_name(), 'Top-Level JSON', message)
    def _log_warning(self, message): #helper function
        self.issue_handler.log_warning(self.standard_name.get_full_name(), 'Top-Level JSON', message)
    def validate(self):
        self.issue_handler.clear()
        if self.name == None: self._log_error(f'must contain a \"{NAME_KEY}\" key')
        if self.image == None: self._log_warning(f'an \"{IMAGE_KEY}\" key is recommended')
        if self.metadata_standard == None: self._log_error(f'must contain a \"{METADATA_STANDARD_KEY}\" key')
        if self.extensions == None: self._log_error(f'must contain a \"{EXTENSIONS_KEY}\" key')
        else:
            for extension in self.extensions:
                if not extension.standard_name.is_valid:
                    self._log_error(f'extension \"{extension.standard_name.get_full_name()}\" has an invalid name')
                extension.validate()
        return self
    def printout(self, indent_base_level=0):
        print(self.standard_name.get_full_name())
        self.print_entry(NAME_KEY, self.name, indent_level=1)
        self.print_entry(DESCRIPTION_KEY, self.description, indent_level=1)
        self.print_entry(IMAGE_KEY, self.image, indent_level=1)
        self.print_entry(METADATA_STANDARD_KEY, self.metadata_standard, indent_level=1)
        self.print_entry(EXTENSIONS_KEY, [e.standard_name.get_full_name() for e in self.extensions], indent_level=1)
        for extension in self.extensions:
            print('')
            extension.printout(indent_base_level=0)
    def try_get_extension(self, exension_basename):
        for extension in self.extensions:
            if extension.standard_name.get_basename() == exension_basename:
                return extension
        return None
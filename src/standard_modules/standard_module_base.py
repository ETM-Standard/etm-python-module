from abc import ABC, abstractmethod
import importlib
from re import S
from turtle import st
from standard_modules.issue_handler import IssueHandler

# def extension_name_valid(extension_name):
#     if len(extension_name.split('_')) != 3: return False #verify 3 sections separated by underscores
#     extension_name_parts = extension_name.split('_')
    
#     if not extension_name_parts[0] == 'ETM': return False

#     if not extension_name_parts[2].startswith('v'): return False
#     version = extension_name_parts[2][1:]
#     if len(version.split('.')) != 3: return False #verify version
#     version_parts = version.split('.')
#     for digit in version_parts:
#         if not digit.isdigit(): return False
#     return True

def get_extension_module(standard_name_str, parent=None):
    standard_name = get_standard_name(standard_name_str)
    module = importlib.import_module(f'standard_modules.{standard_name.get_basename()}'.lower())
    if not hasattr(module, standard_name_str.replace('.','_')): raise Exception(standard_name_str)
    extension_module_class = getattr(module, standard_name_str.replace('.','_'))
    return extension_module_class(parent)


# Standard Name -----------------------------------------------------------------------------------
class StandardName(ABC):
    def __init__(self, standard_name_str):
        self.is_valid = self._validate(standard_name_str)
    @abstractmethod
    def _parse(self, standard_name_str):
        pass
    @abstractmethod
    def _validate(self, standard_name_str):
        pass
    def _validate_version(self, version_str):
        if not version_str.startswith('v'): return False
        version = version_str[1:]
        if len(version.split('.')) != 3: return False #verify version
        version_parts = version.split('.')
        for digit in version_parts:
            if not digit.isdigit(): return False
        return True
    @abstractmethod
    def get_basename(self):
        pass
    @abstractmethod
    def get_full_name(self):
        pass

class BaseStandardName(StandardName):
    def __init__(self, standard_name_str):
        StandardName.__init__(self, standard_name_str)
        if self.is_valid: self._parse(standard_name_str)
    def _parse(self, standard_name_str):
        standard_name_parts = standard_name_str.split('_')
        self.developer_code = standard_name_parts[0]
        standard_version_parts = standard_name_parts[1][1:].split('.')
        self.version_major = int(standard_version_parts[0])
        self.version_minor = int(standard_version_parts[1])
        self.version_patch = int(standard_version_parts[2])
    def _validate(self, standard_name_str):
        if len(standard_name_str.split('_')) != 2: return False #verify 3 sections separated by underscores
        standard_name_parts = standard_name_str.split('_')
        if not standard_name_parts[0] == 'ETM': return False
        return self._validate_version(standard_name_parts[1])
    def get_basename(self):
        return self.developer_code
    def get_full_name(self):
        return f'{self.developer_code}_v{self.version_major}.{self.version_minor}.{self.version_patch}'

class ExtensionName(StandardName):
    def __init__(self, standard_name_str):
        StandardName.__init__(self, standard_name_str)
        if self.is_valid: self._parse(standard_name_str)
    def _parse(self, standard_name_str):
        standard_name_parts = standard_name_str.split('_')
        self.developer_code = standard_name_parts[0]
        self.extension_name = standard_name_parts[1]
        standard_version_parts = standard_name_parts[2][1:].split('.')
        self.version_major = int(standard_version_parts[0])
        self.version_minor = int(standard_version_parts[1])
        self.version_patch = int(standard_version_parts[2])
    def _validate(self, standard_name_str):
        if len(standard_name_str.split('_')) != 3: return False #verify 3 sections separated by underscores
        standard_name_parts = standard_name_str.split('_')
        if not standard_name_parts[0] == 'ETM': return False
        return self._validate_version(standard_name_parts[2])
    def get_basename(self):
        return f'{self.developer_code}_{self.extension_name}'
    def get_full_name(self):
        return f'{self.developer_code}_{self.extension_name}_v{self.version_major}.{self.version_minor}.{self.version_patch}'

def get_standard_name(standard_name_str):
    standard_name_parts = standard_name_str.split('_')
    if len(standard_name_parts) == 2: return BaseStandardName(standard_name_str)
    else: return ExtensionName(standard_name_str)

def class_name_to_standard_name(class_name_str):
    class_name_parts = class_name_str.split('_') #this relies on classes being named as extension names with '.' replaced with '_' (due to variable naming restrictions)
    if len(class_name_parts) == 5: #it is an extension
        return f'{class_name_parts[0]}_{class_name_parts[1]}_{class_name_parts[2]}.{class_name_parts[3]}.{class_name_parts[4]}'
    elif len(class_name_parts) == 4: #it is the ETM base class
        return f'{class_name_parts[0]}_{class_name_parts[1]}.{class_name_parts[2]}.{class_name_parts[3]}'
    else: #it is something invalid
        return 'INVALID'


# Module Base Classes -----------------------------------------------------------------------------------
class JsonObject(ABC):
    def __init__(self, parent=None):
        self.parent = parent
        self.issue_handler = parent.issue_handler if parent != None else IssueHandler()
    @abstractmethod
    def from_values(self):
        pass
    @abstractmethod
    def from_dict(self, metadata_dict):
        pass
    @abstractmethod
    def to_dict(self, metadata_dict):
        pass
    @abstractmethod
    def validate(self):
        pass
    @abstractmethod
    def printout(self, indent_base_level=0):
        pass
    def print_indented(self, message, indent_level):
        indent = '   '*indent_level
        print(f'{indent}{message}')
    def print_standard_name(self, indent_level=0):
        self.print_indented(self.standard_name.get_full_name(), indent_level)
    def print_entry(self, key, value, indent_level=0):
        self.print_indented(f'{key}: {value}', indent_level)

class StandardModule(JsonObject):
    def __init__(self, parent=None):
        JsonObject.__init__(self, parent)
        self.standard_name = get_standard_name(self._get_standard_name())
    def _get_standard_name(self): #this exists to prevent redundant entering of versions - instead they are defined by class name
        class_name = type(self).__name__
        if class_name == 'StandardModule': return '_get_standard_name must be called on an extension module and not the StandardModule base class.'
        return class_name_to_standard_name(class_name)

class BaseStandardModule(StandardModule):
    def __init__(self):
        StandardModule.__init__(self, None)

#this only exists to pass back an "invalid" module rather than None if there is a fundamental issue with the metadataStandard
class InvalidStandardModule(StandardModule):
    def __init__(self, parent=None):
        StandardModule.__init__(self, None)
        self.metadata_dict = {}
    def from_values(self):
        return self
    def from_dict(self, metadata_dict):
        self.metadata_dict = metadata_dict
        return self
    def to_dict(self):
        return {}
    def validate(self):
        metadata_standard_key = 'metadataStandard'
        if not metadata_standard_key in self.metadata_dict:
            self.issue_handler.log_error('ETM_EXTENSIBLE_v...', 'Top-Level JSON', 'must contain a \"metadataStandard\" key')
        else:
            self.issue_handler.log_error('ETM_EXTENSIBLE_v...', 'Top-Level JSON', 'the \"metadataStandard\" value is invalid')
        return self
    def printout(self, indent_base_level=0):
        pass
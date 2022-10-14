from standard_modules.standard_module_base import JsonObject

DISPLAY_TYPE_KEY = 'display_type'
TRAIT_TYPE_KEY = 'trait_type'
VALUE_KEY = 'value'

class Attribute(JsonObject):
    def __init__(self, parent):
        JsonObject.__init__(self, parent)
        self.attribute_index = -1
    def from_values(self, value, trait_type=None, display_type=None):
        self.value = value
        self.value_type = self._get_value_type()
        self._value_key_present = True
        self.trait_type = trait_type
        self.display_type = display_type
        return self
    def from_dict(self, attribute_dict):
        self.display_type = attribute_dict.get(DISPLAY_TYPE_KEY)
        self.trait_type = attribute_dict.get(TRAIT_TYPE_KEY)
        self.value = attribute_dict.get(VALUE_KEY)
        self._value_key_present = VALUE_KEY in attribute_dict #this check exists since 'value' can be null
        self.value_type = self._get_value_type()
        return self
    def _get_value_type(self):
        if self.value == None: return 'null'
        if type(self.value)==bool: return 'boolean'
        if type(self.value)==int or type(self.value)==float: return 'number'
        #check if number as string
        def _is_number(s):
            try:
                float(s)
                return True
            except ValueError:
                return False
        if _is_number(self.value): return 'number_string'
        #check if boolean as string
        if self.value.lower() in ('true', 'false'): return 'boolean_string'
        #default to string
        return 'string'
    def to_dict(self, attribute_dict_list):
        attribute_dict = {}
        if self.display_type != None: attribute_dict[DISPLAY_TYPE_KEY] = self.display_type
        if self.trait_type != None: attribute_dict[TRAIT_TYPE_KEY] = self.trait_type
        attribute_dict[VALUE_KEY] = self.value
        attribute_dict_list.append(attribute_dict)
    def _log_error(self, message):
        self.issue_handler.log_error(self.parent.standard_name.get_full_name(), f'Attribute[{self.attribute_index}]', message)
    def _log_warning(self, message):
        self.issue_handler.log_warning(self.parent.standard_name.get_full_name(), f'Attribute[{self.attribute_index}]', message)
    def validate(self):
        if self.trait_type == None: self._log_warning(f'a \"{TRAIT_TYPE_KEY}\" key is recommended')
        if not self._value_key_present: self._log_error(f'\'attribute\' JSON must contain a \"{VALUE_KEY}\" key')
        if self.value_type == 'number_string': self._log_warning(f'\"{VALUE_KEY}\" is a string, should it be a number?')
        if self.value_type == 'boolean_string': self._log_warning(f'\"{VALUE_KEY}\" is a string, should it be a boolean?')
        return self
    def printout(self, indent_base_level=0):
        self.print_indented(f'ATTRIBUTE {self.attribute_index}:', indent_base_level)
        self.print_entry(DISPLAY_TYPE_KEY, self.display_type, indent_level=indent_base_level+1)
        self.print_entry(TRAIT_TYPE_KEY, self.trait_type, indent_level=indent_base_level+1)
        self.print_entry(VALUE_KEY, self.value, indent_level=indent_base_level+1)
        self.print_entry('value_type', self.value_type, indent_level=indent_base_level+1)
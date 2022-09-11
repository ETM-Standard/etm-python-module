from standard_modules.standard_module_base import StandardModule
from standard_modules.etm_attributes_attribute import Attribute

ATTRIBUTES_KEY = 'attributes'

class ETM_ATTRIBUTES_v1_0_0(StandardModule):
    def __init__(self, parent=None):
        StandardModule.__init__(self, parent)
    def from_values(self):
        self.attributes = []
        return self
    def from_dict(self, metadata_dict):
        attribute_dicts = metadata_dict.get(ATTRIBUTES_KEY)
        if attribute_dicts == None: self.attributes = None
        else:
            self.attributes = []
            for attribute_dict in attribute_dicts:
                attribute = Attribute(self).from_dict(attribute_dict)
                self.add_attribute(attribute)
        return self
    def to_dict(self, metadata_dict):
        metadata_dict[ATTRIBUTES_KEY] = []
        for attribute in self.attributes:
            attribute.to_dict(metadata_dict[ATTRIBUTES_KEY])
    def add_attribute(self, attribute):
        if self.attributes == None: return
        attribute.attribute_index = len(self.attributes)
        self.attributes.append(attribute)
    def _log_error(self, message): #helper function
        self.issue_handler.log_error(self.standard_name.get_full_name(), 'Top-Level JSON', message)
    def validate(self):
        if self.attributes == None: self._log_error(f'must contain a \"{ATTRIBUTES_KEY}\" key')
        else:
            for attribute in self.attributes:
                attribute.validate()
        return self
    def printout(self, indent_base_level=0):
        self.print_standard_name(indent_base_level)
        for attribute in self.attributes:
            attribute.printout(indent_base_level+1)

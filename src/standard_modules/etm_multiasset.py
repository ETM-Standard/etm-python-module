from standard_modules.standard_module_base import JsonObject, StandardModule
from standard_modules.etm_multiasset_asset import Asset
from standard_modules.etm_multiasset_common import VALID_MEDIA_TYPES

ASSETS_KEY = 'assets'

class ETM_MULTIASSET_v1_0_0(StandardModule):
    def __init__(self, parent=None):
        StandardModule.__init__(self, parent)
    def from_values(self):
        self.assets = []
        return self
    def from_dict(self, metadata_dict):
        asset_dicts = metadata_dict.get(ASSETS_KEY)
        if asset_dicts == None: self.assets = None
        else:
            self.assets = []
            for asset_dict in asset_dicts:
                asset = Asset(self).from_dict(asset_dict, self.parent.name, self.parent.description)
                self.add_asset(asset)
        return self
    def to_dict(self, metadata_dict):
        metadata_dict[ASSETS_KEY] = []
        for asset in self.assets:
            asset.to_dict(metadata_dict[ASSETS_KEY])
    def add_asset(self, asset):
        if self.assets == None: return
        asset.asset_index = len(self.assets)
        self.assets.append(asset)
    def _log_error(self, message): #helper function
        self.issue_handler.log_error(self.standard_name.get_full_name(), 'Top-Level JSON', message)
    def validate(self):
        if self.assets == None: self._log_error(f'must contain a \"{ASSETS_KEY}\" key')
        else:
            for asset in self.assets:
                asset.validate()
        return self
    def printout(self, indent_base_level=0):
        self.print_standard_name(indent_base_level)
        for asset in self.assets:
            asset.printout(indent_base_level+1)

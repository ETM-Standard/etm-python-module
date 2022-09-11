from abc import ABC, abstractmethod

class Filter(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def matches_filter(self):
        pass
    @abstractmethod
    def filter(self):
        pass

class AssetFilter(Filter):
    def __init__(self, media_type=None, asset_type=None):
        self.media_type = media_type
        self.asset_type = asset_type
    def matches_filter(self, asset):
        return (self.media_type == None or asset.media_type == self.media_type) and\
            (self.asset_type == None or asset.asset_type == self.asset_type)
    def filter(self, assets):
        return [a for a in assets if self.matches_filter(a)]

class FileFilter(Filter):
    def __init__(self, asset=None, asset_filter=None, file_type=None, media_type=None):
        self.asset = asset
        self.asset_filter = asset_filter
        self.file_type = file_type
        self.media_type = media_type
    def matches_filter(self, file):
        return (self.asset == None or file.parent == self.asset) and\
            (self.asset_filter == None or self.asset_filter.matches_filter(file.parent)) and\
            (self.media_type == None or file.media_type == self.media_type) and\
            (self.media_type == None or file.media_type == self.media_type)
    def filter(self, files):
        return [f for f in files if self.matches_filter(f)]

class AttributeFilter(Filter):
    def __init__(self, display_type=None, trait_type=None, value=None, value_type=None):
        self.display_type = display_type
        self.trait_type = trait_type
        self.value = value
        self.value_type = value_type
    def matches_filter(self, attribute):
        return (self.display_type in [None, attribute.display_type]) and\
            (self.trait_type in [None, attribute.trait_type]) and\
            (self.value in [None, attribute.value]) and\
            (self.value_type in [None, attribute.value_type])
    def filter(self, attributes):
        return [a for a in attributes if self.matches_filter(a)]
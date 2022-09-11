import os, sys
import pytest, copy

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
import etm_reader
from standard_modules import etm_attributes_attribute

VALID_METADATA_DICT = {
    "name": "My Cool NFT",
    "description": "A very cool NFT.",
    "image": "https://coolnfts.com/preview.mp4",
    "metadata_standard": "ETM_v1.0.0",
    "extensions": [ "ETM_ATTRIBUTES_v1.0.0" ],
    "attributes": []
}

VALID_ATTRIBUTE_DICT = {
    "display_type": None,
    "trait_type": "Eyes",
    "value": "Blue"
}

# TOP LEVEL ---------------------------------------------------------------------------------------

def test_etmAttributes_validMetadataHasNoErrorsOrWarnings():
    etm = etm_reader.read_metadata_dict(VALID_METADATA_DICT)
    assert not etm.issue_handler.has_errors() and not etm.issue_handler.has_warnings()

def test_etmAttributes_missingAttributesHasError():
    metadata_dict = copy.deepcopy(VALID_METADATA_DICT)
    del metadata_dict['attributes']
    etm = etm_reader.read_metadata_dict(metadata_dict)
    assert etm.issue_handler.has_errors()

# ASSET -------------------------------------------------------------------------------------------

def _create_test_attribute(etm, dict=VALID_ATTRIBUTE_DICT):
    attribute = etm_attributes_attribute.Attribute(etm).from_dict(dict)
    return attribute.validate()

def test_etmAttributesAttribute_validAttributeHasNoErrorsOrWarnings():
    etm = etm_reader.read_metadata_dict(VALID_METADATA_DICT)
    attribute = _create_test_attribute(etm)
    assert not attribute.issue_handler.has_errors() and not attribute.issue_handler.has_warnings()

def _remove_valid_attribute_dict_key_and_create_attribute(key):
    etm = etm_reader.read_metadata_dict(VALID_METADATA_DICT)
    attribute_dict = copy.deepcopy(VALID_ATTRIBUTE_DICT)
    del attribute_dict[key]
    attribute = _create_test_attribute(etm, dict=attribute_dict)
    return attribute

def test_etmAttributesAttribute_missingDisplayTypeHasNoError():
    attribute = _remove_valid_attribute_dict_key_and_create_attribute('display_type')
    assert not attribute.issue_handler.has_errors()

def test_etmAttributesAttribute_missingTraitTypeHasNoError():
    attribute = _remove_valid_attribute_dict_key_and_create_attribute('trait_type')
    assert not attribute.issue_handler.has_errors()

def test_etmAttributesAttribute_missingValueHasError():
    attribute = _remove_valid_attribute_dict_key_and_create_attribute('value')
    assert attribute.issue_handler.has_errors()

def _replace_value_and_create_attribute(key, value):
    etm = etm_reader.read_metadata_dict(VALID_METADATA_DICT)
    attribute_dict = copy.deepcopy(VALID_ATTRIBUTE_DICT)
    attribute_dict[key] = value
    attribute = _create_test_attribute(etm, dict=attribute_dict)
    return attribute

def test_etmAttributesAttribute_nullValueTypeRecognized():
    attribute = _replace_value_and_create_attribute('value', None)
    assert attribute.value_type == 'null'

def test_etmAttributesAttribute_stringValueTypeRecognized():
    attribute = _replace_value_and_create_attribute('value', 'stringly')
    assert attribute.value_type == 'string'

def test_etmAttributesAttribute_integerValueTypeRecognized():
    attribute = _replace_value_and_create_attribute('value', 0)
    assert attribute.value_type == 'number'

def test_etmAttributesAttribute_floatValueTypeRecognized():
    attribute = _replace_value_and_create_attribute('value', -1.234)
    assert attribute.value_type == 'number'

def test_etmAttributesAttribute_booleanValueTypeRecognized():
    attribute = _replace_value_and_create_attribute('value', True)
    assert attribute.value_type == 'boolean'

def test_etmAttributesAttribute_floatStringValueTypeRecognized():
    attribute = _replace_value_and_create_attribute('value', '-1.234')
    assert attribute.value_type == 'number_string'

def test_etmAttributesAttribute_floatStringHasWarning():
    attribute = _replace_value_and_create_attribute('value', '-1.234')
    assert attribute.issue_handler.has_warnings()

def test_etmAttributesAttribute_booleanStringValueTypeRecognized():
    attribute = _replace_value_and_create_attribute('value', 'TRUE')
    assert attribute.value_type == 'boolean_string'

def test_etmAttributesAttribute_booleanStringHasWarning():
    attribute = _replace_value_and_create_attribute('value', 'TRUE')
    assert attribute.issue_handler.has_warnings()

if __name__ == '__main__':
    os.system(f'pytest {__file__}')
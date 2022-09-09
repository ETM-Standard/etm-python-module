import os, sys
import pytest, copy

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
import etm_reader
from standard_modules import standard_module_base

VALID_METADATA_DICT = {
    "name": "My Cool NFT",
    "description": "A very cool NFT.",
    "image": "https://coolnfts.com/preview.mp4",
    "metadata_standard": "ETM_v1.0.0",
    "extensions": []
}

def test_metadata_standardName_nameIsValid():
    metadata_dict = {'metadata_standard': 'ETM_v1.0.0'}
    assert etm_reader.is_etm(metadata_dict)

def test_metadata_standardName_isNotEtm():
    metadata_dict = {'metadata_standard': 'OTHER_EXTENSIBLE_v1.0.0'}
    assert not etm_reader.is_etm(metadata_dict)

def test_metadata_standardName_versionFormattedWrong():
    has_succeeded = False
    has_succeeded = has_succeeded or etm_reader.is_etm({'metadata_standard': 'ETM_1.0.0'}) #missing 'v'
    has_succeeded = has_succeeded or etm_reader.is_etm({'metadata_standard': 'ETM_v1.0'}) #too few digits
    has_succeeded = has_succeeded or etm_reader.is_etm({'metadata_standard': 'ETM_v1.0.0.0'}) #too many digits
    has_succeeded = has_succeeded or etm_reader.is_etm({'metadata_standard': 'ETM_vX.0.0'}) #non-numeric digit 1
    has_succeeded = has_succeeded or etm_reader.is_etm({'metadata_standard': 'ETM_v0.X.0'}) #non-numeric digit 2
    has_succeeded = has_succeeded or etm_reader.is_etm({'metadata_standard': 'ETM_v0.0.X'}) #non-numeric digit 3
    assert not has_succeeded

def test_etmExtensible_validMetadataHasNoErrorsOrWarnings():
    etm = etm_reader.read_metadata_dict(VALID_METADATA_DICT)
    assert not etm.issue_handler.has_errors() and not etm.issue_handler.has_warnings()

def test_etmExtensible_missingNameHasError():
    metadata_dict = copy.deepcopy(VALID_METADATA_DICT)
    del metadata_dict['name']
    etm = etm_reader.read_metadata_dict(metadata_dict)
    assert etm.issue_handler.has_errors()

def test_etmExtensible_missingDescriptionHasNoError():
    metadata_dict = copy.deepcopy(VALID_METADATA_DICT)
    del metadata_dict['description']
    etm = etm_reader.read_metadata_dict(metadata_dict)
    assert not etm.issue_handler.has_errors()

def test_etmExtensible_missingImageHasWarning():
    metadata_dict = copy.deepcopy(VALID_METADATA_DICT)
    del metadata_dict['image']
    etm = etm_reader.read_metadata_dict(metadata_dict)
    assert etm.issue_handler.has_warnings()

def test_etmExtensible_missingMetadataStandardHasError():
    metadata_dict = copy.deepcopy(VALID_METADATA_DICT)
    del metadata_dict['metadata_standard']
    etm = etm_reader.read_metadata_dict(metadata_dict)
    assert etm.issue_handler.has_errors()

def test_etmExtensible_metadata_standardFormattedWrong():
    metadata_dict = copy.deepcopy(VALID_METADATA_DICT)
    metadata_dict['metadata_standard'] = 'ETM_v...'
    etm = etm_reader.read_metadata_dict(metadata_dict)
    assert etm.issue_handler.has_errors()

def test_etmExtensible_missingExtensionsHasError():
    metadata_dict = copy.deepcopy(VALID_METADATA_DICT)
    del metadata_dict['extensions']
    etm = etm_reader.read_metadata_dict(metadata_dict)
    assert etm.issue_handler.has_errors()


if __name__ == '__main__':
    os.system(f'pytest {__file__}')
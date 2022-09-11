import os, sys
import pytest, copy

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
import etm_reader
from standard_modules import etm_multiasset_asset, etm_multiasset_file

VALID_METADATA_DICT = {
    "name": "My Cool NFT",
    "description": "A very cool NFT.",
    "image": "https://coolnfts.com/preview.mp4",
    "metadata_standard": "ETM_v1.0.0",
    "extensions": [ "ETM_MULTIASSET_v1.0.0" ],
    "assets": []
}

VALID_ASSET_DICT = {
    "name": "Glasses",
    "description": "An unassuming pair of glasses.",
    "media_type": "model",
    "files": []
}

VALID_FILE_DICT = {
    "name": "Glasses",
    "description": "An unassuming pair of glasses.",
    "url": "https://ipfs.io/bafybeigdyrzt5sfp7udm7hu76uh7y26nf3efuylqabf3oclgtqy55fbzdi",
    "file_type": "model/fbx"
}

# TOP LEVEL ---------------------------------------------------------------------------------------

def test_etmMultiasset_validMetadataHasNoErrorsOrWarnings():
    etm = etm_reader.read_metadata_dict(VALID_METADATA_DICT)
    assert not etm.issue_handler.has_errors() and not etm.issue_handler.has_warnings()

def test_etmMultiasset_missingAssetsHasError():
    metadata_dict = copy.deepcopy(VALID_METADATA_DICT)
    del metadata_dict['assets']
    etm = etm_reader.read_metadata_dict(metadata_dict)
    assert etm.issue_handler.has_errors()

# ASSET -------------------------------------------------------------------------------------------

def _create_test_asset(etm, dict=VALID_ASSET_DICT):
    asset = etm_multiasset_asset.Asset(etm).from_dict(dict, 'fallback_name', 'fallback_description')
    asset.add_file(etm_multiasset_file.File(asset).from_dict(VALID_FILE_DICT, 'fallback_name', 'fallback_description')) #add a file with a matching media_type to prevent errors
    return asset.validate()

def test_etmMultiassetAsset_validAssetHasNoErrorsOrWarnings():
    etm = etm_reader.read_metadata_dict(VALID_METADATA_DICT)
    asset = _create_test_asset(etm)
    assert not asset.issue_handler.has_errors() and not asset.issue_handler.has_warnings()

def _remove_valid_asset_dict_key_and_create_asset(key):
    etm = etm_reader.read_metadata_dict(VALID_METADATA_DICT)
    asset_dict = copy.deepcopy(VALID_ASSET_DICT)
    del asset_dict[key]
    asset = _create_test_asset(etm, dict=asset_dict)
    return asset

def test_etmMultiassetAsset_missingNameHasNoError():
    asset = _remove_valid_asset_dict_key_and_create_asset('name')
    assert not asset.issue_handler.has_errors()

def test_etmMultiassetAsset_missingNameFallsBack():
    asset = _remove_valid_asset_dict_key_and_create_asset('name')
    assert asset.name == 'fallback_name'

def test_etmMultiassetAsset_missingDescriptionHasNoError():
    asset = _remove_valid_asset_dict_key_and_create_asset('description')
    assert not asset.issue_handler.has_errors()

def test_etmMultiassetAsset_missingDescriptionFallsBack():
    asset = _remove_valid_asset_dict_key_and_create_asset('description')
    assert asset.description == 'fallback_description'

def test_etmMultiassetAsset_missingMediaTypeHasError():
    asset = _remove_valid_asset_dict_key_and_create_asset('media_type')
    assert asset.issue_handler.has_errors()

def test_etmMultiassetAsset_missingFilesHasError():
    asset = _remove_valid_asset_dict_key_and_create_asset('files')
    assert asset.issue_handler.has_errors()

def test_etmMultiassetAsset_noValidFileMediaTypeHasError():
    etm = etm_reader.read_metadata_dict(VALID_METADATA_DICT)
    asset_dict = copy.deepcopy(VALID_ASSET_DICT)
    asset = _create_test_asset(etm, dict=asset_dict)
    asset.files[0]._set_file_type('image/png')
    asset.validate()
    assert asset.issue_handler.has_errors()

# FILE --------------------------------------------------------------------------------------------

def _create_test_file(asset, dict=VALID_FILE_DICT):
    return etm_multiasset_file.File(asset).from_dict(dict, 'fallback_name', 'fallback_description').validate()

def test_etmMultiassetFile_validFileHasNoErrorsOrWarnings():
    etm = etm_reader.read_metadata_dict(VALID_METADATA_DICT)
    asset = _create_test_asset(etm)
    file = _create_test_file(asset)
    assert not file.issue_handler.has_errors()

def _remove_valid_file_dict_key_and_create_file(key):
    etm = etm_reader.read_metadata_dict(VALID_METADATA_DICT)
    asset = _create_test_asset(etm)
    file_dict = copy.deepcopy(VALID_FILE_DICT)
    del file_dict[key]
    file = _create_test_file(asset, dict=file_dict)
    return file

def test_etmMultiassetFile_missingNameHasNoError():
    file = _remove_valid_file_dict_key_and_create_file('name')
    assert not file.issue_handler.has_errors()

def test_etmMultiassetFile_missingNameFallsBack():
    file = _remove_valid_file_dict_key_and_create_file('name')
    assert file.name == 'fallback_name'

def test_etmMultiassetFile_missingDescriptionHasNoError():
    file = _remove_valid_file_dict_key_and_create_file('description')
    assert not file.issue_handler.has_errors()

def test_etmMultiassetFile_missingDescriptionFallsBack():
    file = _remove_valid_file_dict_key_and_create_file('description')
    assert file.description == 'fallback_description'

def test_etmMultiassetFile_missingUrlHasError():
    file = _remove_valid_file_dict_key_and_create_file('url')
    assert file.issue_handler.has_errors()

def test_etmMultiassetFile_missingFileTypeHasError():
    file = _remove_valid_file_dict_key_and_create_file('file_type')
    assert file.issue_handler.has_errors()

def _set_valid_file_dict_key_and_create_file(key, value):
    etm = etm_reader.read_metadata_dict(VALID_METADATA_DICT)
    asset = _create_test_asset(etm)
    file_dict = copy.deepcopy(VALID_FILE_DICT)
    file_dict[key] = value
    file = _create_test_file(asset, dict=file_dict)
    return file

def test_etmMultiassetFile_file_typeFormattedWrongHasError():
    has_succeeded = False
    has_succeeded = has_succeeded or not _set_valid_file_dict_key_and_create_file('file_type', 'invalid').issue_handler.has_errors() #too few parts
    has_succeeded = has_succeeded or not _set_valid_file_dict_key_and_create_file('file_type', 'invalid/invalid/invalid').issue_handler.has_errors() #too many parts
    assert not has_succeeded

def test_etmMultiassetFile_file_typeWithInvalidMediaTypeHasError():
    file = _set_valid_file_dict_key_and_create_file('file_type', 'invalid/fbx')
    assert file.issue_handler.has_errors()

def test_etmMultiassetFile_file_typeWithInvalidFileExtensionHasError():
    file = _set_valid_file_dict_key_and_create_file('file_type', 'model/.fbx')
    assert file.issue_handler.has_errors()

if __name__ == '__main__':
    os.system(f'pytest {__file__}')
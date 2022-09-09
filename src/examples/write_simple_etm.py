import os, sys
from example_common import reset_outputs, get_output_filepath, OUTPUT_DIRPATH

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from etm_writer import write_metadata_to_file

from standard_modules.etm import ETM_v1_0_0

from standard_modules.etm_multiasset import ETM_MULTIASSET_v1_0_0
from standard_modules.etm_multiasset_asset import Asset
from standard_modules.etm_multiasset_file import File

'''
This example shows how to build a single, simple metadata.json that follows the minimum
implementation of the ETM standard using the ETM_MULTIASSET extension.

Optional fields are commented out below.
'''

if __name__ == '__main__':
    reset_outputs()

    etm = ETM_v1_0_0()
    etm.from_values(
        name='My NFT',
        #description='I am describing',
        #image='https://blah'
        )
    
    etm_multiasset = ETM_MULTIASSET_v1_0_0(etm).from_values()
    etm.extend(etm_multiasset)

    asset = Asset(etm_multiasset).from_values(
        #name='The first asset',
        #description='The description of the first asset',
        media_type='model',
        #asset_type='avatar'
        )
    etm_multiasset.add_asset(asset)

    file = File(asset).from_values(
        #name='The first file of the first asset',
        #description='The description of the first file of the first asset',
        url='https://blah',
        file_type='model/fbx',
    )
    asset.add_file(file)

    write_metadata_to_file(etm, get_output_filepath())

    print(f'Wrote metadata file to {OUTPUT_DIRPATH}\n')
    


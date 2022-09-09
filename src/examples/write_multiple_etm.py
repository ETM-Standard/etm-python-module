import os, sys
from example_common import reset_outputs, get_output_filepath, OUTPUT_DIRPATH

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from etm_writer import write_metadata_to_file

from standard_modules.etm import ETM_v1_0_0

from standard_modules.etm_multiasset import ETM_MULTIASSET_v1_0_0
from standard_modules.etm_multiasset_asset import Asset
from standard_modules.etm_multiasset_file import File

'''
This example shows how to build a multiple metadata.json files for a collection of NFTs.

This is also an example of an NFT based around a single asset which is represented in
multiple forms of media (model, video, and image).
'''

NUM_METADATA = 10

if __name__ == '__main__':
    reset_outputs()

    for i in range(1, NUM_METADATA+1):

        etm = ETM_v1_0_0()
        etm.from_values(
            name=f'Legendary Pistol {i}',
            description=f'One of {NUM_METADATA} legendary pistols created by the master gunsmith on a remote island in the metaverse.',
            image=f'http://nifty-island-pistol-drop-public.s3-website.us-east-2.amazonaws.com/{i}' #TODO
            )
        
        etm_multiasset = ETM_MULTIASSET_v1_0_0(etm).from_values()
        etm.extend(etm_multiasset)

        asset = Asset(etm_multiasset).from_values(
            media_type='model',
            asset_type='pistol'
            )
        etm_multiasset.add_asset(asset)

        file = File(asset).from_values(
            name=f'Legendary Pistol {i} Model',
            url=f'http://nifty-island-pistol-drop-public.s3-website.us-east-2.amazonaws.com/{i}/model', #TODO
            file_type='model/fbx',
        )
        asset.add_file(file)

        file = File(asset).from_values(
            name=f'Legendary Pistol {i} Video',
            url=f'http://nifty-island-pistol-drop-public.s3-website.us-east-2.amazonaws.com/{i}/video', #TODO
            file_type='video/mp4',
        )
        asset.add_file(file)

        file = File(asset).from_values(
            name=f'Legendary Pistol {i} Image',
            url=f'http://nifty-island-pistol-drop-public.s3-website.us-east-2.amazonaws.com/{i}/image', #TODO
            file_type='image/png',
        )
        asset.add_file(file)

        write_metadata_to_file(etm, get_output_filepath(i))
    
    print(f'Wrote {NUM_METADATA} metadata files to {OUTPUT_DIRPATH}\n')
    


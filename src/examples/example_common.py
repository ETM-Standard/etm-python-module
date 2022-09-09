import os, shutil

METADATA_FILE_EXTENSION = 'json'

INPUT_DIRNAME = 'inputs'
INPUT_DIRPATH = os.path.join(os.path.dirname(__file__), INPUT_DIRNAME)

def get_input_filepath(filename): return os.path.join(INPUT_DIRPATH, f'{filename}.{METADATA_FILE_EXTENSION}')

OUTPUT_DIRNAME = 'outputs'
OUTPUT_DIRPATH = os.path.join(os.path.dirname(__file__), OUTPUT_DIRNAME)

OUTPUT_FILE_BASENAME = 'metadata'

def get_output_filename(index=None): return f'{OUTPUT_FILE_BASENAME}{index if index != None else ""}.{METADATA_FILE_EXTENSION}'
def get_output_filepath(index=None): return os.path.join(OUTPUT_DIRPATH, get_output_filename(index))

def reset_dir(dirpath):
    if os.path.exists(dirpath): shutil.rmtree(dirpath)
    os.mkdir(dirpath)

def reset_outputs():
    reset_dir(OUTPUT_DIRPATH)
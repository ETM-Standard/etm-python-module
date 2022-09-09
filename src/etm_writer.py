import json

def write_metadata_to_file(etm, filepath):
    with open(filepath, 'w') as f:
        json.dump(etm.to_dict(), f, indent=4)



if __name__ == '__main__':
    pass
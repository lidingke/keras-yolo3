import os

def get_id(path):
    assert isinstance(path,str)
    return os.path.basename(path.strip()).split('.')[0]
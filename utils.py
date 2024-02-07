import os

def get_files(target_dir: str) -> list:
    '''
    Get all files in the target directory
    '''
    files = []
    for root, dirs, filenames in os.walk(target_dir):
        for file in filenames:
            files.append(file)
    return files


def get_py_files(target_dir: str) -> list:
    '''
    Get all python files in the target directory
    '''
    files = get_files(target_dir)
    py_files = [file for file in files if file.endswith('.py')]
    return py_files

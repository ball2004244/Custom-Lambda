from typing import List
import os

'''
This file contains all the utility functions used in the app
'''


def get_files(target_dir: str) -> List[str]:
    '''
    Get all files in the target directory
    '''
    files = []
    for root, dirs, filenames in os.walk(target_dir):
        for file in filenames:
            files.append(file)
    return files


def get_py_files(target_dir: str) -> List[str]:
    '''
    Get all python files in the target directory
    '''
    files = get_files(target_dir)
    py_files = [file for file in files if file.endswith('.py')]
    return py_files


def create_dir(target_dir: str) -> None:
    '''
    Create a directory if it does not exist
    '''
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)


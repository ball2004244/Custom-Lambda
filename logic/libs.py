from typing import List
import os

'''
This file handles all the library management in the virtual environment
'''

def install_libs(libs: List[str]) -> None:
    '''
    Install a list of libraries to the virtual environment
    '''
    # Check if the library is already installed
    installed_libs = get_libs()
    libs_to_install = []

    # Iterate over the libraries to extract non-existing ones
    for lib in libs:
        if any(lib in installed_lib for installed_lib in installed_libs):
            continue

        # If not yet installed, then install it
        libs_to_install.append(lib)

    for lib in libs_to_install:
        os.system(f'pip install {lib}')


def get_libs() -> List[str]:
    '''
    Get all installed libraries in the virtual environment
    '''
    temp_file = 'temp-requirements.txt'
    os.system(f'pip freeze > {temp_file}')
    data = []
    with open(temp_file, 'r') as f:
        data = f.readlines()

    os.system(f'rm {temp_file}')
    return data
from typing import List
import os
import subprocess

'''
This file handles all the library management in the virtual environment
'''

def get_libs() -> List[str]:
    '''
    Get all installed libraries in the virtual environment
    '''
    result = subprocess.run(['pip', 'freeze'], stdout=subprocess.PIPE)
    installed_libs = result.stdout.decode('utf-8').split('\n')
    return [lib for lib in installed_libs if lib]  # Filter out empty strings

def install_libs(libs: List[str], req_file: str = 'cloud_requirements.txt') -> None:
    '''
    Install a list of libraries to the virtual environment
    '''
    # Check if the library is already installed
    installed_libs = get_libs()
    libs_to_install = []

    # Sort both lists
    libs.sort()
    installed_libs.sort()

    # Use two-pointer technique to find non-existing libraries
    i, j = 0, 0
    while i < len(libs) and j < len(installed_libs):
        if libs[i] < installed_libs[j]:
            libs_to_install.append(libs[i])
            i += 1
        elif libs[i] > installed_libs[j]:
            j += 1
        else:
            i += 1
            j += 1

    # Add remaining libraries that are not in installed_libs
    while i < len(libs):
        libs_to_install.append(libs[i])
        i += 1

    if libs_to_install:
        install_str = ' '.join(libs_to_install)
        os.system(f'pip install {install_str}')

    update_requirements(req_file)

def update_requirements(file_path: str) -> None:
    '''
    Update requirements.txt file with all installed libraries, instead of manually updating it
    '''
    os.system(f'pip freeze > {file_path}')

def install_on_startup(req_file: str = 'cloud_requirements.txt') -> None:
    '''
    Install all libraries in the cloud_requirements.txt file during startup
    '''

    # verify if the file exists
    if not os.path.exists(req_file):
        # raise Exception('cloud_requirements.txt file not found')
        print('cloud_requirements.txt file not found, start with default requirements')
        os.system(f'cp requirements.txt {req_file}')

    libs = []
    with open(req_file, 'r') as f:
        libs = [lib.strip() for lib in f.readlines()]
    install_libs(libs)

if __name__ == '__main__':
    print(get_libs())
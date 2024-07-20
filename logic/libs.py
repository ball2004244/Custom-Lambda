from typing import List
import os

'''
This file handles all the library management in the virtual environment
'''


def install_libs(libs: List[str], req_file: str = 'cloud_requirements.txt') -> None:
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

    install_str = ' '.join(libs_to_install)
    os.system(f'pip install {install_str}')

    update_requirements(req_file)


def get_libs(req_file: str = 'cloud_requirements.txt') -> List[str]:
    '''
    Get all installed libraries in the virtual environment, then save to requirements.txt
    '''
    # use popen without passing the file to pip freeze
    libs = os.popen('pip freeze').read()

    # save to requirements.txt
    update_requirements(req_file)

    return libs


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
        libs = f.readlines()
    install_libs(libs)


if __name__ == '__main__':
    print(get_libs())

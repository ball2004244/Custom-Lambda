from utils import get_py_files
from config import LINE_LIMIT, FUNC_DELIMITER
from typing import Union, List, Dict
from .signature import *
import subprocess
import sys
import os
import re
import pickle
import base64
import shutil
import inspect
import importlib.util

'''
This file accounts for all the logic in the application
'''


def split_func_content(func_content: str) -> Union[str, List[str], Union[str, None]]:
    '''
    Split function into name, params and return type
    '''
    # assume that the first line is the function signature
    # look like this: def hello(a: int, b: str) -> str:
    # or this: def hello(a, b):

    # Get the first line of the function content
    lines = func_content.split('\n')
    lines = [line.strip() for line in lines if line.strip()]
    first_line = lines[0]

    pattern = r'def (\w+)\((.*?)\)(?:\s*->\s*(\w+))?:'
    # Use regex to extract the function name and params
    match = re.match(pattern, first_line)

    if not match:
        return None

    func_name = match.group(1)
    params = match.group(2).split(',')
    params = [param.strip() for param in params]
    return_type = match.group(3) if match.group(3) else None

    return func_name, params, return_type


def func_exists(func_name: str, target_dir: str) -> bool:
    '''
    Check if a function exists in a python file
    '''
    funcs = get_funcs(target_dir)

    for val in list(funcs.values())[0]:
        if val['function'] == func_name:
            return True
    return False


def get_funcs(target_dir: str) -> Dict[str, List[str]]:
    '''
    Get all serverless functions from a python file
    '''
    funcs = {}
    py_files = get_py_files(target_dir)
    for file in py_files:
        with open(f'{target_dir}/{file}', 'r') as f:
            # ignore init file
            if file == '__init__.py':
                continue

            # add functions of each file to a dictionary
            out_list = []
            formatted_file = file.split('.')[0]
            func_lst = get_all_func_names_by_signature(
                target_dir, formatted_file)
            if func_lst is None:
                continue

            # get params for each function
            for func in func_lst:
                params = get_params_by_signature(
                    func, target_dir, formatted_file)
                if params is None:
                    continue

                out_list.append({
                    'function': func,
                    'params': params
                })

            # get rid of extension
            funcs[formatted_file] = out_list

    return funcs


def add_func(func_content: str, target_dir: str) -> Union[str, None]:
    '''
    Add a serverless function to a python file,
    return a target file name
    '''
    func_name, params, _ = split_func_content(func_content)
    funcs = get_funcs(target_dir)

    # If function already exists, return None
    if func_exists(func_name, target_dir):
        return None

    target_file = list(funcs.keys())[-1] if funcs else 0
    write_mode = 'a'
    file_path = f'{target_dir}/{target_file}.py'

    # If file doesnt exist or is too large, create a new one
    if not os.path.exists(file_path) or len(open(file_path).readlines()) + len(func_content.split('\n')) > LINE_LIMIT:
        target_file = target_file + 1 if target_file else 0
        write_mode = 'w'

    # Add the new function to the file
    file_path = f'{target_dir}/{target_file}.py'
    with open(file_path, write_mode) as f:
        f.write(start_signature(func_name, params))
        f.write(func_content)
        f.write(end_signature(func_name))

    return target_file


def invoke_func(func_name: str, params: list, target_dir: str, target_file: str) -> Dict[str, Union[int, str, int]]:
    '''
    Run a serverless function from a function store
    '''
    # Check if function exists
    if not func_exists(func_name, target_dir):
        return None

    # Define necessary file names and signatures
    invokee_file = 'invokee.py'
    template_file = 'invokee_template.py'
    return_signature = f'#function-return: {FUNC_DELIMITER}'

    # Reset the invokee file with the original content
    shutil.copyfile(template_file, invokee_file)

    # Add the key phrase to the invokee file
    add_key_to_invokee(invokee_file)

    # Import the function from the function store
    spec = importlib.util.spec_from_file_location(
        target_file, os.path.join(target_dir, f'{target_file}.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    func = getattr(module, func_name)

    # Rename function to 'func'
    src = inspect.getsource(func)
    src = src.replace(func_name, 'func')

    # Insert the function between the signatures in the invokee file
    insert_func_to_invokee(src, invokee_file)

    # Prepare the command, pass params as pickle through io stream
    encoded_params = base64.b64encode(pickle.dumps(params)).decode()
    command = [sys.executable, invokee_file, encoded_params]

    # Run the command and capture output
    process = subprocess.run(command, capture_output=True, text=True)

    # Extract the return value from the last line of stdout
    *stdout, return_value = process.stdout.split(return_signature)
    decoded_return_value = pickle.loads(
        base64.b64decode(return_value)) if return_value else None

    # Prepare the output
    output = {
        'return_value': decoded_return_value,
        'stdout': stdout,
        'stderr': process.stderr
    }

    return output


def modify_func(func_name: str, new_func: str, target_dir: str, target_file: str) -> Union[str, None]:
    '''
    Modify a serverless function in a python file,
    return a target file name
    '''
    if not func_exists(func_name, target_dir):
        return None

    # check for start and end of function
    start, end = locate_function(func_name, target_dir, target_file)

    if start is None or end is None:
        return None

    # open the file and write the new function to new location
    with open(f'{target_dir}/{target_file}.py', 'r+') as f:
        lines = f.readlines()
        # replace old content with new one
        # ignore the signature
        lines[start+1:end-1] = new_func.split('\n')

        # write the new content to the file
        f.seek(0)
        f.writelines(lines)
        f.truncate()

    return target_file


def delete_func(func_name: str, target_dir: str, target_file: str) -> Union[str, None]:
    '''
    Delete a serverless function from a python file,
    return a target file name
    '''
    if not func_exists(func_name, target_dir):
        return None

    # check for start and end of function

    start, end = locate_function(func_name, target_dir, target_file)
    if start is None or end is None:
        return None

    with open(f'{target_dir}/{target_file}.py', 'r+') as f:
        lines = f.readlines()
        # delete the function and signature
        del lines[start:end]

        # write the new content to the file
        f.seek(0)
        f.writelines(lines)
        f.truncate()

    return target_file


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


if __name__ == '__main__':
    # test split func
    func_content = """
        def hello(a, b):
            c = a + b / 2
            return c
        """

    print(split_func_content(func_content))

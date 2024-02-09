from utils import get_py_files
from typing import Union, List, Dict
from config import FUNC_DELIMITER
import importlib.util
import traceback
import io
import sys
import os

'''
This file accounts for all the logic in the application
'''


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
            lines = f.readlines()
            func_lst = []
            for line in lines:
                if not line.strip():  # check if line is empty
                    continue

                if not line.strip().startswith('def '):  # check if line is not a function
                    continue

                func_name = line.split('def ')[1].split('(')[0]
                func_lst.append(func_name)

            # get rid of extension
            funcs[str(file).split('.')[0]] = func_lst

    return funcs


def add_func(func_name: str, new_func: str, target_dir: str) -> Union[str, None]:
    '''
    Add a serverless function to a python file,
    return a target file name
    '''
    # check if function exists
    funcs = get_funcs(target_dir)
    if func_name in list(funcs.values())[0]:
        return None

    # otherwise, get latest file name from last key in funcs
    target_file = list(funcs.keys())[-1] if funcs else 0
    LINE_LIMIT = 10000
    write_mode = 'a'

    # check if the file have enough empty lines for new function
    new_func_lines = len(new_func.split('\n'))
    with open(f'{target_dir}/{target_file}.py', 'r') as f:
        lines = f.readlines()
        if len(lines) + new_func_lines > LINE_LIMIT:
            target_file = int(target_file) + 1
            write_mode = 'w'

    # add the new function to the file
    with open(f'{target_dir}/{target_file}.py', write_mode) as f:
        f.write(f'#start-function: {func_name} with {FUNC_DELIMITER}\n')
        f.write(new_func)
        f.write(f'\n#end-function: {func_name} with {FUNC_DELIMITER}\n')

    return target_file


def invoke_func(func_name: str, params: list, target_dir: str, target_file: str) -> Dict[str, Union[str, None]]:
    '''
    Run a serverless function from a function store
    '''

    # check if function exists
    funcs = get_funcs(target_dir)
    if func_name not in list(funcs.values())[0]:
        return None

    # load the target file
    spec = importlib.util.spec_from_file_location(
        target_file, f'{target_dir}/{target_file}.py')
    func_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(func_module)

    # check if function exists in the module
    if not hasattr(func_module, func_name):
        return None

    # Invoke the function and capture print() output and exceptions
    func = getattr(func_module, func_name)
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    sys.stdout = stdout_buffer = io.StringIO()
    sys.stderr = stderr_buffer = io.StringIO()
    try:
        result = func(*params)
    except Exception:
        traceback.print_exc()
    finally:
        sys.stdout = original_stdout
        sys.stderr = original_stderr
    print_output = stdout_buffer.getvalue()
    error_output = stderr_buffer.getvalue()

    output = {
        'return_result': result,
        'stdout': print_output,
        'stderr': error_output
    }
    return output


def modify_func(func_name: str, new_func: str, target_dir: str, target_file: str) -> Union[str, None]:
    '''
    Modify a serverless function in a python file,
    return a target file name
    '''
    # check if function exists
    funcs = get_funcs(target_dir)
    if func_name not in list(funcs.values())[0]:
        return None

    # check for start and end of function
    start = None
    end = None
    lines = None
    with open(f'{target_dir}/{target_file}.py', 'rw') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if f'#start-function: {func_name} with {FUNC_DELIMITER}' in line:
                start = i
            if f'#end-function: {func_name} with {FUNC_DELIMITER}' in line:
                end = i

    if start is None or end is None:
        return None

    # replace old content with new one
    lines[start+1:end] = new_func.split('\n')
    return target_file


def delete_func(func_name: str, target_dir: str, target_file: str) -> Union[str, None]:
    '''
    Delete a serverless function from a python file,
    return a target file name
    '''
    # check if function exists
    funcs = get_funcs(target_dir)
    if func_name not in list(funcs.values())[0]:
        return None

    # check for start and end of function
    start = None
    end = None
    lines = None
    with open(f'{target_dir}/{target_file}.py', 'rw') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if f'#start-function: {func_name} with {FUNC_DELIMITER}' in line:
                start = i
            if f'#end-function: {func_name} with {FUNC_DELIMITER}' in line:
                end = i

    if start is None or end is None:
        return None

    # delete the function
    del lines[start:end+1]
    return target_file


def install_libs(libs: List[str]) -> None:
    '''
    Install a list of libraries to the virtual environment
    '''
    for lib in libs:
        os.system(f'pip install {lib}')


def get_libs() -> List[str]:
    '''
    Get all installed libraries in the virtual environment
    '''
    os.system('pip freeze > requirements.txt')
    with open('requirements.txt', 'r') as f:
        return f.readlines()


if __name__ == '__main__':
    # test invoke_func
    print(invoke_func('hello', [], 'functions_store', '0'))

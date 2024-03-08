from utils import get_py_files, create_py_file
from config import LINE_LIMIT, TIME_LIMIT, MEMORY_LIMIT, MAX_UPLOAD_SIZE
from typing import Union, List, Dict, Any
from .signature import *
from .invoke import invoke_with_limit, prepare_invokee
import os
import re
import pickle
import base64

'''
This file contains the logic to modify and manage invokee/invoker functions
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

    if not funcs:
        return False

    for val in list(funcs.values())[0]:
        if val['function'] == func_name:
            return True
    return False


def get_funcs(target_dir: str, author: str='admin', password: str='admin') -> Union[Dict[str, List[str]], None]:
    '''
    Get all serverless functions from a python file
    Permission: ADMIN, NORMAL USER
    '''
    # Mock data for admin
    admin_username = 'admin'
    admin_pass = 'admin'
    

    funcs = {}
    py_files = get_py_files(target_dir)
    # handle when no store exists
    if not py_files:
        create_py_file(target_dir, '0.py')
        return None
    
    for file in py_files:
        with open(f'{target_dir}/{file}', 'r') as f:
            # ignore init file
            if file == '__init__.py':
                continue

            # add functions of each file to a dictionary
            out_list = []
            funcc_list = None
            formatted_file = file.split('.')[0]
            
            # either return all funcs of 1 user or return all funcs in the system
            if author == admin_username and password == admin_pass:
                func_lst = get_all_func_names_by_signature(
                    target_dir, formatted_file)
            else:
                func_lst = get_func_names_by_author(
                    target_dir, formatted_file, author, password)
                

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

    return funcs if funcs else None


def add_func(func_content: str, target_dir: str, author: str='admin', password: str='admin') -> Union[str, None]:
    '''
    Add a serverless function to a python file,
    return a target file name
    '''

    func_name, params, _ = split_func_content(func_content)
    funcs = get_funcs(target_dir)

    # Not allow same function name
    #TODO: Work out so different user can have same function name
    # if func_exists(func_name, target_dir):
    #     return None

    # Reject overly long functions
    if len(func_content.split('\n')) > LINE_LIMIT:
        return None

    # Reject overly large functions
    if len(func_content.encode('utf-8')) > MAX_UPLOAD_SIZE:
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
        f.write(get_start_signature(func_name, params))
        f.write(get_author_signature(author, password))
        f.write(func_content)
        f.write(get_end_signature(func_name))

    return target_file


def invoke_func(func_name: str, params: list, target_dir: str, target_file: str, author: str='admin', password: str='admin') -> Dict[str, Any]:
    '''
    Run a serverless function from a function store
    '''
    if not func_exists(func_name, target_dir):
        return None

    invokee_file = 'invokee.py'
    template_file = 'invokee_template.py'
    return_signature = get_return_signature()
    user_auth = verify_author(author, password, func_name, target_dir, target_file)

    # User not found
    if user_auth is None:
        return None
    
    # Wrong password
    if not user_auth:
        return None

    prepare_invokee(func_name, target_dir, target_file,
                    invokee_file, template_file)


    output = invoke_with_limit(
        invokee_file, params, TIME_LIMIT, MEMORY_LIMIT)


    stdout, return_value = output['stdout'].split(return_signature)
    decoded_return_value = pickle.loads(
        base64.b64decode(return_value)) if return_value else None

    output = {
        'return_value': decoded_return_value,
        'stdout': stdout,
        'stderr': output['stderr'],
    }

    return output


def modify_func(func_name: str, new_func: str, target_dir: str, target_file: str) -> Union[str, None]:
    '''
    Modify a serverless function in a python file,
    return a target file name
    '''
    if not func_exists(func_name, target_dir):
        return None

    start, end = locate_function(func_name, target_dir, target_file)

    if start is None or end is None:
        return None

    # replace old content with new one
    with open(f'{target_dir}/{target_file}.py', 'r+') as f:
        lines = f.readlines()
        lines[start+1:end-1] = new_func.split('\n')
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

    # delet function and signatures
    with open(f'{target_dir}/{target_file}.py', 'r+') as f:
        lines = f.readlines()
        del lines[start:end]
        f.seek(0)
        f.writelines(lines)
        f.truncate()

    return target_file


if __name__ == '__main__':
    # test split func
    func_content = """
        def hello(a, b):
            c = a + b / 2
            return c
        """

    print(split_func_content(func_content))

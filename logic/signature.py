from config import FUNC_DELIMITER
from typing import List, Tuple, Union, Literal
from .auth import hash_password, check_password
'''
This file accounts for function signature verification.
Signature is used to distinguish between different functions in the same file,
or to divide a function into different parts
'''


def get_return_signature() -> str:
    '''
    Get the return signature of a function
    Return signature separate stdout from function return values
    '''
    return f'#function-return: {FUNC_DELIMITER}'


def get_start_signature(func_name: str, params: List[str]) -> str:
    '''
    Return a start signature for a saved function
    '''
    return f'#start-function: {FUNC_DELIMITER}, function: {func_name}, params: {params}\n'


def get_end_signature(func_name: str) -> str:
    '''
    Return an end signature for a saved function
    '''
    return f'#end-function: {FUNC_DELIMITER}, function: {func_name}\n'


def get_author_signature(name: str, password: str) -> str:
    '''
    Add author name and password of an invokee function
    '''
    return f'#author: {name}, creds: {hash_password(password)}\n'


def locate_function(func_name: str, target_dir: str, target_file: str) -> Union[Tuple[int, int], None]:
    '''
    Locate the start & end of a function in a python file
    '''
    start = None
    end = None
    with open(f'{target_dir}/{target_file}.py', 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if f'#start-function: {FUNC_DELIMITER}, function: {func_name}' in line:
                start = i
            if f'#end-function: {FUNC_DELIMITER}, function: {func_name}' in line:
                end = i + 1  # include the end line

    if start is None or end is None:
        return None, None

    return start, end


def get_all_func_names_by_signature(target_dir: str, target_file: str) -> Union[List[str], None]:
    '''
    Get all func names from a python file by signature
    '''
    func_names = []
    with open(f'{target_dir}/{target_file}.py', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if f'#start-function: {FUNC_DELIMITER}, function: ' in line:
                func_name = line.split(',')[1].split('function: ')[1]
                func_names.append(func_name)

    if len(func_names) == 0:
        return None

    return func_names

def get_func_names_by_author(target_dir: str, target_file: str, author: str, password: str) -> Union[List[str], None]:
    '''
    Get all func names from 1 author in current py file
    Required user to have valid auth
    '''
    func_names = set()
    with open(f'{target_dir}/{target_file}.py', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if f'#start-function: {FUNC_DELIMITER}, function: ' in line:
                func_name = line.split(',')[1].split('function: ')[1]
                verified_author = verify_author(author, password, func_name, target_dir, target_file)
                if verified_author is None:
                    return None
                
                if not verified_author:
                    continue

                func_names.add(func_name)

    if len(func_names) == 0:
        return None

    return list(func_names)
    

def get_params_by_signature(func_name: str, target_dir: str, target_file: str) -> Union[List[str], None]:
    '''
    Get all params from a saved function using signature
    '''

    params = []
    with open(f'{target_dir}/{target_file}.py', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if f'#start-function: {FUNC_DELIMITER}, function: {func_name}' in line:
                params = eval(line.split('params: ')[1])
                break

    if len(params) == 0:
        return None

    return params


def add_signature_to_invokee(invokee: str) -> Union[str, None]:
    '''
    Replace default key phrase in invokee file with secret key phrase
    '''
    with open(invokee, 'r+') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            # Replace start key phrase
            if '#start-function: KEYPHRASE' in line:
                lines[i] = f'#start-function: {FUNC_DELIMITER}\n'
            # Replace end key phrase
            if '#end-function: KEYPHRASE' in line:
                lines[i] = f'#end-function: {FUNC_DELIMITER}\n'
                break
        f.seek(0)
        f.writelines(lines)
        f.truncate()

    return invokee


def insert_func_to_invokee(src: str, invokee: str) -> Union[str, None]:
    '''
    Insert a function to invokee file
    '''
    start_signature = f'#start-function: {FUNC_DELIMITER}'
    end_signature = f'#end-function: {FUNC_DELIMITER}'

    with open(invokee, 'r+') as file:
        lines = file.readlines()

        # Locate the start and end signature
        start_index = next(i for i, line in enumerate(lines)
                           if start_signature in line)
        end_index = next(i for i, line in enumerate(
            lines) if end_signature in line)

        # Write the new content to the file
        file.seek(0)
        file.writelines(lines[:start_index + 1])
        file.write(src)  # Insert the function
        file.writelines(lines[end_index:])
        file.truncate()
    return invokee


def verify_author(author: str, password: str, func_name: str, target_dir: str, target_file: str) -> Union[bool, None]:
    '''
    Check if the author and password are correct for a specific function
    True - User is authorized with the correct function
    False - User is not authorized with the correct function
    None - User is not exists
    '''

    i = 0
    lines = []
    with open(f'{target_dir}/{target_file}.py', 'r') as f:
        lines = f.readlines()

    for i in range(1, len(lines)):
        # Check if the author exists
        if f'#author: {author}, creds: ' in lines[i]:
            hashed_password = lines[i].split('creds: ')[1].strip()

            # Check if the function is correct
            if f'#start-function: {FUNC_DELIMITER}, function: {func_name}' in lines[i-1]:
                return check_password(password, hashed_password)
    return None

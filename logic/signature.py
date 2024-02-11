from config import FUNC_DELIMITER
from typing import List, Tuple, Union
'''
This file accounts for function signature verification
'''


def start_signature(func_name: str, params: List[str]) -> str:
    '''
    Return a start signature for a function
    '''
    return f'#start-function: {FUNC_DELIMITER}, function: {func_name}, params: {params}\n'


def end_signature(func_name: str) -> str:
    '''
    Return an end signature for a function
    '''
    return f'#end-function: {FUNC_DELIMITER}, function: {func_name}\n'


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


def get_params_by_signature(func_name: str, target_dir: str, target_file: str) -> Union[List[str], None]:
    '''
    Get all params from a function by signature and function name
    '''

    params = []
    with open(f'{target_dir}/{target_file}.py', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if f'#start-function: {FUNC_DELIMITER}, function: {func_name}' in line:
                params = line.split(',')[2].split('params: ')[1].strip().split(',')
                break

    if len(params) == 0:
        return None

    return params

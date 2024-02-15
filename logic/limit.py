import os
import psutil
import time
from typing import Any, Callable, Union

'''
This file add some limits to a cloud function to avoid infinite loops or memory leaks
#TODO: Let the invokee function to run in an independent process for easier memory & time tracking
#! This is a work in progress
'''


def invoke_limit(time_limit: int = 60, memory_limit: int = 50000000) -> Callable:
    '''
    A decorator to limit some aspects during function running
    '''
    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Union[Any, None]:
            # track time here
            start_time = time.perf_counter()
            # track memory here
            start_mem = memory_usage()

            result = func(*args, **kwargs)

            check_time_limit(start_time, time_limit)
            check_memory_limit(start_mem, memory_limit)

            return result
        return wrapper
    return decorator


def check_time_limit(start_time: float, limit: int = 60) -> None:
    '''
    A function to limit the execution time of a process
    If the function runs for longer than the time limit, a TimeoutError is raised
    '''
    if time.perf_counter() - start_time > limit:
        raise TimeoutError(
            f"Function exceeded the time limit of {limit} seconds")


def check_memory_limit(start_mem: int, limit: int = 50000000) -> None:
    '''
    A function to limit the memory usage of a process
    If the function exceeds the memory limit, a MemoryError is raised
    '''
    if memory_usage() - start_mem > limit:
        raise MemoryError(
            f"Function exceeded the memory limit of {limit} bytes")


def memory_usage():
    '''
    A function to get the current memory usage
    '''
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss

# Test for 5s time limit and 50MB memory limit


@invoke_limit(time_limit=5, memory_limit=50000000)
def test_function():
    # a function to test the decorator
    a = [i for i in range(1000000)]
    for i in range(1000000):
        for j in range(1000000):

            print(a[i])
    return a


if __name__ == "__main__":
    print('Running test function...')
    test_function()
    print('Test function ran successfully')

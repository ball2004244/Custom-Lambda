import time
import psutil
import subprocess
import pickle
import base64
import importlib.util
import inspect
import os
import shutil
from signature import add_signature_to_invokee, insert_func_to_invokee
from typing import Dict, Union
from threading import Thread
from queue import Queue, Empty
from config import MAX_STDOUT

'''
This file contains the low-level logic of invoking a function
'''


def prepare_invokee(func_name: str, funcstore_dir: str, funcstore_file: str, invokee_file: str = 'invokee.py', template: str = 'invokee_template.py') -> Union[str, None]:
    '''
    This function do minimal modification to the invokee file
    so it will be ready for next call
    '''
    try:
        # * RESET invokee file
        shutil.copyfile(template, invokee_file)
        add_signature_to_invokee(invokee_file)

        # * PREPARE function to be invoked
        # Get the function from funcstore
        spec = importlib.util.spec_from_file_location(
            funcstore_file, os.path.join(funcstore_dir, f'{funcstore_file}.py'))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        func = getattr(module, func_name)

        # Rename function
        src = inspect.getsource(func)
        src = src.replace(func_name, 'func')

        # * PASS function to invokee file
        insert_func_to_invokee(src, invokee_file)

        return 'Function prepared successfully'
    except Exception:
        return None


def invoke_with_limit(invokee: str, params: str, time_limit: int = 60, memory_limit: int = 1000000000) -> Dict[str, str]:
    '''
    Run invokee with some limits on top
    Current check for time and memory limits
    '''
    output = {
        'status': 'error',
        'message': 'Function did not run successfully',
        'stdout': '',
        'stderr': ''
    }

    try:
        encoded_params = base64.b64encode(pickle.dumps(params)).decode()
        cmd = ['python3', invokee, encoded_params]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, text=True)

        # Define threads to store stdout and stderr
        stdout_queue = Queue()
        stderr_queue = Queue()
        stdout_thread = Thread(target=enqueue_output,
                               args=(process.stdout, stdout_queue, MAX_STDOUT))
        stderr_thread = Thread(target=enqueue_output,
                               args=(process.stderr, stderr_queue, MAX_STDOUT))
        stdout_thread.daemon = True
        stderr_thread.daemon = True

        # Start time and memory tracking
        start_time = time.perf_counter()
        start_mem = psutil.Process(process.pid).memory_info().rss

        # start stdout and stderr threads
        stdout_thread.start()
        stderr_thread.start()

        # last_print_time = start_time
        while process.poll() is None:
            if over_time_limit(start_time, time_limit):
                raise TimeoutError('Function exceeded the time limit')
            if over_mem_limit(process.pid, start_mem, memory_limit):
                raise MemoryError('Function exceeded the memory limit')

            # Print the dashboard every 2s
            # if time.perf_counter() - last_print_time > 2:
            #     print_dashboard(process.pid, start_time,
            #                     time_limit, memory_limit)
            #     last_print_time = time.perf_counter()

            # Store the output in a list

        output['status'] = 'success'
        output['message'] = 'Function ran successfully'
    except (TimeoutError, MemoryError) as Exception:
        process.terminate()
        output['message'] = str(Exception)

    except Exception as e:
        output['message'] = 'Unexpected error occurred'
        print('Unexpected error:', e)
    finally:
        output['stdout'] = get_queue_content(stdout_queue)
        output['stderr'] = get_queue_content(stderr_queue)

    return output


def over_time_limit(start_time: float, limit: int = 60) -> bool:
    '''
    A helper function to limit the execution time of a process
    If the function runs for longer than the time limit, a TimeoutError is raised
    '''
    return time.perf_counter() - start_time > limit


def over_mem_limit(pid: int, start_mem: int, limit: int = 50000000) -> bool:
    '''
    A helper function to limit the memory usage of a process
    If the function exceeds the memory limit, a MemoryError is raised
    '''
    return psutil.Process(pid).memory_info().rss - start_mem > limit


def enqueue_output(out: subprocess.Popen, queue: Queue, maxsize: int = MAX_STDOUT) -> None:
    '''
    A helper function to enqueue the output of a process.
    It will store stdout and stderr in a queue
    Auto delete the oldest item if the queue is full
    '''

    for line in iter(out.readline, b''):
        if line.strip():
            queue.put(line)
        if queue.qsize() > maxsize:
            queue.get()
    out.close()


def get_queue_content(queue: Queue, limit: int = MAX_STDOUT) -> str:
    '''
    A helper function to retrieve the output from a queue
    '''
    lst = []
    while True:
        try:
            lst.append(queue.get_nowait())
        except Empty:
            break
    return ''.join(lst)


def print_dashboard(pid: int, start_time: float, time_limit: int, memory_limit: int):
    '''
    A helper to print the current memory usage and execution time of a process
    '''
    current_mem = psutil.Process(pid).memory_info().rss
    current_time = time.perf_counter() - start_time

    # Convert to MB
    display_mem = current_mem / 1000000
    display_limit = memory_limit / 1000000

    print(f"PID: {pid}")
    print(f"Memory Usage: {display_mem:.2f}/{display_limit:.2f} MB")
    print(f"Execution Time: {current_time:.2f}/{time_limit} seconds")


if __name__ == "__main__":
    test_file = 'test.py'
    time_limit = 10  # seconds ~ 5 minutes
    memory_limit = 1000000000  # bytes ~ 1GB
    print('Running test function...')
    print(invoke_with_limit(test_file, time_limit, memory_limit))
    print('Finished running test function')

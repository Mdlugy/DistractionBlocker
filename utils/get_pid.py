from .windll32 import windll_32
from ctypes.wintypes import DWORD, HWND
from ctypes import POINTER, byref

get_window_thread_process_id = windll_32.GetWindowThreadProcessId
get_window_thread_process_id.argtypes = [HWND, POINTER(DWORD)]
get_window_thread_process_id.restype = DWORD

def get_pid_from_window(hwnd):
    # The process ID will be stored in this variable
    process_id = DWORD()
    
    # Call the function and get the thread ID
    thread_id = get_window_thread_process_id(HWND(hwnd), byref(process_id))
    
    # Return both the thread ID and the process ID
    return thread_id, process_id.value
from .windll32 import windll_32
from ctypes.wintypes import DWORD, HWND
from ctypes import POINTER, byref

GetWindowThreadProcessId = windll_32.GetWindowThreadProcessId
GetWindowThreadProcessId.argtypes = [HWND, POINTER(DWORD)]
GetWindowThreadProcessId.restype = DWORD

def getPidFromWindow(hwnd):
    # The process ID will be stored in this variable
    process_id = DWORD()
    
    # Call the function and get the thread ID
    thread_id = GetWindowThreadProcessId(HWND(hwnd), byref(process_id))
    
    # Return both the thread ID and the process ID
    return thread_id, process_id.value
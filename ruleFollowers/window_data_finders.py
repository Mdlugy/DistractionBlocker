from pywinauto.application import Application
from utils.windll32 import windll_32
from ctypes import create_unicode_buffer
from utils.get_pid import get_pid_from_window
import psutil

def get_text_from_window(hwnd):
    length = windll_32.GetWindowTextLengthW(hwnd)
    buf = create_unicode_buffer(length + 1)
    windll_32.GetWindowTextW(hwnd, buf, length + 1)
    if buf.value:
        return buf.value
    else:
        return None

def get_foreground_window_pid(hwnd):
    pid = get_pid_from_window(hwnd)
    # print(pid)
    return pid

def get_foregroud_window_path(hwnd):
    pid = get_foreground_window_pid(hwnd)
    active_window_path = psutil.Process(pid[1]).exe()
    return active_window_path
    
def get_foreground_window_title():
    return get_text_from_window(windll_32.GetForegroundWindow())

def get_explorer_path(hwnd):
    # Get the handle to the address bar
    addr_bar_hwnd = windll_32.FindWindowExW(hwnd, None, 'WorkerW', None)
    addr_bar_hwnd = windll_32.FindWindowExW(addr_bar_hwnd, None, 'ReBarWindow32', None)
    addr_bar_hwnd = windll_32.FindWindowExW(addr_bar_hwnd, None, 'Address Band Root', None)
    addr_bar_hwnd = windll_32.FindWindowExW(addr_bar_hwnd, None, 'msctls_progress32', None)
    addr_bar_hwnd = windll_32.FindWindowExW(addr_bar_hwnd, None, 'Breadcrumb Parent', None)
    addr_bar_hwnd = windll_32.FindWindowExW(addr_bar_hwnd, None, 'ToolbarWindow32', None)
    if addr_bar_hwnd:
        return get_text_from_window(addr_bar_hwnd)
    return None    

def get_hwnd():
    return windll_32.GetForegroundWindow()


# assume this is only ever called with an active chrome tid,pid tuple 
def get_chrome_adress(pid):
    app = Application(backend="uia").connect(process=pid[1], timeout=10)
    dlg = app.top_window()
    title = "Address and search bar"
    url = dlg.child_window(title=title, control_type="Edit").get_value()
    return url


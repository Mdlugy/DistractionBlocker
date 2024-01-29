import psutil
import pyKey
import time
from .window_data_finders import get_foreground_window_pid, get_hwnd

def kill_process_Agressive(pid):
    print("kill_process_Agressive")
    process = psutil.Process(pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()
    
def kill_window():
    pyKey.pressKey("CTRL")
    pyKey.pressKey("W")
    pyKey.releaseKey("CTRL")
    pyKey.releaseKey("W")

def kill_process_Chill():
    print("kill_process_Chill")
    pyKey.pressKey("ALT")
    pyKey.pressKey("F4")
    pyKey.releaseKey("ALT")
    pyKey.releaseKey("F4")

def kill (killType, hwnd, pid=None):
    if get_hwnd() != hwnd:
        return
    if killType=="exe":
        kill_process_Chill()
        time.sleep(1)
        if get_foreground_window_pid(hwnd) == pid:
            kill_process_Agressive(pid)
    else :
        kill_window()
    return
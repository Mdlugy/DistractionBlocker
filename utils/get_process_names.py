from ruleFollowers.window_data_finders import get_chrome_adress,get_text_from_window, get_foreground_window_pid, get_foregroud_window_path, get_foreground_window_title, get_explorer_path, get_hwnd
import time
def get_names():
    while True:
        hwnd = get_hwnd()
        title = get_foreground_window_title()
        path = get_foregroud_window_path(hwnd)
        print("title",title)
        print("path",path)
        if path =="C:\Windows\explorer.exe":
            print("explorer")
            explorerPath = get_explorer_path(hwnd)
            print(explorerPath)
        if path =="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe":
            pid = get_foreground_window_pid(hwnd)
            chromeadd=get_chrome_adress(pid)
            print(chromeadd)
        time.sleep(1)

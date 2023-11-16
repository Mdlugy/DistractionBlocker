from ruleFollowers.WindowDataFinders import getChromeAdress,getTextFromWindow, getForegroundWindowPid, getForegroudWindowPath, getForegroundWindowTitle, get_explorer_path, getHwnd
import time
def getNames():
    while True:
        hwnd = getHwnd()
        title = getForegroundWindowTitle()
        path = getForegroudWindowPath(hwnd)
        print("title",title)
        print("path",path)
        if path =="C:\Windows\explorer.exe":
            print("explorer")
            explorerPath = get_explorer_path(hwnd)
            print(explorerPath)
        if path =="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe":
            pid = getForegroundWindowPid(hwnd)
            chromeadd=getChromeAdress(pid)
            print(chromeadd)
        time.sleep(1)

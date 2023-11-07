from typing import Optional
import threading
import pyKey
import time 
import psutil
import win32process
import win32gui
import win32com
from .createMessage import warningMessage
from .exeBlocker import kill
import json
import os
from .WindowDataFinders import getTextFromWindow, getForegroundWindowPid, getForegroudWindowPath, getForegroundWindowTitle, get_explorer_path, getHwnd
def ReadBlackList():
    file_path = os.path.join("jsonFiles", 'blackList.json')
    absolute_file_path = os.path.abspath(file_path)

    if not os.path.exists(absolute_file_path):
        return None
    else:
        with open(absolute_file_path, 'r') as file:
            return json.load(file)
        
def StopRun(exitTime):
    now = datetime.now().strftime("%H:%M:%S")
    

def windowCloser(breakLeft=20):
    fiveMinuteWarning = False
    breakOverrideTime = None
    if not breakLeft==0:
        fiveMinuteWarning = True
        
        if (breakLeft>300):
            time.sleep(breakLeft-300)
            breakOverrideTime = 300
        else:
            breakOverrideTime = breakLeft
            
    BlockList = ReadBlackList()
        
    # Schedule = ReadSchedule()
    
    # today = datetime.now().strftime("%m:%d:%y")
    # if (Schedule["daysOff"].contains(today)):
    #     return 
    
    # weekday = datetime.now().strftime("%A")
    
    # exitTime = Schedule[weekday]["exitTime"]
    
    # startTime = Schedule[weekday]["startTime"]
    
    def warnKill(KillTime, killType, hwnd, pid = None):
        warningMessage(KillTime, killType, hwnd)
        time.sleep(KillTime-5)
        if getHwnd() != hwnd:
            return
        kill(killType, hwnd, pid)
    def justwarn(KillTime, killType, hwnd, pid = None):
        warningMessage(KillTime, killType, hwnd)
    while True:
        hwnd = getHwnd()
        title = getForegroundWindowTitle()
        path = getForegroudWindowPath(hwnd)
        print(title)
        print(path)
        for pathStart in BlockList["paths"]:
            pid = getForegroundWindowPid(hwnd)[-1]
            if path.startswith(pathStart):
                if fiveMinuteWarning==True:
                    warnKill(breakOverrideTime, "exe", hwnd, pid)
                else:
                    warnKill(10, "exe", hwnd, pid)
                break
               
        time.sleep(1)
                    

                    
#     if path == 'C:\Windows\explorer.exe':
#         hwnd = windll_32.GetForegroundWindow()
#         path = getTextFromWindow(get_explorer_path(hwnd))
#         print (path)
#         time.sleep(3)
#         continue
#     if type(title) == None:
#         time.sleep(3)
#         continue
#     if type(path) == None:
#         time.sleep(3)
#         continue
#     print(title)
#     print(path)
#     if ("Visual" in getForegroundWindowTitle()):
#         pid = getForegroundWindowPid()
#         print('here')
#         warningMessage(10)
#         print(pid)
#         # time.sleep(10)
#         # if getForegroundWindowPid() == pid:
#             # kill_process(pid[-1])
#     time.sleep(3)
# # import win32gui, win32con, win32process
# # from ctypes import windll
# # from time import sleep
# # sleep(5)
# # create a new tinkter window
# hwnd = int(eval(<toplevel>.wm_frame()))	# Get the window info from the window manager
# hwnd = int(eval(TestWindow.wm_frame())) # Get the window info from the window manager
# win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
# win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
# 
# exes to consider:
# LariLauncher



# p = psutil.Process(pid)
# p.terminate()
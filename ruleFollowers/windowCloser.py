from typing import Optional
from datetime import datetime,timedelta
import threading
import pyKey
import time 
import psutil
import win32process
import win32gui
import win32com
from .createMessage import warningMessage
from .exeBlocker import kill
from .WindowDataFinders import getTextFromWindow, getForegroundWindowPid, getForegroudWindowPath, getForegroundWindowTitle, get_explorer_path, getHwnd
from utils.JsonManipulators import ReadBlackList, ReadSchedule, removeBreak, removeDayOff, isBreak,ReadJSON,getList

def warnKill(KillTime, killType, hwnd, pid = None):
        warningMessage(KillTime, killType, hwnd)
        time.sleep(KillTime-5)
        if getHwnd() != hwnd:
            return
        kill(killType, hwnd, pid)

def stringChecker(blockedStrings, string, blockme):
        for blockedString in blockedStrings:
            if blockedString in string:
                return not blockme
        return blockme
        
def windowCloser():
    
    Schedule = ReadSchedule()
    breakLeft = Schedule["break"]
    fiveMinuteWarning = False
    breakOverrideTime = None
    if not breakLeft==0:
        fiveMinuteWarning = True
        if (breakLeft>300):
            time.sleep(breakLeft-300)
            breakOverrideTime = 300
        else:
            breakOverrideTime = breakLeft
        removeBreak(Schedule)
    timefromepoch = time.time()
    BlackList = ReadBlackList()
    specialCases = BlackList["specialCases"]
    
    
    today = datetime.now().strftime("%m/%d/%Y")
    print(today)
    for day in Schedule["DaysOff"]:
        if day == today:
            removeDayOff(Schedule)
            print("Today is a day off")
            return 
    
    weekday = datetime.now().strftime("%A")
    
    exitTime = Schedule[weekday]["end"]
    
    startTime = Schedule[weekday]["start"]
    
    # # get the current time
    now = datetime.now().strftime("%H:%M:%S")
    print (now)
    # # if the current time is less than the start time, sleep until the start time
    if now < startTime:
        print("Sleeping until start time")
        # sleep until the start time
        time.sleep((datetime.strptime(startTime, "%H:%M:%S") - datetime.strptime(now, "%H:%M:%S")).total_seconds())
    if now > exitTime:
        print("Sleeping until tomorrow")
        tomorrow = (datetime.today() + timedelta(days=1)).strftime('%A')
        # sleep until the start time of tomorrow
        time.sleep((datetime.strptime(Schedule[tomorrow]["start"], "%H:%M:%S") - datetime.strptime(now, "%H:%M:%S")).total_seconds()+86400)
    
    while True:
        hwnd = getHwnd()
        title = getForegroundWindowTitle()
        path = getForegroudWindowPath(hwnd)
        print(title)
        print(path)
        pid = getForegroundWindowPid(hwnd)[-1]
        if stringChecker(BlackList["paths"],path):
            if fiveMinuteWarning:
                if time.time()-timefromepoch<breakOverrideTime:
                    breakOverrideTime = breakOverrideTime - (time.time()-timefromepoch)
                    warnKill(breakOverrideTime, "exe", hwnd, pid)
            else:
                warnKill(10, "exe", hwnd, pid)
            fiveMinuteWarning=False
        
        if stringChecker(BlackList["titles"],title):
            if fiveMinuteWarning:
                if time.time()-timefromepoch<breakOverrideTime:
                    breakOverrideTime = breakOverrideTime - (time.time()-timefromepoch)
                    warnKill(breakOverrideTime, "exe", hwnd)
            else:
                warnKill(10, "exe", hwnd)
            fiveMinuteWarning=False
        for specialCase in specialCases:         
            if specialCase["testTarget"]=="path":
                if path and specialCase["case"] != path:
                    break
                if len(specialCase["whiteList"])>0:
                    blocktarget = specialCase["blockTarget"]
                    whiteList = getList(specialCase["whiteList"])
                    blockme = True
                    match blocktarget:
                        case "title":
                            blockme = stringChecker(whiteList, title, blockme)
                        case "URL":
                            # can only be accessed by chrome
                            url = getChromeAdress(pid)
                            blockme = stringChecker(whiteList, url,blockme)
                        case "explorerPath":
                            # can only be accessed by windows explorer
                            explorerPath = get_explorer_path(hwnd)
                            blockme = stringChecker(whiteList, explorerPath, blockme)
                        case "path":
                            blockme = stringChecker(whiteList, path,blockme)
                    if not blockme:
                        break
                    else :
                        # check for 5 minute warning
                        if fiveMinuteWarning:
                            if time.time()-timefromepoch<breakOverrideTime:
                                breakOverrideTime = breakOverrideTime - (time.time()-timefromepoch)
                                warnKill(breakOverrideTime, specialCase["KillType"], hwnd)
                        else:
                            warnKill(10, specialCase["KillType"], hwnd)
                elif path and specialCase["case"] in path:
                    blockTarget = specialCase["blockTarget"]
                    if specialCase["BlackListPath"][0]=="blackList.json":
                        specialCaseBlockList = getList(specialCase["BlackListPath"])
                    else :
                        specialCaseBlockList = specialCase["BlackListPath"]
                    blockme = False
                    match blockTarget:
                        case "title":
                            blockme = stringChecker(specialCaseBlockList, title,blockme)
                        case "URL":
                            url = getChromeAdress(pid)
                            blockme = stringChecker(specialCaseBlockList, url,blockme)
                            # this is used only for chrome, other web browsers should be blocked.
                        case "explorerPath":
                            explorerPath = get_explorer_path(hwnd)
                            blockme = stringChecker(specialCaseBlockList, explorerPath,blockme)
                            # this is used only for windows explorer
                        case "path":
                            blockme = stringChecker(specialCaseBlockList, path,blockme)
                        case _:
                            break
                    if blockme:
                        # check for 5 minute warning
                        if fiveMinuteWarning:
                            if time.time()-timefromepoch<breakOverrideTime:
                                breakOverrideTime = breakOverrideTime - (time.time()-timefromepoch)
                                warnKill(breakOverrideTime, specialCase["KillType"], hwnd)
                        else:
                            warnKill(10, specialCase["KillType"], hwnd)
                    

        
        # if path =="C:\Windows\explorer.exe":
        #     print("explorer")
        #     explorerPath = get_explorer_path(hwnd)
        #     print(explorerPath)
        #     if stringChecker(BlackList["FolderPaths"], explorerPath):   
        #         if fiveMinuteWarning:
        #             if time.time()-timefromepoch<breakOverrideTime:
        #                 breakOverrideTime = breakOverrideTime - (time.time()-timefromepoch)
        #                 time.sleep(breakOverrideTime)
        #                     # justwarn(5, "window", hwnd)
        #             # test to see that the window is still the same
        #             testHwnd = getHwnd()
        #             if testHwnd == hwnd:
        #                 testpath = getForegroudWindowPath(testHwnd)
        #                 if testpath == path:
        #                     kill("window", hwnd)
        #                     break                  
        # for pathStart in BlackList["paths"]:
        #     pid = getForegroundWindowPid(hwnd)[-1]
        #     if path.startswith(pathStart):
        #         if fiveMinuteWarning==True:
        #             if time.time()-timefromepoch<breakOverrideTime:
        #                 breakOverrideTime = breakOverrideTime - (time.time()-timefromepoch)
        #                 warnKill(breakOverrideTime, "exe", hwnd, pid)
        #         else:
        #             warnKill(10, "exe", hwnd, pid)
        #         fiveMinuteWarning=False
        #         break
                    # get the specialCaseBlockList and BlockTarget
        time.sleep(1)
        if isBreak():
            return windowCloser()
        

                    
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
from datetime import datetime,timedelta
import time 
from .createMessage import warningMessage
from .exeBlocker import kill
from .WindowDataFinders import getForegroundWindowPid, getForegroudWindowPath, getForegroundWindowTitle, get_explorer_path, getHwnd,getChromeAdress
from utils.JsonManipulators import ReadBlackList, ReadSchedule, removeBreak, removeDayOff, isBreak,getList

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
        
def windowCloser(control):
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
    specialCases = BlackList["SpecialCases"]
    
    
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
    while control.is_alive:
        try:
            windowCloserLoop(fiveMinuteWarning, breakOverrideTime, timefromepoch, BlackList, specialCases, control)
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            return
        except:
            time.sleep(1)
            windowCloserLoop(fiveMinuteWarning, breakOverrideTime, timefromepoch, BlackList, specialCases)
    # except:   
    #     # sometimes windows acts up and the window closer loop crashes, this is a failsafe to make sure that the program doesn't crash. 
    #     # it seems like the crashes mostly occur when a user is closing a window while that window is being checked against the blacklist.
    #     time.sleep(1)
    #     return windowCloserLoop(fiveMinuteWarning, breakOverrideTime, timefromepoch, BlackList, specialCases)
    
def windowCloserLoop(fiveMinuteWarning, breakOverrideTime, timefromepoch, BlackList, specialCases, control): 
    Schedule = ReadSchedule()
    weekday = datetime.now().strftime("%A")
    exitTime = Schedule[weekday]["end"]
    while control.is_alive:
        print(control.is_alive)
        hwnd = getHwnd()
        title = getForegroundWindowTitle()
        path = getForegroudWindowPath(hwnd)
        print(title)
        print(path)
        pid = getForegroundWindowPid(hwnd)[-1]
        # blockme  is used to check if the process is being checked against a blacklist or a whitelist. If it's set to true, then the process is being checked against a whitelist, if it's set to false, then the process is being checked against a blacklist. 
        blockme = False
        if stringChecker(BlackList["paths"],path,blockme):
            if fiveMinuteWarning:
                if time.time()-timefromepoch<breakOverrideTime:
                    breakOverrideTime = breakOverrideTime - (time.time()-timefromepoch)
                    warnKill(breakOverrideTime, "exe", hwnd, pid)
            else:
                warnKill(10, "exe", hwnd, pid)
            fiveMinuteWarning=False
        
        if stringChecker(BlackList["titles"],title,blockme):
            if fiveMinuteWarning:
                if time.time()-timefromepoch<breakOverrideTime:
                    breakOverrideTime = breakOverrideTime - (time.time()-timefromepoch)
                    warnKill(breakOverrideTime, "exe", hwnd)
            else:
                warnKill(10, "exe", hwnd)
            fiveMinuteWarning=False
        for specialCase in specialCases:         
            if specialCase["TestTarget"]=="path":
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
        time.sleep(1)
        now = datetime.now().strftime("%H:%M:%S")
        if now > exitTime:
            return windowCloser(control)
        if isBreak():
            return windowCloser(control)

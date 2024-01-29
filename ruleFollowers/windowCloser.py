from datetime import datetime,timedelta
import time 
from .create_message import warningMessage
from .exe_blocker import kill
from .window_data_finders import get_foreground_window_pid, get_foregroud_window_path, get_foreground_window_title, get_explorer_path, get_hwnd,get_chrome_adress
from utils.json_manipulators import read_blacklist, read_schedule, remove_break, remove_day_off, is_break,getList

def warn_kill(kill_time, kill_type, hwnd, pid = None):
        warningMessage(kill_time, kill_type, hwnd)
        time.sleep(kill_time-5)
        if get_hwnd() != hwnd:
            return
        kill(kill_type, hwnd, pid)

def string_checker(blocked_strings, string, blockme):
    if not string:
        return blockme
    else:
        for blocked_string in blocked_strings:
            if blocked_string in string:
                return not blockme
        return blockme
        
def window_closer(control):
    Schedule = read_schedule()
    break_left = Schedule["break"]
    five_minute_warning = False
    break_override_time = None
    if not break_left==0:
        five_minute_warning = True
        if (break_left>300):
            time.sleep(break_left-300)
            break_override_time = 300
        else:
            break_override_time = break_left
        remove_break(Schedule)
    time_from_epoch = time.time()
    blackList = read_blacklist()
    special_cases = blackList["special_cases"]
    
    
    today = datetime.now().strftime("%m/%d/%Y")
    print(today)
    for day in Schedule["DaysOff"]:
        if day == today:
            remove_day_off(Schedule)
            print("Today is a day off")
            return 
    
    weekday = datetime.now().strftime("%A")
    
    exit_time = Schedule[weekday]["end"]
    
    start_time = Schedule[weekday]["start"]
    
    # # get the current time
    now = datetime.now().strftime("%H:%M:%S")
    print (now)
    # # if the current time is less than the start time, sleep until the start time
    if now < start_time:
        print("Sleeping until start time")
        # sleep until the start time
        time.sleep((datetime.strptime(start_time, "%H:%M:%S") - datetime.strptime(now, "%H:%M:%S")).total_seconds())
    if now > exit_time:
        print("Sleeping until tomorrow")
        tomorrow = (datetime.today() + timedelta(days=1)).strftime('%A')
        # sleep until the start time of tomorrow
        time.sleep((datetime.strptime(Schedule[tomorrow]["start"], "%H:%M:%S") - datetime.strptime(now, "%H:%M:%S")).total_seconds()+86400)
    while control.is_alive:
        try:
            window_closerLoop(five_minute_warning, break_override_time, time_from_epoch, blackList, special_cases, control)
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            return
        except:
            time.sleep(1)
            window_closerLoop(five_minute_warning, break_override_time, time_from_epoch, blackList, special_cases,control)
    # except:   
    #     # sometimes windows acts up and the window closer loop crashes, this is a failsafe to make sure that the program doesn't crash. 
    #     # it seems like the crashes mostly occur when a user is closing a window while that window is being checked against the blacklist.
    #     time.sleep(1)
    #     return window_closerLoop(five_minute_warning, break_override_time, time_from_epoch, blackList, special_cases)
    
def window_closerLoop(five_minute_warning, break_override_time, time_from_epoch, blackList, special_cases, control): 
    Schedule = read_schedule()
    weekday = datetime.now().strftime("%A")
    exit_time = Schedule[weekday]["end"]
    while control.is_alive:
        print(control.is_alive)
        hwnd = get_hwnd()
        title = get_foreground_window_title()
        path = get_foregroud_window_path(hwnd)
        print(title)
        print(path)
        pid = get_foreground_window_pid(hwnd)[-1]
        # blockme  is used to check if the process is being checked against a blacklist or a whitelist. If it's set to true, then the process is being checked against a whitelist, if it's set to false, then the process is being checked against a blacklist. 
        blockme = False
        if string_checker(blackList["paths"],path,blockme):
            if five_minute_warning:
                if time.time()-time_from_epoch<break_override_time:
                    break_override_time = break_override_time - (time.time()-time_from_epoch)
                    warn_kill(break_override_time, "exe", hwnd, pid)
            else:
                warn_kill(10, "exe", hwnd, pid)
            five_minute_warning=False
        
        if string_checker(blackList["titles"],title,blockme):
            if five_minute_warning:
                if time.time()-time_from_epoch<break_override_time:
                    break_override_time = break_override_time - (time.time()-time_from_epoch)
                    warn_kill(break_override_time, "exe", hwnd)
            else:
                warn_kill(10, "exe", hwnd)
            five_minute_warning=False
        for specialCase in special_cases:         
            if specialCase["TestTarget"]=="path":
                if path and specialCase["case"] != path:
                    break
                if len(specialCase["whiteList"])>0:
                    blocktarget = specialCase["blockTarget"]
                    whiteList = getList(specialCase["whiteList"])
                    blockme = True
                    match blocktarget:
                        case "title":
                            blockme = string_checker(whiteList, title, blockme)
                        case "URL":
                            # can only be accessed by chrome
                            url = get_chrome_adress(pid)
                            blockme = string_checker(whiteList, url,blockme)
                        case "explorerPath":
                            # can only be accessed by windows explorer
                            explorerPath = get_explorer_path(hwnd)
                            blockme = string_checker(whiteList, explorerPath, blockme)
                        case "path":
                            blockme = string_checker(whiteList, path,blockme)
                    if not blockme:
                        break
                    else :
                        # check for 5 minute warning
                        if five_minute_warning:
                            if time.time()-time_from_epoch<break_override_time:
                                break_override_time = break_override_time - (time.time()-time_from_epoch)
                                warn_kill(break_override_time, specialCase["Kill_type"], hwnd)
                        else:
                            warn_kill(10, specialCase["Kill_type"], hwnd)
                elif path and specialCase["case"] in path:
                    blockTarget = specialCase["blockTarget"]
                    if specialCase["BlackListPath"][0]=="blackList.json":
                        specialCaseBlockList = getList(specialCase["BlackListPath"])
                    else :
                        specialCaseBlockList = specialCase["BlackListPath"]
                    blockme = False
                    match blockTarget:
                        case "title":
                            blockme = string_checker(specialCaseBlockList, title,blockme)
                        case "URL":
                            url = get_chrome_adress(pid)
                            blockme = string_checker(specialCaseBlockList, url,blockme)
                            # this is used only for chrome, other web browsers should be blocked.
                        case "explorerPath":
                            explorerPath = get_explorer_path(hwnd)
                            blockme = string_checker(specialCaseBlockList, explorerPath,blockme)
                            # this is used only for windows explorer
                        case "path":
                            blockme = string_checker(specialCaseBlockList, path,blockme)
                        case _:
                            break
                    if blockme:
                        # check for 5 minute warning
                        if five_minute_warning:
                            if time.time()-time_from_epoch<break_override_time:
                                break_override_time = break_override_time - (time.time()-time_from_epoch)
                                warn_kill(break_override_time, specialCase["Kill_type"], hwnd)
                        else:
                            warn_kill(10, specialCase["Kill_type"], hwnd)
        time.sleep(1)
        now = datetime.now().strftime("%H:%M:%S")
        if now > exit_time:
            return window_closer(control)
        if is_break():
            return window_closer(control)

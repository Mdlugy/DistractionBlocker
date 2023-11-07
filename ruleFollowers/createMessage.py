import time
import threading
from utils.windll32 import windll_32
from datetime import timedelta
from .WindowDataFinders import getHwnd
# from utils.bringToFront import bring_to_front



def worker1(title,close_event,close_until_seconds,finished_event):
    
    close_event.wait(timeout=close_until_seconds)
    wd=windll_32.FindWindowW(0,title)
    if wd:
        windll_32.SendMessageW(wd,0x0010,0,0)
    finished_event.set()
    return


def worker3(hwnd,finished_event):
    # maximizes the window after the messagebox closes itself
    # 9 is the code for restore window
    finished_event.wait()
    windll_32.ShowWindow(hwnd,9)
    return

def AutoCloseMessageBoxW(text, title, close_until_seconds, handle=None):
    close_event = threading.Event()
    finished_event = threading.Event()
    t1 = threading.Thread(target=worker1,args=(title,close_event,close_until_seconds,finished_event))
    t2 = threading.Thread(target=worker3,args=(handle,finished_event))

    if handle:
        # minimizes the window before the messagebox opens
        # 6 is the code for minimize window
        windll_32.ShowWindow(handle, 6)
        # restores the window after the messagebox closes (by itself, or by the user)
        t2.start()
    t1.start()
        
    windll_32.MessageBoxW(0, text, title, 0x00000000)
    wd = windll_32.FindWindowW(0, title)
    close_event.set()
    t1.join()
    if t2.is_alive():
        # finished_event.set()
        t2.join()
    return
        
def warningMessage(quickness , closeType,  hwnd=None, ):
    seconds = quickness
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    timeLeft = "%d:%02d:%02d" % (hour, minutes, seconds)
    new_line = '\n'
    message=f"{timeLeft} until Break is over, please close the window and return to work"
    if hwnd:
        message = f"{timeLeft} left until window is closed {new_line} please Save your progress and exit the window"
        AutoCloseMessageBoxW(message, "AlertMessage", 5, hwnd)
    else:
        print("no hwnd")
        AutoCloseMessageBoxW(message, "AlertMessage", 5)
 
 

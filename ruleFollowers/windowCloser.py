from typing import Optional
from ctypes import wintypes, windll, create_unicode_buffer
from distutils import spawn
import pyKey
import time 

def getForegroundWindowTitle() -> Optional[str]:
    hWnd = windll.user32.GetForegroundWindow()
    length = windll.user32.GetWindowTextLengthW(hWnd)
   # pid = windll.user32.GetWindowThreadProcessId(hWnd, None)
   # print(pid)
    buf = create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hWnd, buf, length + 1)
    
    # 1-liner alternative: return buf.value if buf.value else None
    if buf.value:
        return buf.value
    else:
        return None

for i in range(20):
    time.sleep(5)
    title = getForegroundWindowTitle()
    if title == "Among Us":
        pyKey.press.key("alt")
        pyKey.press.key("f4")
        pyKey.release.key("alt")
        pyKey.release.key("f4")

    print(title)

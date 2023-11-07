import ctypes
from ctypes import wintypes, windll, create_unicode_buffer,c_uint, c_int,byref

# def get_window_text(hwnd):
#     if type (hwnd)== None 
#     length = windll.user32.GetWindowTextLengthW(hwnd)
#     buf = create_unicode_buffer(length + 1)
#     windll.user32.GetWindowTextW(hwnd, buf, length + 1)
#     if buf.value:
#         return buf.value
#     else:
#         return None
# Function to get the path from an Explorer window


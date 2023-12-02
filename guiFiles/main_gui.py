from guizero import App, Text, PushButton, Box
import time
from datetime import datetime
from utils.JsonManipulators import ReadSchedule, addBreak
from threading import Thread
from .components import  header_box,create_time_box
from .component_utils import DisableButton, RunStop, TimeBox
from .add_a_break_window import create_break_Window
from .add_settings_window import add_settings_window
import asyncio

def get_static_time():
    schedule = ReadSchedule()
    weekday = datetime.now().strftime("%A")
    return schedule[weekday]['end']
def get_break_left():
    schedule = ReadSchedule()
    break_left = schedule['break']
    return break_left
def seconds_to_time(seconds):
    return time.strftime('%H:%M:%S', time.gmtime(seconds))
def remove_break():
    addBreak(0)
    force_update_time()
def close():
    run_stop.close(app)  
def create_new_break_window():
    create_break_Window(app,disable_break_button,time_state)
def create_settings_window():
    add_settings_window(app,disable_settings_button)
def start ():
    app.display()

app = App(title="Distraction Blocker", layout="auto", bg='lightblue')
run_stop = RunStop()
app.when_closed = close
time_state = TimeBox(run_stop)
header_box(app, "Distraction Blocker", "main")
Text(app, text="", size=10)
times_box = create_time_box(app,time_state,run_stop)
Text(app, text="", size=10)
settings_box = Box(app, layout="auto",border=True, align="bottom")
break_buttons_box = Box(app, layout="auto",border=True, align="right")
add_break_button = PushButton(break_buttons_box, text="Add Break", command=create_new_break_window)
disable_break_button = DisableButton(add_break_button)
add_settings_button = PushButton(settings_box, text="Settings", command=create_settings_window)
disable_settings_button = DisableButton(add_settings_button)
start()
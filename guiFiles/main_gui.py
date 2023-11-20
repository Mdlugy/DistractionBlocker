from guizero import App, Text, PushButton, Box
import time
from datetime import datetime
from utils.JsonManipulators import ReadSchedule, addBreak
from threading import Thread
from .components import  header_box,create_time_box
from .component_utils import DisableButton, RunStop, TimeBox
from .add_a_break_window import create_break_Window
import asyncio
# import styles

    
def get_static_time():
    schedule = ReadSchedule()
    # Load time from JSON file (replace 'your_file.json' with your file path)
    weekday = datetime.now().strftime("%A")
    return schedule[weekday]['end']
def get_break_left():
    schedule = ReadSchedule()
    break_left = schedule['break']
    return break_left
def seconds_to_time(seconds):
    return time.strftime('%H:%M:%S', time.gmtime(seconds))

# change this 
# def update_break(seconds):
#     addBreak(seconds)
#     update_break_left()
    
    
    
    
    
    
    
def remove_break():
    addBreak(0)
    force_update_time()
    
def close():
    run_stop.close(app)
 
    # while len(run_stop.processes) > 0:
    #     await asyncio.sleep(0.1)
    # app.destroy()
    
app = App(title="Distraction Blocker", layout="auto", bg='lightblue')
run_stop = RunStop()
app.when_closed = close

time_state = TimeBox(run_stop)

# setup formating boxes
header_box(app, "Distraction Blocker", "main")
# header_box = Box(app, layout="auto",border=True, align="top")
# padding between header_box and times_box
Text(app, text="", size=10)
times_box = create_time_box(app,time_state,run_stop)
# inner boxes for times_box
Text(app, text="", size=10)
# inner boxes for buttons_box
settings_box = Box(app, layout="auto",border=True, align="bottom")
break_buttons_box = Box(app, layout="auto",border=True, align="right")


# timer_selector(app)
# # header_box
# Text(header_box, text="", size=10)
# Text(header_box, text="Distraction Blocker", size=20, color= "white")
# Text(header_box, text="", size=20)

# current_time_box

# Text(current_time_box, text="Current Time", size=10, align="left")
# current_time = Text(current_time_box, text="00:00:00", size=20,align="right")
# Thread(target=update_time, daemon=True).start()

# end_time_box
# Text(end_time_box, text="End Time", size=10, align="left")

# static_time = Text(end_time_box, text=get_static_time(), size=20,align="right")
# remove_break_button = PushButton(break_left_box, text="End Break", command=remove_break)

# Break Left (Placeholder for now)
# break_left = Text(break_left_box, text="", size=20)
def create_new_break_window():
    create_break_Window(app,disable_break_button,time_state)
# Buttons
# settings_button = PushButton(settings_box, text="Settings", command=open_settings)
add_break_button = PushButton(break_buttons_box, text="Add Break", command=create_new_break_window)
disable_break_button = DisableButton(add_break_button)

def start ():
    app.display()
    return

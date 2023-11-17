from guizero import App, Text, PushButton, Box
import time
from datetime import datetime
from utils.JsonManipulators import ReadSchedule, addBreak
from threading import Thread
# import styles
def update_time():
    while True:
        current_time.value = time.strftime('%H:%M:%S')
        update_break_left()
        time.sleep(1)
def force_update_time():
    current_time.value = time.strftime('%H:%M:%S')
    update_break_left()
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
def update_break_left():
    break_seconds = get_break_left()
    if break_seconds > 300:
        break_left.value = f"Break Left: {seconds_to_time(break_seconds)}"
    elif break_seconds > 0:
        break_left.value = f"Break is almost over! \n Break Left: {seconds_to_time(break_seconds)}"
    else:
        break_left.value = ""
    if break_seconds > 0:
        addBreak(break_seconds-1)
def open_settings():
    # Placeholder for settings window functionality
    pass

def add_break():
    addBreak(200000)
    force_update_time()
def remove_break():
    addBreak(0)
    force_update_time()

app = App(title="Distraction Blocker", layout="auto", bg='lightblue')
# state for current time
current_time = Text(app, text="", size=20)



# Header

head_box = Box(app, layout="auto", align="top",)

# top padding for header
Text(head_box, text="", size=10)
# Header Text
Text(head_box, text="Distraction Blocker", size=20, color= "white")
# bottom padding for header
Text(head_box, text="", size=20)
# padding between Header and times_box
Text(app, text="", size=10)


# thread to update time for current time and check on BreakLeft
Thread(target=update_time, daemon=True).start()
times_box = Box(app, layout="auto", align="top")
current_time_box = Box(times_box, layout="auto", align="left")


# Label for Current Time
Text(hbox, text="Current Time", size=10)

# Static Time from JSON
static_time = Text(hbox, text=get_static_time(), size=20)

# Break Left (Placeholder for now)
break_left = Text(hbox, text="", size=20)

# Buttons
settings_button = PushButton(app, text="Settings", command=open_settings)
remove_break_button = PushButton(app, text="remove Break", command=remove_break)
add_break_button = PushButton(app, text="Add Break", command=add_break)
def start ():
    app.display()
    return

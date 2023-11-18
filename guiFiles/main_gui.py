from guizero import App, Text, PushButton, Box
import time
from datetime import datetime
from utils.JsonManipulators import ReadSchedule, addBreak
from threading import Thread
from .components import  header_box
from .component_utils import HideButton
from .add_a_break_window import create_break_Window
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
    if break_seconds != 0:
        break_left_box.show()
    if break_seconds > 300:
        break_left.value = f"Break Left: {seconds_to_time(break_seconds)}"
    elif break_seconds > 0:
        break_left.value = f"Break is almost over! \n Break Left: {seconds_to_time(break_seconds)}"
    else:
        break_left.value = ""
        break_left_box.hide()
    if break_seconds > 0:
        addBreak(break_seconds-1)
def open_settings():
    # Placeholder for settings window functionality
    pass





# change this 
def add_break():
    addBreak(200000)
    update_break_left()
    
    
    
    
    
    
    
def remove_break():
    addBreak(0)
    force_update_time()

app = App(title="Distraction Blocker", layout="auto", bg='lightblue')

# setup formating boxes
header_box(app, "Distraction Blocker", "main")
# header_box = Box(app, layout="auto",border=True, align="top")
# padding between header_box and times_box
Text(app, text="", size=10)
times_box = Box(app, layout="auto",border=True, align="top")
# inner boxes for times_box
constant_time_box = Box(times_box, layout="auto",border=True, align="top")
current_time_box = Box(constant_time_box, layout="auto",border=True, align="left")
end_time_box = Box(constant_time_box, layout="auto",border=True, align="right")
break_left_box = Box(times_box, layout="auto",border=True, align="bottom", visible=False)

# padding between times_box and buttons_box
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

Text(current_time_box, text="Current Time", size=10, align="left")
current_time = Text(current_time_box, text="00:00:00", size=20,align="right")
Thread(target=update_time, daemon=True).start()

# end_time_box
Text(end_time_box, text="End Time", size=10, align="left")

static_time = Text(end_time_box, text=get_static_time(), size=20,align="right")

# Break Left (Placeholder for now)
break_left = Text(break_left_box, text="", size=20)

# Buttons
settings_button = PushButton(settings_box, text="Settings", command=open_settings)
remove_break_button = PushButton(break_left_box, text="End Break", command=remove_break)
hide_break_button = HideButton()
create_break_Window(app,hide_break_button)
add_break_button = PushButton(break_buttons_box, text="Add Break", command=add_break, visible = hide_break_button.shown)
def start ():
    app.display()
    return

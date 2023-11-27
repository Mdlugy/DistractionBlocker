# import components/componentutils
from guizero import  Text, Box, Window
from .components import create_new_window, schedule_show
from .component_utils import RunStop, Scheduler
from utils.JsonManipulators import ReadSchedule, addBreak
def add_settings_window(parent):
#  create a window usint create_new_window from components, using app as the parent "settings" "edit"
    add_settings_window = create_new_window(parent, "Settings", "edit")
    add_settings_window.height = 1200
    add_settings_window.width = 500
    schedule = Scheduler()
    schedule_show(add_settings_window, schedule)
    Text(add_settings_window, text="", size=10)
#  this window will show the current times from the json file for the next week, days off and if there's an active break

    add_settings_window.show()

#  this window also shows information on blacklisted apps/ websites/ folders
#  there are 3 buttons "close", edit blacklists, edit schedule
# 
# close button just closes the window, there's no difference between closing the window and clicking the x, this just feels like a good stylistic choice

# edit blacklists button opens a new window calls add_blacklist_window from add_blacklist_window (expanded on in that file)
# edit schedule button opens a new window calls add_schedule_window from add_schedule_window (expanded on in that file)    pass
#     break_Window.show()
#     timer_selector(break_Window, timer_val)
#     def close_window():
#         creationButtonShown.toggleEnabled()
#         break_Window.destroy()
#     def kill_window():
#         break_Window.destroy()
#     def calculate_break():
#         timer_val.updateBreak()
#         creationButtonShown.toggleEnabled()
#         kill_window()
#     submit_break_button = create_button(break_Window, "Submit", calculate_break, "util_run", "large")
#     break_Window.show()
#     break_Window.when_closed = close_window
    
    pass

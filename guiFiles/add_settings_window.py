# import components/componentutils
from guizero import  Text, Box, Window
from .components import create_new_window, schedule_show, blackList_show
from .component_utils import Run_Stop, Scheduler
from utils.json_manipulators import read_schedule, add_break

def add_settings_window(parent,disable_creation_button):
#  create a window usint create_new_window from components, using app as the parent "settings" "edit"
    settings_window = create_new_window(parent, "Settings", "edit",disable_creation_button)
    settings_window.height = 1200
    settings_window.width = 1000
    schedule = Scheduler()
    
    schedule_show(settings_window, schedule)
    
    # blackList_show(settings_window)
    Text(settings_window, text="", size=10)
    
    pass

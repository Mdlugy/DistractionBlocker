from .components import timer_selector, create_new_window, create_button
from utils.JsonManipulators import addBreak
from .component_utils import TimerValue
# creating a class to store the state of the timervalue

def create_break_Window(parent,creationButtonShown=True):
    creationButtonShown = False
    timer_val = TimerValue()
    break_Window = create_new_window(parent,"Add a Break", "util_run")

    timer_selector(break_Window, timer_val)

    def kill_window():
        break_Window.destroy()
    def calculate_break():
        breakTime=timer_val.convertToSeconds()
        addBreak(breakTime)
        creationButtonShown = True
        kill_window()
    submit_break_button = create_button(break_Window, "Submit", calculate_break, "util_run", "large")
    break_Window.show()
from .components import timer_selector, create_new_window, create_button
from utils.JsonManipulators import addBreak
from .component_utils import TimerValue
# creating a class to store the state of the timervalue

def create_break_Window(parent,creationButtonShown, time_state):
    creationButtonShown.toggleEnabled()
    timer_val = TimerValue(addBreak)
    break_Window = create_new_window(parent,"Add a Break", "util_run")

    timer_selector(break_Window, timer_val)
    def close_window():
        creationButtonShown.toggleEnabled()
        break_Window.destroy()
    def kill_window():
        break_Window.destroy()
    def calculate_break():
        timer_val.updateBreak()
        creationButtonShown.toggleEnabled()
        kill_window()
    submit_break_button = create_button(break_Window, "Submit", calculate_break, "util_run", "large")
    break_Window.show()
    break_Window.when_closed = close_window
    
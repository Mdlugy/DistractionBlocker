from .components import timer_selector, create_new_window, create_button
from utils.json_manipulators import add_break
from .component_utils import CountDownTimer
# creating a class to store the state of the CountDownTimer

def create_break_Window(parent,creationButtonShown):
    # creationButtonShown.toggleEnabled()
    timer_val = CountDownTimer(add_break)
    break_Window = create_new_window(parent,"Add a Break", "util_run",creationButtonShown)

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
    
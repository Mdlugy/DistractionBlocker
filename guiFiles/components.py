import threading
from guizero import TextBox, Text, PushButton, Box, Window
from .styles import  TextColors, BGcolors,fonts, ButtonPaddings
from .component_utils import increment, decrement, validate_int, validate_value, TimeBox, update_text_simple, update_hidden_box,update_text_static_label,componentUpdater
def header_box(parent, heading, pageType):
    padding_size = 5 
    bg = BGcolors[pageType+"_header"]
    fg = TextColors[pageType+"_header"]
    font = fonts["header"]
    size = 20
    
    if pageType == "main":
        padding_size = 10
        size =40
    if pageType.startswith('util'):
        padding_size = 5
        size = 10
        
    header_box = Box(parent, layout="auto",border=True, align="top", width="fill")
    header_box.tk.configure(background=bg)
    # background color needs to be done in a text box 
    Text(header_box, text="", size=padding_size, bg=bg)
    Text(header_box, text=heading, color=fg, font=font, size=size, bg=bg    )
    # bottom padding
    Text(header_box, text="", size=padding_size*2, bg=bg)
def update_day_schedule(day,parent):
    
def day_schedule_box(parent, day, start, end,Parentwindow):
    def update_day_schedule_box_lambda(day, Parentwindow):
        update_day_schedule(day)
    day_schedule_box = Box(parent, layout="auto",border=True, align="top", width="fill")
    Text(day_schedule_box, text=day, align="left")
    Text(day_schedule_box, text=start, align="right")
    Text(day_schedule_box, text=end, align="right")
    
    return day_schedule_box

def schedule_show(parent,schedule):
    main_box = Box(parent, layout="auto",border=True, align="top")
    day_schedule_box(main_box, "Day", "Start", "End")
    print(schedule)
    day_schedule_box(main_box, "Mondays", schedule["Monday"]["start"], schedule["Monday"]["end"],parent)
    day_schedule_box(main_box, "Tuesdays", schedule["Tuesday"]["start"], schedule["Tuesday"]["end"],parent)
    day_schedule_box(main_box, "Wednesdays", schedule["Wednesday"]["start"], schedule["Wednesday"]["end"],parent)
    day_schedule_box(main_box, "Thursdays", schedule["Thursday"]["start"], schedule["Thursday"]["end"],parent)
    day_schedule_box(main_box, "Fridays", schedule["Friday"]["start"], schedule["Friday"]["end"],parent)
    day_schedule_box(main_box, "Saturdays", schedule["Saturday"]["start"], schedule["Saturday"]["end"],parent)
    day_schedule_box(main_box, "Sundays", schedule["Sunday"]["start"], schedule["Sunday"]["end"],parent)

def create_counter(parent,text, timerstate,timer_val, value ="00",  max_val=100 ):
    counter_box = Box(parent, layout="auto")
    Text(counter_box, text=text, align="left")
    number_box = TextBox(counter_box, text=value, align="left")
    def updateValue(value):
        if text == "hours:":
            timer_val.updateHour(value)
        elif text == "minutes:":
            timer_val.updateMinute(value)
        else :
            timer_val.updateSecond(value)
    
    def decrementLa():
        number_box.value=decrement(number_box.value, max_val)
        updateValue(number_box.value)
    def incrementLa():
        number_box.value=increment(number_box.value, max_val)
        updateValue(number_box.value)

    def validate_input():
        number_box.value= validate_int(number_box.value)
        number_box.value= validate_value(number_box.value, max_val)
        updateValue(number_box.value)

    number_box.when_key_released  = validate_input
    decrement_button = PushButton(counter_box, text="-", command=decrementLa, align="right")
    decrement_button.tk.config(borderwidth=0)
    increment_button = PushButton(counter_box, text="+", command=incrementLa, align="right")
    increment_button.tk.config(borderwidth=0)
    return counter_box

def timer_selector(parent,timer_val):
    timer_selector_box = Box(parent, layout="auto",border=True, align="top")
    create_counter(timer_selector_box,"hours:",timer_val.timerHour,timer_val, "00" ,24)
    create_counter(timer_selector_box,"minutes:",timer_val.timerMinute,timer_val, "00" ,59)
    create_counter(timer_selector_box,"seconds:",timer_val.timerSecond,timer_val, "00" ,59)
    return timer_selector_box
    
def create_new_window(parent,title, windowType):
        # app = App(title="Distraction Blocker", layout="auto", bg='lightblue')   

    window = Window(parent,title=title, layout="auto", bg=BGcolors[windowType])
    header_box(window, title, windowType)
    return window

def create_button(parent, text, command, buttonType, size):
    button = PushButton(parent, text=text, command=command, pady=ButtonPaddings[size]["pady"], padx=ButtonPaddings[size]["padx"])
    button.tk.config(bg=BGcolors[buttonType], fg=TextColors[buttonType+"_text"], font=fonts["button"])
    return button
def create_time_box(parent, time_state,run_stop):
    
    # outer box 
    outer_box = Box(parent, layout="auto",border=True, align="top", width="fill")
    outer_box.tk.configure(background=BGcolors["main"])
    # middle boxes X2 use outer box as parent
    # 1st middle box is never hidden, top aligned to outer box no border
    always_visible_box = Box(outer_box, layout="auto",border=True, align="top", width="fill")
    
    # inner boxes X2 use 1st middle box 1 as parent
    # inner box 1 is "current_time", uses state to get time every second it calls the state.update() function left aligned 
    current_time_box = Box(always_visible_box, layout="auto",border=True,align="left", width="fill")
    Text(current_time_box, text="Current Time", size=10, align="left")
    current_time = Text(current_time_box, text=time_state.current_time, size=20,align="right")
    current_time_updater = componentUpdater(time_state,"current_time", current_time, update_text_simple, run_stop)
    # Thread(target=update_time, daemon=True).start()
    # inner box 2 is "static_times", on creation it checks the current time and if its less than time_state.start_time, it will use the start time values for "label" and "time" else it will use the end time values for "label" and "time" right aligned otherwise it uses end_time values
    static_times_box = Box(always_visible_box, layout="auto",border=True, align="right", width="fill")
    static_time_label=Text(static_times_box, text="Static Time", size=10, align="left")
    static_time_value = Text(static_times_box, text=time_state.active_static_time, size=20,align="right")
    static_time_updater_label = componentUpdater(time_state,"waiting_for_start", static_time_label, update_text_static_label, run_stop)
    static_time_updater_value = componentUpdater(time_state,"active_static_time", static_time_value, update_text_simple, run_stop)
    # when the time_state_current time is equal to whatever the static time is, the static time will update to the next time this will use jsonUtils to get the next time to use
    break_left_box = Box(outer_box, layout="auto",border=True, align="bottom", width="fill", visible=True)
    Text(break_left_box, text="Break Left", size=20, )
    break_left = Text(break_left_box, text=time_state.break_time, size=20, align="right")
    break_left_updater = componentUpdater(time_state,"break_time_str", break_left, update_text_simple, run_stop)
    break_box_updater = componentUpdater(time_state,"break_time", break_left_box, update_hidden_box, run_stop)
    remove_break_button = PushButton(break_left_box, text="End Break", command=time_state.remove_break,align="left")
    # 2nd middle box is "break_left" uses state to get time left, bottom aligned to outer box it is default to hidden, unless there is a value in state.break_time in which case it will be shown it also includes a button which calls state.remove_break() and hides the box
    # outer box is returned
    pass

# constant_time_box = Box(times_box, layout="auto",border=True, align="top")
# current_time_box = Box(constant_time_box, layout="auto",border=True, align="left")
# end_time_box = Box(constant_time_box, layout="auto",border=True, align="right")
# break_left_box = Box(times_box, layout="auto",border=True, align="bottom", visible=False)

# # padding between times_box and buttons_box

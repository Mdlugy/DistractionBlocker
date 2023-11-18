from guizero import TextBox, Text, PushButton, Box, Window
from .styles import  TextColors, BGcolors,fonts, ButtonPaddings
from .component_utils import increment, decrement, validate_int, validate_value
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
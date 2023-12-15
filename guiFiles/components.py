from guizero import TextBox, Text, PushButton, Box, Window,ButtonGroup
from tkinter import Canvas, Scrollbar, Frame, Label
from .styles import  TextColors, BGcolors,fonts, ButtonPaddings
from .component_utils import increment, decrement, validate_int, validate_value, TimeBox, update_text_simple, update_hidden_box,update_text_static_label, componentUpdater,DisableButton,ListUpdater,datecreator, BlackList, wait_for_destruction
from functools import partial
import time 



# Shared Components
def create_scrollable_list_box(parent_box, items, stylestring, update_callBack, height=200, LabelText=None):
    if LabelText:
        Label(parent_box.tk, text=LabelText, bg=BGcolors[stylestring],fg="white", font=("Arial", 12)).grid(row=0, column=0, sticky="nsew")

    canvas = Canvas(parent_box.tk, highlightthickness=0, bg=BGcolors[stylestring], height=height,width=400)
    scrollbar = Scrollbar(parent_box.tk, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    # Grid layout for canvas and scrollbar
    canvas.grid(row=1, column=0, sticky="nsew")
    scrollbar.grid(row=1, column=1, sticky="ns")

    # Frame inside canvas with styling
    frame = Frame(canvas, bg=BGcolors[stylestring])
    canvas_frame = canvas.create_window((0, 0), window=frame, anchor="nw")

    # Function to update the content of the frame
    def rebuild_content():
        print("rebuild content called")
        # Clear existing content
        for widget in frame.winfo_children():
            widget.destroy()

        # Rebuild with updated items
        for item in items:
            label = Label(frame, text=item, bg=BGcolors[stylestring], fg="black", font=(fonts['default'], 12))
            label.pack()

        # Update scroll region
        canvas.configure(scrollregion=canvas.bbox("all"))

    # Bind the frame configuration to update the scroll region
    frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

    # Store the rebuild function in the callback
    callbackname = "scrollableListBox"
    if LabelText:
        callbackname = f"{LabelText}_scrollableListBox"
    update_callBack.setCallback('scrollableListBox',rebuild_content)
    rebuild_content()

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

def create_new_window(parent,title, windowType,disable_creation_button):
        # app = App(title="Distraction Blocker", layout="auto", bg='lightblue')   

    window = Window(parent,title=title, layout="auto", bg=BGcolors[windowType])
    header_box(window, title, windowType)
    Text(window, text="", size=10)
    disable_creation_button.toggleEnabled()
    def close_window():
        disable_creation_button.toggleEnabled()
        window.destroy()
    window.when_closed = close_window
    window.show()
    return window

# Components for the main window
def create_time_box(parent, time_state, run_stop):
    outer_box = Box(parent, layout="auto",border=True, align="top", width="fill")
    outer_box.tk.configure(background=BGcolors["main"])
    always_visible_box = Box(outer_box, layout="auto",border=True, align="top", width="fill")
    current_time_box = Box(always_visible_box, layout="auto",border=True,align="left", width="fill")
    Text(current_time_box, text="Current Time", size=10, align="left")
    current_time = Text(current_time_box, text=time_state.current_time, size=20,align="right")
    current_time_updater = componentUpdater(time_state,"current_time", current_time, update_text_simple, run_stop)
    static_times_box = Box(always_visible_box, layout="auto",border=True, align="right", width="fill")
    static_time_label=Text(static_times_box, text="Static Time", size=10, align="left")
    static_time_value = Text(static_times_box, text=time_state.active_static_time, size=20,align="right")
    static_time_updater_label = componentUpdater(time_state,"waiting_for_start", static_time_label, update_text_static_label, run_stop)
    static_time_updater_value = componentUpdater(time_state,"active_static_time", static_time_value, update_text_simple, run_stop)
    break_left_box = Box(outer_box, layout="auto",border=True, align="bottom", width="fill", visible=True)
    Text(break_left_box, text="Break Left", size=20, )
    break_left = Text(break_left_box, text=time_state.break_time, size=20, align="right")
    break_left_updater = componentUpdater(time_state,"break_time_str", break_left, update_text_simple, run_stop)
    break_box_updater = componentUpdater(time_state,"break_time", break_left_box, update_hidden_box, run_stop)
    remove_break_button = PushButton(break_left_box, text="End Break", command=time_state.remove_break,align="left")

#Components for the schedule section of the settings window


def schedule_show(parent,schedule):
    main_box = Box(parent, layout="auto",border=True, align="left")
    # day_schedule_box(main_box, "Day", "Start", "End")
    day_schedule_box(main_box, "Monday", schedule,schedule.Monday,parent)
    day_schedule_box(main_box, "Tuesday", schedule,schedule.Tuesday,parent)
    day_schedule_box(main_box, "Wednesday", schedule,schedule.Wednesday,parent)
    day_schedule_box(main_box, "Thursday", schedule,schedule.Thursday,parent)
    day_schedule_box(main_box, "Friday", schedule,schedule.Friday,parent)
    day_schedule_box(main_box, "Saturday", schedule,schedule.Saturday,parent)
    day_schedule_box(main_box, "Sunday", schedule,schedule.Sunday,parent)
    daysOff_box(main_box, schedule.daysOff, schedule)
    
def day_schedule_box(parent, day_name,state,day,Parentwindow):
    def refreshValue(startend):
        if startend == "start":
            print('start', day["start"].time)
            start_time_text.value = f"start-time: {day['start'].time}"
        else:
            print('end', day["end"].time)
            end_time_text.value = f"end-time: {day['end'].time}"
       
    def update_day_schedule_box():
        update_day_schedule(day_name,day, state, Parentwindow,refreshValue, disable_edit_button)
        
    day_schedule_box = Box(parent, layout="auto",border=True, align="top", width="fill")
    Text(day_schedule_box, text=day_name, align="left")
    start_time_text=Text(day_schedule_box, text=f"start-time: {day["start"].time}" )
    end_time_text=Text(day_schedule_box, text=f"end-time:{day["end"].time}")
    edit_button=PushButton(day_schedule_box, text="Edit", command=update_day_schedule_box, align="right")
    disable_edit_button = DisableButton(edit_button)
    return day_schedule_box












def daysOff_box(parent, daysOff, schedule):
    refresh_dates_box = ListUpdater()
    
    def update_daysOff_box_creator():
        update_daysOff(parent, schedule,refresh_dates_box,disable_edit_button)

    daysOff_box = Box(parent, layout="auto",border=True, align="right", width="fill")
    label = Text(daysOff_box, text="Days Off", size=14, font="Arial", align="top")
    dates_box = Box(daysOff_box, layout="auto",border=True, align="top", width="fill")
    create_scrollable_list_box(dates_box, daysOff, "util_edit", refresh_dates_box)
    edit_button=PushButton(daysOff_box, text="Edit", command=update_daysOff_box_creator, align="top")
    disable_edit_button = DisableButton(edit_button)

    return daysOff_box







def update_day_schedule(day_name,day,state,parent,refreshValue,disable_edit_button):
    disable_edit_button.toggleEnabled()
    def close_window():
        disable_edit_button.toggleEnabled()
        timeWindow.destroy()
    def update_day_start():
        state.update_sched_val(day_name,"start",day["start"].time)
        refreshValue("start")
    def update_day_end():
        state.update_sched_val(day_name,"end",day["end"].time)
        refreshValue("end")
        
    
    timeWindow = create_new_window(parent, f"schedule for {day_name}", "util_edit",disable_edit_button)
    start_time_box = Box(timeWindow, layout="auto",border=True, align="top", width="fill")
    Text(start_time_box, text="start time:", align="left")
    startTime = day["start"]
    create_counter(start_time_box,"hours:",startTime, startTime.timerHour ,24)
    create_counter(start_time_box,"minutes:",startTime,startTime.timerMinute ,59)
    create_counter(start_time_box,"seconds:",startTime,startTime.timerSecond ,59)
    PushButton(start_time_box, text= "Update", command=update_day_start, align="right")
    end_time_box = Box(timeWindow, layout="auto",border=True, width="fill")
    Text(end_time_box, text="end time:", align="left")
    end_time =day["end"]
    create_counter(end_time_box,"hours:",end_time, end_time.timerHour ,24)
    create_counter(end_time_box,"minutes:",end_time, end_time.timerMinute ,59)
    create_counter(end_time_box,"seconds:",end_time, end_time.timerSecond ,59)
    PushButton(end_time_box, text= "Update", command=update_day_end, align="right")
    timeWindow.when_closed = close_window
    return timeWindow


def remove_dayOffsOffBox(parent,state,refreshcomponent):
    current_page = 0
    totalPages = len(state.daysOff)/6
    totalPages = int(totalPages)
    
    print(totalPages)
    removeDaysOFfParentBox=Box(parent,layout="auto",border=True,align="top",width="fill")
    removeDaysOffBox = Box(parent, layout="auto",border=True, align="top",width="fill")
    dayBoxes={}
    def createDayBoxpage(parentBox, dayOff, pageNumber):
        refreshcomponent.setCallback("refreshDaysOff", partial(createDayBoxpage, parentBox, dayOff, pageNumber), True)
        nonlocal current_page
        wait_for_destruction(parentBox)
        # for widget in parentBox.children:
        #     widget.destroy()
        if pageNumber<=totalPages and pageNumber>=0:
            current_page=pageNumber
        print(current_page)
        # Clear existing content
        updateNavigationButtons()
        startIndex = pageNumber * 6
        endIndex = startIndex + 6
        print(startIndex,endIndex)
    # Slice the daysOff list for the current page
        daysOffSlice = state.daysOff[startIndex:endIndex+1]
        print(daysOffSlice)
        dayBoxes ={}
        for dayOff in daysOffSlice:
            daybox = Box(removeDaysOffBox, layout="auto", border=True, align="top")
            dayBoxButton = PushButton(daybox, text="remove", command=lambda dayOff=dayOff: remove_dayOff(dayOff),align="right")
            Text(daybox, text=dayOff, align="left")
            dayBoxes[dayOff] = daybox 
    def updateNavigationButtons():
        nonlocal totalPages
        totalPages = len(state.daysOff)/6
        # Clear existing navigation buttons
        wait_for_destruction(removeDaysOFfParentBox)
        # for widget in removeDaysOFfParentBox.children:
        #     widget.destroy()
        
        # Create navigation buttons
        nonlocal current_page
        
        if current_page != 0:
            previous_button = PushButton(removeDaysOFfParentBox, text="Previous", command=lambda: createDayBoxpage(removeDaysOffBox, state.daysOff, current_page - 1), align="left")
        if current_page < totalPages-1:
           next_button = PushButton(removeDaysOFfParentBox, text="Next", command=lambda: createDayBoxpage(removeDaysOffBox, state.daysOff, current_page + 1), align="right")


    def remove_dayOff(day):
        print(day)
        state.remove_day_off(day)
        refreshcomponent.callAllCallbacks()

        keys_to_check = list(dayBoxes.keys())
        for day_key in keys_to_check:
            if day_key not in state.daysOff:
                box = dayBoxes[day_key]
                box.destroy()
                del dayBoxes[day_key]
                refreshcomponent.callAllCallbacks()
        nonlocal totalPages
        totalPages = len(state.daysOff) // 10
        nonlocal current_page
        if current_page>totalPages:
            current_page-=1
        createDayBoxpage(removeDaysOffBox, state.daysOff, current_page)
    
    createDayBoxpage(removeDaysOffBox, state.daysOff,current_page)
    return removeDaysOffBox

def addDayOffBox(parent,state,refreshcomponent):
    add_dayOff_box = Box(parent, layout="auto",border=True, align="right", width="fill")
    date_val = datecreator()
    day = date_val.day
    month = date_val.month
    year = date_val.year
    create_counter(add_dayOff_box,"month:",date_val, month ,12,1)
    create_counter(add_dayOff_box,"day:",date_val, day ,31,1)
    create_counter(add_dayOff_box,"year:",date_val, year ,9999,2023)
    def add_dayOff():
        date_val.validate()
        date = date_val.date
        print("day to add",date)
        state.add_day_off(date)
        refreshcomponent.callAllCallbacks()
    PushButton(add_dayOff_box, text= "Add", command=add_dayOff, align="right")
    
    
def update_daysOff(parent,state,refreshcomponent, disable_edit_button):
    daysOffWindow = create_new_window(parent, "Days Off", "util_edit", disable_edit_button)
    daysOffWindow.height = 750
    daysOffWindow.width = 500
    
    remove_dayOffsOffBox(daysOffWindow,state,refreshcomponent)
    addDayOffBox(daysOffWindow,state,refreshcomponent)


def create_counter(parent,text,timer_val, value ="00",  max_val=100, min_val=0 ):
    counter_box = Box(parent, layout="auto")
    Text(counter_box, text=text, align="left")
    number_box = TextBox(counter_box, text=value, align="left")
    def updateValue(value):
        match text:
            case "hours:":
                timer_val.updateHour(value)
            case "minutes:":
                timer_val.updateMinute(value)
            case "seconds:":
                timer_val.updateSecond(value)
            case "month:":
                timer_val.updateMonth(value)
            case "day:":
                timer_val.updateDay(value)
            case "year:":
                timer_val.updateYear(value)
                
    def decrementLa():
        number_box.value=decrement(number_box.value, max_val,min_val)
        updateValue(number_box.value)
    def incrementLa():
        number_box.value=increment(number_box.value, max_val,min_val)
        updateValue(number_box.value)

    def validate_input():
        number_box.value= validate_int(number_box.value)
        number_box.value= validate_value(number_box.value, max_val,min_val)
        updateValue(number_box.value)

    number_box.when_key_released  = validate_input
    decrement_button = PushButton(counter_box, text="-", command=decrementLa, align="right")
    decrement_button.tk.config(borderwidth=0)
    increment_button = PushButton(counter_box, text="+", command=incrementLa, align="right")
    increment_button.tk.config(borderwidth=0)
    return counter_box

def timer_selector(parent,timer_val):
    timer_selector_box = Box(parent, layout="auto",border=True, align="top")
    create_counter(timer_selector_box,"hours:",timer_val, "00" ,24)
    create_counter(timer_selector_box,"minutes:",timer_val, "00" ,59)
    create_counter(timer_selector_box,"seconds:",timer_val, "00" ,59)
    return timer_selector_box
    

def create_button(parent, text, command, buttonType, size):
    button = PushButton(parent, text=text, command=command, pady=ButtonPaddings[size]["pady"], padx=ButtonPaddings[size]["padx"])
    button.tk.config(bg=BGcolors[buttonType], fg=TextColors[buttonType+"_text"], font=fonts["button"])
    return button

# constant_time_box = Box(times_box, layout="auto",border=True, align="top")
# current_time_box = Box(constant_time_box, layout="auto",border=True, align="left")
# end_time_box = Box(constant_time_box, layout="auto",border=True, align="right")
# break_left_box = Box(times_box, layout="auto",border=True, align="bottom", visible=False)

# # padding between times_box and buttons_box
# def create_scrollable_list_box(parent_box, items, stylestring, update_callBack):

def blackList_category_box(parent, category, state, refreshcomponent):
    category_box = Box(parent, layout="auto",border=True, align="top", width="fill")
    itemList = state.get_category(category)
    # label = Text(parent, text=category, size=10, font="Arial", align="top")
    items_area = create_scrollable_list_box(category_box, itemList, "util_edit", refreshcomponent,75, category) 
    return category_box
def blackList_show(parent):
    blackList_box = Box(parent, layout="auto",border=True, align="right", width="fill")
    blackList_box.tk.configure(background=BGcolors["edit"])
    blackList_box.tk.configure(background=BGcolors["edit"])
    Text(blackList_box, text="BLACKLIST", size=20)
    blacklist_state = BlackList()
  
    refresh_paths_box = ListUpdater()
    paths_box = blackList_category_box(blackList_box, "paths", blacklist_state, refresh_paths_box)
    
    refresh_titles_box = ListUpdater()
    titles_box = blackList_category_box(blackList_box, "titles", blacklist_state, refresh_titles_box)
    refresh_folder_paths_box = ListUpdater()
    folder_paths_box = blackList_category_box(blackList_box, "FolderPaths", blacklist_state, refresh_folder_paths_box)
    refresh_urls_box = ListUpdater()
    urls_box = blackList_category_box(blackList_box, "Urls", blacklist_state, refresh_urls_box)
    refresh_special_cases_box = ListUpdater()
    special_cases_box = blackList_category_box(blackList_box, "SpecialCases", blacklist_state,refresh_special_cases_box)
    def create_blackList_edit_window():
        blackList_edit_window(parent, disable_edit_button, blacklist_state,refresh_special_cases_box)
    
    edit_button=PushButton(blackList_box, text="Edit", command=create_blackList_edit_window, align="bottom")
    disable_edit_button = DisableButton(edit_button)
    return blackList_box

def blackList_edit_window(parent, disable_edit_button, blacklist_state, refresh_special_cases_box):
    blackList_edit_window = create_new_window(parent, "Edit Blacklist", "util_edit")
    blackList_edit_window.height = 750
    blackList_edit_window.width = 500
    body = Box(blackList_edit_window, layout="auto", border=True, align="top", width="fill", height="fill")
    top = Box(body, layout="auto", border=True, align="top", width="fill", height="fill")
    top_top = Box(top, layout="auto", border=True, align="top", width="fill", height="fill")
    top_bottom = Box(top, layout="auto", border=True, align="bottom", width="fill", height="fill")
    bottom = Box(body, layout="auto", border=True, align="bottom", width="fill", height="fill")
    pathsBox= create_blackList_edit_box(top_top, "paths", blacklist_state,"left" )
    titlesBox= create_blackList_edit_box(top_top, "titles", blacklist_state,"right" )
    
    folderPathsBox= create_blackList_edit_box(top_bottom, "FolderPaths", blacklist_state,"left" )
    urlsBox= create_blackList_edit_box(top_bottom, "Urls", blacklist_state,"right" )
    choice = ButtonGroup(bottom, options=["SpecialCases", "standard"], selected="SpecialCases")
    addItem = add_blackList_item_box(bottom, choice.value, blacklist_state, refresh_special_cases_box)
    current_choice = "SpecialCases"
    def add_blackList_item():
        nonlocal current_choice
        if current_choice =="SpecialCases":
            current_choice = "standard"
        else:
            current_choice = "SpecialCases"
        print(current_choice)
        # choice._selected = current_choice
        nonlocal addItem
        addItem.destroy()
        nonlocal choice
        choice.destroy()
        choice = ButtonGroup(bottom, options=["SpecialCases", "standard"], selected=current_choice)
        addItem = add_blackList_item_box(bottom, current_choice, blacklist_state, refresh_special_cases_box)
        choice.when_clicked=add_blackList_item

        # choice._selected = choice_value
    choice.when_clicked=add_blackList_item
    blackList_edit_window.show()
    
def create_blackList_edit_box(parent, category, blacklist_state, align_pos):
    print(category)
    category_box = Box(parent, layout="auto",border=True, width="fill", height="fill", align= align_pos)
    category_text=Text(category_box, text=category, size=10, font="Arial", align="top")
    itemList = blacklist_state.get_category(category)
    for item in itemList:
        def removeItem():
            blacklist_state.remove_blackList_item(category, item)
            
        create_blackList_edit_item_box(category_box, item,removeItem) 
        
    return category_box
def create_blackList_edit_item_box(parent, item, remove_blackList_item_callback=None):
    item_box = Box(parent, layout="auto",border=True, align="top", width="fill")
    Text(item_box, text=item, size=10, font="Arial", align="left")
    remove_button = PushButton(item_box, text="remove", command=remove_blackList_item_callback,align="right")


def add_blackList_item_box(parent, category, blacklist_state, refreshcomponent):
    add_blackList_item_box = Box(parent, layout="auto",border=True, align="left", width="fill")
    if category == "SpecialCases":
        label = Text(add_blackList_item_box, text="Special Case", size=10, font="Arial", align="left")
        # input_box_label = Box(add_blackList_item_box, layout="auto",border=True, align="top", width="fill")
        # Text(input_box_label, text="Label", size=10, font="Arial", align="left")
        # input_box_label = Box(add_blackList_item_box, layout="auto",border=True, align="top", width="fill")
        # kill_type_box = Box(input_box_label, layout="auto",border=True, align="left", width="fill")
        # Text(kill_type_box, text="Kill Type", size=10, font="Arial", align="left")
        # kill_type_choice = ButtonGroup(kill_type_box, options=["exe", "window"], selected="exe")
        # target_box = Box(input_box_label, layout="auto",border=True, align="right", width="fill")
        # Text(target_box, text="target", size=10, font="Arial", align="left")
        # target = TextBox(case_box, text="", align="right")
        # test_target_box = Box(input_box_label, layout="auto",border=True, align="right", width="fill")
        # Text(test_target_box, text="test target", size=10, font="Arial", align="left")
        # test_target_choice = ButtonGroup(test_target_box, options=["path", "title"], selected="path")
        # white_or_blacklist_box = Box(input_box_label, layout="auto",border=True, align="right", width="fill")
        # Text(white_or_blacklist_box, text="whitelist or blacklist exceptions", size=8, font="Arial", align="left")
        # white_or_blacklist_choice = ButtonGroup(white_or_blacklist_box, options=["whitelist", "blacklist"], selected="whitelist")
        # if white_or_blacklist_box.value=="whitelist":
        #     whitelist_box = Box(input_box_label, layout="auto",border=True, align="right", width="fill")
        #     Text(whitelist_box, text="whitelist", size=10, font="Arial", align="left")
        #     Text(whitelist_box, text="please comma seperate exceptions", size=7, font="Arial", align="left")
        #     whitelist = TextBox(whitelist_box, text="", align="right")
        # else:
        #     blacklist_box = Box(input_box_label, layout="auto",border=True, align="right", width="fill")
        #     Text(blacklist_box, text="blacklist", size=10, font="Arial", align="left")
        #     existing_list_or_array_box = Box(blacklist_box, layout="auto",border=True, align="right", width="fill")
        #     Text(existing_list_or_array_box, text="comma separated List, or existing list", size=8, font="Arial", align="left")
        #     existing_list_or_array_choice = ButtonGroup(existing_list_or_array_box, options=["new", "existing"], selected="list")           
        #     if existing_list_or_array_box.value=="new":
        #         Text(blacklist_box, text="please comma seperate exceptions", size=7, font="Arial", align="left")
        #         blacklist = TextBox(blacklist_box, text="", align="right")
        #     else:
        #         blacklist = ButtonGroup(blacklist_box, options=["FolderPaths", "Urls","paths","titles"], selected="FolderPaths")
        # block_target_box = Box(input_box_label, layout="auto",border=True, align="right", width="fill")
        # Text(block_target_box, text="block target", size=10, font="Arial", align="left")
        # block_target_choice = ButtonGroup(block_target_box, options=["URL", "title","explorerPath","path"], selected="URL")
    else:
        label = Text(add_blackList_item_box, text=category, size=10, font="Arial", align="left")
        input_box_label = Box(add_blackList_item_box, layout="auto",border=True, align="top", width="fill")
        blockType_choice = ButtonGroup(input_box_label, options=["FolderPaths", "Urls","paths","titles"], selected="FolderPaths")
        Text(input_box_label, text="enter blocklist item here", size=10, font="Arial", align="left")
        blocklist_item = TextBox(input_box_label, text="", align="right")
    def submit():
        refreshcomponent.callAllCallbacks()
        print ("test")
    submit_button = PushButton(add_blackList_item_box, text="submit", command=submit,align="right")
    return add_blackList_item_box
    #                           BlackList Edit Window
    #                        Paths:              Titles:   
    
          
    #                       FolderPaths:            Urls:    
    
    
    #                       SpecialCases:       addNew:
    
    
    
    
    # 
    
    # day_schedule_box(main_box, "Monday", schedule,schedule.Monday,parent)
    # day_schedule_box(main_box, "Tuesday", schedule,schedule.Tuesday,parent)
    # day_schedule_box(main_box, "Wednesday", schedule,schedule.Wednesday,parent)
    # day_schedule_box(main_box, "Thursday", schedule,schedule.Thursday,parent)
    # day_schedule_box(main_box, "Friday", schedule,schedule.Friday,parent)
    # day_schedule_box(main_box, "Saturday", schedule,schedule.Saturday,parent)
    # day_schedule_box(main_box, "Sunday", schedule,schedule.Sunday,parent)
    # daysOff_box(main_box, schedule.daysOff, schedule)
    
#     {"paths": ["I:\\"], "titles": ["Games (I:)"], "FolderPaths": ["I:\\"], "Urls":[],
# "SpecialCases":[
#         {   
#             "Label":"Firefox"
#             "KillType":"exe",
#             "Case":"C:\\Program Files\\Mozilla Firefox\\firefox.exe",
#             "TestTarget":"path",
#             "WhiteList":["Firefox Developer Edition"],
#             "BlackListpath":[],
#             "BlockTarget":"title"
#         },
#         {   "Label": "IrfanView"
#             "KillType":"exe",
#             "case":"C:\\Program Files\\IrfanView\\i_view64.exe",
#             "TestTarget":"path",
#             "WhiteList":[],
#             "BlackListpath":["blackList.json","FolderPaths"],
#             "BlockTarget":"title"
#         },
#         {   "Label": "Chrome"
#             "KillType":"window",
#             "case":"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
#             "TestTarget":"path",
#             "WhiteList":[],
#             "BlackListpath":["blackList.json","Urls"],
#             "BlockTarget":"URL"
#         },
#         {   
#             "Label": "Explorer"
#             "KillType":"window",
#             "case":"C:\\Windows\\explorer.exe",
#             "WhiteList":[],
#             "TestTarget":"path",
#             "BlackListpath":["blackList.json","Urls"],
#             "BlockTarget":"explorerPath"
#         }
        
#     ]} 
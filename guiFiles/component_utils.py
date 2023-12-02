import threading
import time
from datetime import datetime, timedelta
from utils.JsonManipulators import ReadSchedule, addBreak, writeJson,ReadBlackList
def destroy_widgets(container, tk_or_guizero):
    if tk_or_guizero == "tk":
        for widget in container.winfo_children():
            widget.destroy()
        return check_widgets_destroyed(container)
    for widget in container.children:
        widget.destroy()
    return check_widgets_destroyed(container)

def check_widgets_destroyed(container):
    # Check if all widgets are destroyed
    return len(container.children) == 0

def wait_for_destruction(container, tk_or_guizero="guizero"):
    while not destroy_widgets(container, tk_or_guizero):
        time.sleep(0.01)  # Wait for a short period before checking again
    print("succesfully removed widgets")
    return True

def is_time_between(current_time_str, start_time_str, end_time_str):
    current_time = datetime.strptime(current_time_str, "%H:%M:%S").time()
    start_time = datetime.strptime(start_time_str, "%H:%M:%S").time()
    end_time = datetime.strptime(end_time_str, "%H:%M:%S").time()

    return start_time <= current_time <= end_time

def validate_int(str):
    try:
        num = int(str)
    except:
        num = 0
    if num < 10:
        return f"0{num}"
    return f"{num}"

def validate_value (num,max_val, min_val):
    num = int(num)
    if num > max_val:
        if min_val == 0:
            return "00"
        elif min_val < 10:
            return f"0{min_val}"
        return f"{min_val}" 
    elif num < min_val:
        if min_val>100:
            # if the min_val is too high I don't want to loop around the max_val, I'd rather just stop the decrement
            return f"{min_val}"
        return f"{max_val}"
    elif num < 10:
        return f"0{num}"
    
    return f"{num}"


def increment(str, max_val, min_val):
    intstr=validate_int(str)
    num = int(intstr)
    num += 1
    num = validate_value(num,max_val, min_val)
    return num

def decrement(str, max_val, min_val):
    intstr=validate_int(str)
    num = int(intstr)
    num -= 1
    num = validate_value(num,max_val,min_val )
    return num
# a utility class that'll be passed into any classes that run treaded processes to trigger a stop from the main thread
class RunStop:
    def __init__(self):
        self.run = True
        self.processes = []
        self.to_join = []

    def stop(self):
        self.run = False

    def addProcess(self, process):
        self.processes.append(process)

    def markForJoin(self, process):
        self.to_join.append(process)
        self.processes.remove(process)

    def joinMarkedThreads(self):
        for process in self.to_join:
            process.join()
        self.to_join = []

    def close(self, app):
        self.stop()
        def wait_and_close():
            for process in self.processes:
                process.join()  # Ensure all threads are joined
            app.destroy()
        threading.Thread(target=wait_and_close, daemon=True).start()


        
# a Class for storing the state of the break being set. might be refactored and extended to be re-used for other time objects 
class TimeBase:
    def __init__(self):
        self.timerHour = "00"
        self.timerMinute = "00"
        self.timerSecond = "00"
    def updateHour(self, value):
        self.timerHour = value
    def updateMinute(self, value):
        self.timerMinute = value
    def updateSecond(self, value):
        self.timerSecond = value

class TimeValue(TimeBase):
    def __init__(self, stringValue):
        super().__init__()
        self.time = stringValue
        self.convertStringToTime()
    def convertStringToTime(self):
        self.timerHour = self.time.split(":")[0]
        self.timerMinute = self.time.split(":")[1]
        self.timerSecond = self.time.split(":")[2]
    def updateTime(self,value):
        self.time = value
        self.convertStringToTime()
    def updateselfTime(self):
        self.time = f"{self.timerHour}:{self.timerMinute}:{self.timerSecond}"
    
    def updateHour(self, value):
        super().updateHour(value)
        self.updateselfTime()

    def updateMinute(self, value):
        super().updateMinute(value)
        self.updateselfTime()

    def updateSecond(self, value):
        super().updateSecond(value)
        self.updateselfTime()
class CountDownTimer(TimeBase):
    def __init__(self, addBreak):
        super().__init__()
        # self.run_stop = run_stop
        self.addBreak = addBreak
    def convertToSeconds(self):
        return int(self.timerHour)*3600 + int(self.timerMinute)*60 + int(self.timerSecond)
    def updateBreak(self):
        seconds = self.convertToSeconds()
        self.addBreak(self.convertToSeconds())

# a utility class passed into objects created after new windows are open to block the use of the button which creates that window
class DisableButton:
    def __init__(self, button):
        self.enabled = True
        self.button = button
     
    def toggleEnabled(self):
        self.enabled = not self.enabled
        self.button.enabled = self.enabled
    
# a larget state object used for TimeBox components.
class TimeBox:
    def __init__(self, runstop):
        # current time initialization and thread
        self.current_time = None
        self.runstop = runstop
        self.update_thread = threading.Thread(target=self.update_times, daemon=True)
        self.update_thread.start()
        # getting the start/stop time, the active start/stop time will be set to "active_static_time", if the active_start_time is "start", waiting_for_start will be set to true
        self.active_static_time = None
        self.next_active_static_time = None
        self.waiting_for_start = False        
        self.get_static_times()
        self.break_time = None
        self.get_break_time()
        self.runstop.addProcess(self.update_thread)
        self.break_time_str=""
    def stop(self):
        self.runstop.markForJoin(self.update_thread)

    def update_times(self):
        counter = 0
        while self.runstop.run:
            if counter % 100 == 0:
                now = datetime.now()
                self.current_time = now.strftime("%H:%M:%S")
                self.get_break_time()
                if self.break_time>0:
                    self.update_break(self.break_time-1)
                     
                self.get_static_times()
            time.sleep(0.01)
            counter += 1
        self.stop()
            
    def get_static_times(self):
        # Load time from JSON file (replace 'your_file.json' with your file path)
        schedule = ReadSchedule()
        weekday = datetime.now().strftime("%A")
        today_start = schedule[weekday]['start']
        today_end = schedule[weekday]['end']       

        if not is_time_between(self.current_time, today_start, today_end):
            self.waiting_for_start = True
            self.active_static_time = today_start
            self.next_active_static_time = today_end
        else:
            self.waiting_for_start = False
            self.active_static_time = today_end
            # get the next day with an active start time
            while True:
                i=1
                weekday = (datetime.now() + timedelta(days=i)).strftime("%A")
                if schedule[weekday]['start'] != None:
                    break
                i+=1
            self.next_active_static_time = schedule[weekday]['start']        
    def get_break_time(self):
        schedule = ReadSchedule()
        self.break_time = schedule['break']
        self.break_time_str =str(timedelta(seconds=self.break_time))
    def update_break(self, seconds):
        addBreak(seconds)
        self.get_break_time()
        
    def remove_break(self):
        addBreak(0)
        self.get_break_time()
        
class ListUpdater:
    def __init__(self):
        self.callback = None
    def setCallback(self,callbackFunction):
        self.callback = callbackFunction
    def callCallback(self):
        self.callback()

class componentUpdater:
    def __init__(self, state,target_attribute, component, update_function, runstop):
        self.state=state
        self.target_attribute = target_attribute
        self.component = component
        self.update_function = update_function
        self.update_thread = threading.Thread(target=self.update, daemon=True)
        self.update_thread.start()

    def update(self):
        while True:
            value = getattr(self.state, self.target_attribute)
            self.update_function(self.component, value)
            time.sleep(0.1)
            
    def stop(self):
        self.runstop.markForJoin(self.update_thread)
class datecreator:
    def __init__(self):
        self.date = None
        self.day = None
        self.month = None
        self.year = None
        self.initialize_date()

    def initialize_date(self):
        self.date = datetime.now().strftime("%m/%d/%Y")
        self.day = datetime.now().strftime("%d")
        self.month = datetime.now().strftime("%m")
        self.year = datetime.now().strftime("%Y")

    def update_date(self):
        try:
            year = int(self.year)
            month = int(self.month)
            day = int(self.day)
            date = datetime(year, month, day)
        except ValueError:
            # Handle invalid date values, e.g., leap year issue, invalid month/day, etc.
            date = decrement_to_valid_date(datetime(year, month, day))  
        self.date = date.strftime("%m/%d/%Y")

    def updateDay(self, value):
        self.day = value
        if len(self.day) == 1:
            self.day = f"0{self.day}"
        self.update_date()
        
    def updateMonth(self, value):
        self.month = value
        if len(self.month) == 1:
            self.month = f"0{self.month}"
        self.update_date()
        
    def updateYear(self, value):
        self.year = value
        self.update_date()
        
    def validate(self):
        date = self.date
        print (date)
        # convert from strftime('%m/%d/%Y') to datetime
        date = datetime.strptime(date, "%m/%d/%Y")
        # get today datetime
        today = datetime.today()
        if date < today:
            date = today
        self.date = date.strftime("%m/%d/%Y")
        
def decrement_to_valid_date(date):
    while True:
        try:
            valid_date = date
            return valid_date.strftime("%m/%d/%Y")
        except ValueError:
            date = date.replace(day=date.day - 1)
            if date.day == 0:
                raise ValueError("Invalid starting date provided.")


    
class Scheduler :
    def __init__(self):
        self.Monday = None
        self.Tuesday = None
        self.Wednesday = None
        self.Thursday = None
        self.Friday = None
        self.Saturday = None
        self.Sunday = None
        self.day_to_update = None
        self.daysOff = None
        self.read_schedule()
    def read_schedule(self):
        schedule = ReadSchedule()
        self.Monday = self.update_day_init(schedule['Monday'])
        self.Tuesday = self.update_day_init(schedule['Tuesday'])
        self.Wednesday = self.update_day_init(schedule['Wednesday'])
        self.Thursday = self.update_day_init(schedule['Thursday'])
        self.Friday = self.update_day_init(schedule['Friday'])
        self.Saturday = self.update_day_init(schedule['Saturday'])
        self.Sunday = self.update_day_init(schedule['Sunday'])
        sorted_dates = sorted(set(schedule['DaysOff']), key=lambda x: time.strptime(x, "%m/%d/%Y"))
        self.daysOff = sorted_dates
    def update_day_init(self, day):
        start =TimeValue(day['start'])
        end = TimeValue(day['end'])
        return {"start":start, "end":end}
    def remove_day_off(self, day):
        if day in self.daysOff:
            self.daysOff.remove(day)
            print(f"Removed {day}. Current days off: {self.daysOff}")
        else:
            print(f"{day} not found in days off.")
        schedule = ReadSchedule()
        schedule['DaysOff'] = self.daysOff
        writeJson('scheduler.json', schedule)
        
    def update_sched_val(self, day, part, value):
        schedule = ReadSchedule()
        print(value)
        schedule[day][part] = value
        writeJson('scheduler.json', schedule)
        if part == "start":
            self.__dict__[day]["start"].updateTime(value)
        elif part == "end":
            self.__dict__[day]["end"].updateTime(value)
    def add_day_off(self,val):
        daysOff = self.daysOff
        daysOff.append(val)
        sorted_dates = sorted(set(daysOff), key=lambda x: time.strptime(x, "%m/%d/%Y"))
        self.daysOff=sorted_dates
        schedule = ReadSchedule()
        schedule['DaysOff'] = self.daysOff
        writeJson('scheduler.json', schedule)
        
def get_break_left():
    schedule = ReadSchedule()
    break_left = schedule['break']
    return break_left
    
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
        
class BlackList:
    def __init__(self):
        self.paths = []
        self.titles = []
        self.FolderPaths = []
        self.Urls = []
        self.specialCases = []
        self.read_blacklist()
        
    def read_blacklist(self):
        blacklist = ReadBlackList()
        self.paths = blacklist['paths']
        self.titles = blacklist['titles']
        self.FolderPaths = blacklist['FolderPaths']
        self.Urls = blacklist['Urls']
        self.SpecialCases = blacklist['SpecialCases']
        
    def get_category(self,categoryName):
        print(categoryName)
        if categoryName=="SpecialCases":          
            labelList = []
            for item in self.SpecialCases:
                labelList.append(item['Label'])
        else:
            labelList = self.__dict__[categoryName]
        print(labelList)
        return labelList
    def remove_blacklist_item(self,categoryName, label):
        if categoryName=="SpecialCases":
            for item in self.SpecialCases:
                if item['Label'] == label:
                    self.SpecialCases.remove(item)
        else:
            self.__dict__[categoryName].remove(label)
        BlackList = ReadBlackList()
        BlackList[categoryName] = self.__dict__[categoryName]
        writeJson('blackList.json', blacklist)
# here I'll include some variatons of the update_text function that may require specific match cases/if else statements, formatting, etc. 
 
# base case where we simply update the text of the component 
def update_text_simple(component, string):
    component.value = string

def update_text_static_label(component, boolean):
    if boolean:
        component.value = "Start Time"
    else:
        component.value = "End Time"
def update_hidden_box(component, value):
    if value:
        component.show()
    else:
        component.hide()

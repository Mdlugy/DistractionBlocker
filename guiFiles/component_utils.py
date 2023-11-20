import threading
import time
from datetime import datetime, timedelta
from utils.JsonManipulators import ReadSchedule, addBreak

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

def validate_value (num,max_val):
    num = int(num)
    if num > max_val:
        return "00"
    elif num < 0:
        return f"{max_val}"
    elif num < 10:
        return f"0{num}"
    return f"{num}"
    
def increment(str, max_val):
    intstr=validate_int(str)
    num = int(intstr)
    num += 1
    num = validate_value(num,max_val)
    return num

def decrement(str, max_val):
    intstr=validate_int(str)
    num = int(intstr)
    num -= 1
    num = validate_value(num,max_val)
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
class TimerValue:
    def __init__(self, addBreak):
        # self.run_stop = run_stop
        self.timerHour = "00"
        self.timerMinute = "00"
        self.timerSecond = "00"
        self.addBreak = addBreak
    def updateHour(self, value):
        self.timerHour = value
    def updateMinute(self, value):
        self.timerMinute = value
    def updateSecond(self, value):
        self.timerSecond = value
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
                if self.break_time>1:
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
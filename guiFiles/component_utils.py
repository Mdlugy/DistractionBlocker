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

class TimerValue:
    def __init__(self, addBreak):
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
        print(self.timerHour)
        print(self.timerMinute)
        print(self.timerSecond)
        seconds = self.convertToSeconds()
        print(seconds)
        self.addBreak(self.convertToSeconds())
    
class DisableButton:
    def __init__(self, button):
        self.enabled = True
        self.button = button
        
    def toggleEnabled(self):
        self.enabled = not self.enabled
        self.button.enabled = self.enabled
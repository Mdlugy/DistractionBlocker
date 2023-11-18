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
        return f"{max_val}"
    elif num < 0:
        return "00"
    elif num < 10:
        return f"0{num}"
    return f"{num}"
    
def increment(str, max_val):
    intstr=validate_int(str)
    num = int(intstr)
    num += 1
    num = validate_value(num,max_val)
    return num

def decrement(str, max_val=max):
    intstr=validate_int(str)
    num = int(intstr)
    num -= 1
    num = validate_value(num,max_val)
    return num

class TimerValue:
    def __init__(self):
        self.timerHour = "00"
        self.timerMinute = "00"
        self.timerSecond = "00"
        
    def convertToSeconds(self):
        return int(self.timerHour)*3600 + int(self.timerMinute)*60 + int(self.timerSecond)
    
class HideButton:
    def __init__(self):
        self.shown = True
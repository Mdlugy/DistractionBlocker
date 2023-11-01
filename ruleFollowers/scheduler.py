# get the current day of the week and time

import datetime
def getDay():
    return datetime.datetime.today().weekday()
# get the schedule.json file
def getSchedule():
    with open('modules/ruleFollowers/schedule.json') as json_file:
        data = json.load(json_file)
        return data
# if the current day is in the schedule.json file, return the time
def todaySched():
    if data[getDay()] != None:
        return data[getDay()]
    else:
        return None
today = todaySched()
# if today is none, return none
if today == None:
    return False
# if today is not none, check if the current time is greater than the start time in the schedule and less than the end time
now = datetime.datetime.now().time()
if today.start < now < today.end:
    return True
return False

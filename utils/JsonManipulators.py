import json
import os
from datetime import datetime
def ReadJSON(fileName):
    file_path = os.path.join("jsonFiles", fileName)
    absolute_file_path = os.path.abspath(file_path)

    if not os.path.exists(absolute_file_path):
        return None
    else:
        with open(absolute_file_path, 'r') as file:
            return json.load(file)
def writeJson(fileName, data):
    file_path = os.path.join("jsonFiles", fileName)
    absolute_file_path = os.path.abspath(file_path) 
    with open(file_path, 'w') as file:
        json.dump(data, file)
    return

def write_json(fileName, data):
    # Define the directory where the JSON file will be saved
    # Construct the full file path
    file_path = os.path.join(directory, fileName)
    
    # Write the JSON data to the file

def ReadPDFs():
    return ReadJSON('PDFs.json')
def ReadBlackList():
    return ReadJSON('blackList.json')
def ReadSchedule():
    return ReadJSON('scheduler.json')

def removeBreak(schedule):
    # set schedule[break] to 0 and write to file
    schedule["break"] = 0
    writeJson('scheduler.json', schedule)

def removeDayOff(schedule):
    # set schedule[break] to 0 and write to file
    today = datetime.now().strftime("%m:%d:%y")
    schedule["DaysOff"].remove(today)
    writeJson('scheduler.json', schedule)

def isBreak():
    Schedule = ReadSchedule()
    breakLeft = Schedule["break"]
    return breakLeft!=0
def addBreak(seconds):
    schedule = ReadSchedule()
    schedule["break"] = seconds
    writeJson('scheduler.json', schedule)
    return
def fixPdfs():
    pdfs = ReadPDFs()
    new=[]
    for pdf in pdfs:
        print(pdf)
        pdf = pdf[:-4]
        new.append(pdf)
        print (pdf)
    writeJson('PDFs.json', new)
    return

def getList(patharr):
    data = ReadJSON(patharr[0])
    for index, item in enumerate(patharr, start=1):
        data = data[item]
    return data

# def setList(data, patharr, value):
#     data = ReadJSON(patharr[0])
#     for index, item in enumerate(patharr, start=1):
#         if index == len(patharr):
#             data[item] = value
#             writeJson(patharr[0], data)
#             return
#         data = data[item]
#     return
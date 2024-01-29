import json
import os
from datetime import datetime
def read_json(fileName):
    file_path = os.path.join("jsonFiles", fileName)
    absolute_file_path = os.path.abspath(file_path)

    if not os.path.exists(absolute_file_path):
        return None
    else:
        with open(absolute_file_path, 'r') as file:
            return json.load(file)
def write_json(fileName, data):
    file_path = os.path.join("jsonFiles", fileName)
    absolute_file_path = os.path.abspath(file_path) 
    with open(file_path, 'w') as file:
        json.dump(data, file)
    return


def read_PDFs():
    return read_json('PDFs.json')
def read_blacklist():
    return read_json('blackList.json')
def read_schedule():
    return read_json('scheduler.json')

def remove_break(schedule):
    # set schedule[break] to 0 and write to file
    schedule["break"] = 0
    write_json('scheduler.json', schedule)

def remove_day_off(schedule):
    # set schedule[break] to 0 and write to file
    today = datetime.now().strftime("%m/%d/%Y")
    schedule["DaysOff"].remove(today)
    write_json('scheduler.json', schedule)

def is_break():
    Schedule = read_schedule()
    break_left = Schedule["break"]
    return break_left!=0
def add_break(seconds):
    schedule = read_schedule()
    schedule["break"] = seconds
    write_json('scheduler.json', schedule)
    return
def fix_pdfs():
    pdfs = read_PDFs()
    new=[]
    for pdf in pdfs:
        print(pdf)
        pdf = pdf[:-4]
        new.append(pdf)
        print (pdf)
    write_json('PDFs.json', new)
    return

def getList(patharr):
    data = read_json(patharr[0])
    for index, item in enumerate(patharr, start=1):
        data = data[item]
    return data

# def setList(data, patharr, value):
#     data = read_json(patharr[0])
#     for index, item in enumerate(patharr, start=1):
#         if index == len(patharr):
#             data[item] = value
#             writejson(patharr[0], data)
#             return
#         data = data[item]
#     return
# DistractionBlocker
A program that runs off a GUI which allows the user to create a blacklist and a timer, then block all of the folders and Executables within those folders while the timer runs. 

before running, please run pip install -r requirements.txt in your terminal to install all the necessary dependancies.

to run, either run main.py in your terminal or, if you've installed WSL you can simply doubleclick the distractionblocker.bat file. 

HOW TO USE:
    please setup the schedule first. you can either edit the JSON file directly, or edit the schedule in the GUI. If you are editing the JSON file please ensure that you are following ("HH:MM:SS") format for start and end times. If you'd like to add days off, please add them in ("01/01/2024") format, comma separated. e.g:["01/01/2024","01/02/2024"]
    
    after setting up the schedule set up the BlackList. (Doing this through the Gui is not yet supported.)

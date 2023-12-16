# DistractionBlocker
A program that runs off a GUI which allows the user to create a blacklist and a timer, then block all of the folders and Executables within those folders while the timer runs. 

before running, please run pip install -r requirements.txt in your terminal to install all the necessary dependencies.

to run, either run main.py in your terminal or, if you've installed WSL you can simply doubleclick the distractionblocker.bat file. 

HOW TO USE
    Schedule Setup
    you can either edit the JSON file directly, or edit the schedule in the GUI. If you are editing the JSON file please ensure that you are following ("HH:MM:SS") format for start and end times. If you'd like to add days off, please add them in ("01/01/2024") format, comma separated. e.g:["01/01/2024","01/02/2024"]
    

    BlackList Setup
    (Doing this through the Gui is not yet supported, this is the next planned feature. For now, please set this up through the blackList.json file.)
    
        JSON explainer
            paths: 
                a comma seperated list of paths. you can copy these directly from your windows explorer. make sure that you replace all instances of "\" with "\\" 
                this should be used for blocking processes which originate inside a folder.
            
                as an example if you have a dedicated drive (I:\) or folder(I:\Games\) for games on your pc and you'd like to block their running you would include "I:\\" or "I:\\Games\\" respectively in this list. 
            titles: 
                a comma seperated list of titles. you can run watch_processes.py and watch the console for the active window title. The current configuration of this project tests to see if the title exists within the current window title before blocking.
            FolderPaths:
                functionally the same as paths, but this list is used for checking which folder is currently open in windows explorer. you can use this list for blocking off windows explorer folders. (same format as path.)
            Urls:
                If you'd like to extend this project to also block certain websites you can include a list of Urls here. As of now, only chrome is supported with this functionality as it exposes this data in a consistent way. You can either include a whole website e.g. "youtube.com", or specific URls e.g. "https://www.youtube.com/watch?v=dQw4w9WgXcQ" 
            SpecialCases:
                This is a somewhat more complicated category. This is a list of objects with the following properties:
                    Label: {string}
                        the name of the program 
                    
                    KillType: "exe" or "window"
                        how the process should be closed. If you would close using (ALT+F4) use "exe", if you would close with (CTRL+W) use "window".

                    case: {string}.
                        the target to show that the process is running
                        e.g.("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe")
                    
                    TestTarget: "path" or "title"
                        where the case is being tested against. (in almost every case it is suggested you use path, however title is supported)

                    WhiteList: a comma seperated list of strings
                        in some cases you want to block all instances of a program running with some exceptions, the exceptions go here

                    BlackListpath: a comma seperated list of strings, or a list which points to an existing blacklist list
                        you can use on of the existing blacklist lists by creating a list with "blackList.json" as the 0 indexed value, with one of the blackList lists as the 1 indexed value, or create a custom list of targets.
                        
                        e.g. ["blackList.json","Urls"] (this will use the Urls list). or e.g.[youtube.com, twitch.tv, facebook.com....]

                    BlockTarget:"title","explorerPath", "path" or "URL"
                        this is the attribute of the currently opened window that we're testing the special case Blacklist/whitelist against to decide wether we close or allow the window to stay open. it is worth running watch_processes.py to decide which target to use. 

                I've included my specialCases portion as an example:
                    "SpecialCases":[
                            {   
                                "Label": "Firefox",
                                "KillType":"exe",
                                "case":"C:\\Program Files\\Mozilla Firefox\\firefox.exe",
                                "TestTarget":"path",
                                "WhiteList":["Firefox Developer Edition"],
                                "BlackListpath":[],
                                "BlockTarget":"title"
                            },
                            {
                                "Label": "Chrome",
                                "KillType":"window",
                                "case":"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
                                "TestTarget":"path",
                                "WhiteList":[],
                                "BlackListpath":["blackList.json","Urls"],
                                "BlockTarget":"URL"
                            },
                            {   
                                "Label": "Explorer",
                                "KillType":"window",
                                "case":"C:\\Windows\\explorer.exe",
                                "WhiteList":[],
                                "TestTarget":"path",
                                "BlackListpath":["blackList.json","FolderPaths"],
                                "BlockTarget":"explorerPath"
                            }
                        ] 
    Running
    either run main.py in the terminal or click on main.bat

    Breaks
    to take a break click the "add a break" button and set how long of a break you'd like to take, then click submit. 5 minutes before the break ends, if you are running a blocked program a popup window will show up that warns you that a break will end in 5 minutes, at which time that window will be closed by the program. 


    Days Off
    the program is setup to run every day with schedules set by days of the week. If you'd like to keep the program running in the background, but have it be inactive, please add the date you'd like it to turn off either through the gui or by editing the scheduler.json. 


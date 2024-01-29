import os
import fnmatch
from ruleFollowers.JsonManipulators import read_JSON, write_Json
def find_extensions_in_dir(directory, extensions):
    for extension in extensions:
        print(extension)
        matched_files = []  # Use a different name to avoid conflict with os.walk files
        jsonName = extension[1:] + "s.json"
 
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                print(file_path) # print all files to track progress
                if fnmatch.fnmatch(file.lower(), f"*{extension}"):
                    matched_files.append(file_path)  # Append the full path
        
        # Read existing data if JSON file exists
        data = read_JSON(jsonName)
        if data == None:
            data = []
        # Add new files to the data list
        for file in matched_files:
            if file not in data:
                data.append(file)
        
        # Write the updated data to the JSON file
        write_Json(jsonName, data)
    
    # The return statement should be here if you want to return something specific
    return

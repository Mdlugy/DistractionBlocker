# import components/componentutils

def add_settings_window(app):
    pass
#  create a window usint create_new_window from components, using app as the parent "settings" "edit"
#  this window will show the current times from the json file for the next week, days off and if there's an active break
#  this window also shows information on blacklisted apps/ websites/ folders
#  there are 3 buttons "close", edit blacklists, edit schedule
# 
# close button just closes the window, there's no difference between closing the window and clicking the x, this just feels like a good stylistic choice

# edit blacklists button opens a new window calls add_blacklist_window from add_blacklist_window (expanded on in that file)
# edit schedule button opens a new window calls add_schedule_window from add_schedule_window (expanded on in that file)
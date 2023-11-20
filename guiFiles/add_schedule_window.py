# import components/componentutils

def add_schedule_window(parent):
    pass
#  create a window usint create_new_window from components, using the parent "settings" "util_edit"
#  this window will show the current times from the json file for the next week, days off and if there's an active break
#  in this window the above information is editable using a custom component called day_schedule for days of the week, and a list of days off for days off

#the days off list is a stateful component which is initialized with the current list of days off, and can be edited using the add and remove buttons the add button is a custom component called add_day which is a text_input (similar to the one in add_break_window, but configured to only accept valid MM/DD/YY dates and a button to add the date to the list of days off. each day besides the empty one has a remove button which removes that day from the list of days off. 

# for the weekdays a similar component from the  add_break_window is used, configured to accept times in the format HH:MM:SS, and a checkbox. if the checkbox is checked the component is greyed out and the start_time and end_time are set to None. if the checkbox is unchecked the component is no longer greyed out and the start_time and end_time are set to 10:00:00 and 18:00:00 respectively as the default values.
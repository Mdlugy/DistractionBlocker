# styles.py

# Define colors
BGcolors = {
    "main": "#7892ac",
    "main_header": "#3c5c7c",
    "main_button": "#3c5c7c",
    "util_run": "#70b8b8",
    "util_run_header": "#7c6b3c",
    "util_run_button": "#7c6b3c",
    "edit": "#ecf3b0",
    "edit_header": "#4e7c3c",
    "edit_button": "#bdd6a6",
    "util_edit": "#7096b8",
    "util_edit_header": "#3c5c7c",
    "util_edit_button": "#3c5c7c",
    
    # "info": "#17a2b8",
    # "light": "#f8f9fa",
    # "dark": "#343a40"
}
TextColors = {
    "main_header": "#cf9d51",
    "main_text": "#ad945a",
    "edit_header": "#ffffff",
    "edit_text": "#216677",
    "util_run_header": "#ffffff",
    "util_run_text": "#b88017",
    "util_edit_header": "#40afaf",
    "util_edit_text": "#3e8db4"
}
# Define fonts
fonts = {
    "default": "Cambria",
    "header": "Impact",
    "button": "Cambria"
}
#  12),
#     "header": "Impact", 20, "bold"),
#     "button": "Cambria", 14)
# Define other styles

# smallButton = {
#     "font": fonts["button"],
#     "width": 10,
#     "height": 1,
#     "bg": BGcolors["edit"],
#     "fg": TextColors["edit_text"],
#     "activebackground": BGcolors["util_edit"],
#     "activeforeground": TextColors["util_edit_text"],
#     "button_padding" :{"padx": 10, "pady": 5}
# }
ButtonPaddings={
    "small": {"padx": 10, "pady": 5},
    "medium": {"padx": 20, "pady": 10},
    "large": {"padx": 30, "pady": 15}
}

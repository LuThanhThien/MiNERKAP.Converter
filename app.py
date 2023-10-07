import os
import tkinter as tk
from src.resize import Resize
from src.utils import *
import customtkinter as ctk
from CTkListbox import *
from src.config import *

# APPERANCE
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# GUI
resizer = Resize()
app = ctk.CTk()
app.title("Image to Word Converter")
app.resizable(False, False) # fixed window size

# Variables to store folder paths
input_folder_var = ctk.StringVar()
output_folder_var = ctk.StringVar(value=os.path.expanduser('~/Desktop'))  # Set the desktop folder as the default value


# row 1 --------------------------------------------------
# Create and configure widgets for selecting output folder
output_folder_label = ctk.CTkLabel(app, text="Select Output Folder:", font=CUSTOMFONT)
output_folder_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

output_folder_entry = ctk.CTkEntry(app, textvariable=output_folder_var, state="readonly")
output_folder_entry.grid(row=0, column=1, padx=5, pady=10, columnspan=2, sticky="ew")

select_output_folder_button = ctk.CTkButton(app, text="Select folder", font=CUSTOMFONT, width=10,\
                                        command=lambda: select_folder(output_folder_var, image_listbox))
select_output_folder_button.grid(row=0, column=4, padx=(0, 10), pady=(10))


# row 2 --------------------------------------------------
# Add a label and entry for user input
repetitions_label = ctk.CTkLabel(app,text="Repetitions per image:", font=CUSTOMFONT)
repetitions_label.grid(row=1, column=0, sticky="w", padx=(10), pady=(10))

repetion_lines_var = ctk.StringVar(value=11)
repetitions_entry = ctk.CTkEntry(app,textvariable=repetion_lines_var)
repetitions_entry.grid(row=1, column=1, padx=(5), pady=(10), sticky="ew")

info_text = ctk.CTkLabel(app, text="(Type in the number of repetitions per image, one line has 11 images by default)",\
                          font=("Helvetica", 12, "italic"))
info_text.grid(row=1, column=2, padx=(5), pady=(10), sticky="w")


# row 3 --------------------------------------------------
select_folder_button = ctk.CTkButton(app, text="Choose images", font=CUSTOMFONT, width=10,\
                                 command=lambda: select_folder(input_folder_var, image_listbox))
select_folder_button.grid(row=2, column=0, padx=(0, 10), pady=(20, 10))

# open_button = ctk.CTkButton(app, text="Open Images", command=open_images(app))
# open_button.grid()

# Create a listbox with a specific height and width
listbox_height = 20
listbox_width = 15
image_listbox = tk.Listbox(app, selectmode=tk.MULTIPLE, height=listbox_height, width=listbox_width, font=CUSTOMFONT)
image_listbox.grid(row=3, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

# Create a scrollbar for the listbox
scrollbar = tk.Scrollbar(app, orient=tk.VERTICAL, command=image_listbox.yview)
scrollbar.grid(row=3, column=5, sticky="ns")
image_listbox.configure(yscrollcommand=scrollbar.set)


# row 4 --------------------------------------------------
# Create the Convert button with the new function
convert_button = ctk.CTkButton(app,text="Convert", height=30, width=50, font=CUSTOMFONT,\
                           command=lambda: resizer.convert_button_click(input_folder_var,output_folder_var,repetion_lines_var))
convert_button.grid(row=4, column=0, padx=10, pady=10, columnspan=4)


app.mainloop()
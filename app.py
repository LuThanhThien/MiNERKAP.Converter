import os
import tkinter as tk
from tkinter import PhotoImage
from src.components.Resizer import Resizer
from src.utils import *
import customtkinter as ctk
from CTkListbox import *
from src.config import *

# APPERANCE
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# GUI
resizer = Resizer()
app = ctk.CTk()
app.title("Image to Word Converter")
app.resizable(False, False) # fixed window size

# Variables to store folder paths
selected_image_paths = []
output_folder_var = ctk.StringVar(value=os.path.expanduser('~/Desktop'))  # Set the desktop folder as the default value


# row 1 --------------------------------------------------
# Create and configure widgets for selecting output folder
output_folder_label = ctk.CTkLabel(app, text="Output Folder:", font=CUSTOMFONT_H1)
output_folder_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

output_folder_entry = ctk.CTkEntry(app, width=450, textvariable=output_folder_var, state="readonly", font=CUSTOMFONT_H1)
output_folder_entry.grid(row=0, column=1, padx=5, pady=10, columnspan=2, sticky="ew")

select_output_folder_button = ctk.CTkButton(app, text="Select folder", width=8, height=28, font=CUSTOMFONT_H1,\
                                        command=lambda: select_folder(output_folder_var, image_listbox))
select_output_folder_button.grid(row=0, column=3, columnspan=1, sticky='w', padx=(0, 10), pady=(10))


# row 2 --------------------------------------------------
# Add a label and entry for user input
repetitions_label = ctk.CTkLabel(app,text="Repetitions per image:", font=CUSTOMFONT_H1)
repetitions_label.grid(row=1, column=0, padx=(10), pady=(10))

repetition_images_var = ctk.StringVar(value=11)
repetitions_entry = ctk.CTkEntry(app,  width=60, textvariable=repetition_images_var, font=CUSTOMFONT_H1)
repetitions_entry.grid(row=1, column=1, padx=(5), pady=(10), sticky="ew")

info_text = ctk.CTkLabel(app, text="(One line has 11 images by default for 16x16mm images)",\
                          font=CUSTOMFONT_H1)
info_text.grid(row=1, column=2, columnspan=2, padx=(5), pady=(10), sticky="w")


# row 3 --------------------------------------------------
select_folder_button = ctk.CTkButton(app, text="Choose images", width=120, height=40, font=CUSTOMFONT_H1,\
                                command=lambda: select_images(selected_image_paths, image_listbox))
select_folder_button.grid(row=2, column=0, padx=(10, 5), pady=(10, 10), sticky='w')

# open_button = ctk.CTkButton(app, text="Open Images", command=open_images(app))
# open_button.grid()

# Create the Delete all images button
delete_all_button = ctk.CTkButton(app, text="Delete All", width=120, height=40, font=CUSTOMFONT_H1, \
                                  command=lambda: delete_all(selected_image_paths, image_listbox))
delete_all_button.grid(row=2, column=1, padx=(0, 5), pady=(10, 10), sticky="w")

# Create a listbox with a specific height and width
listbox_height = 20
listbox_width = 15
image_listbox = tk.Listbox(app, selectmode=tk.MULTIPLE, height=listbox_height, width=listbox_width, font=CUSTOMFONT_H0)
image_listbox.grid(row=3, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

# Create a scrollbar for the listbox
scrollbar = tk.Scrollbar(app, orient=tk.VERTICAL, command=image_listbox.yview)
scrollbar.grid(row=3, column=5, sticky="ns")
image_listbox.configure(yscrollcommand=scrollbar.set)

# row 4 --------------------------------------------------
# Create the Convert button with the new function
convert_button = ctk.CTkButton(app,text="Convert to Docx", height=40, width=120, font=CUSTOMFONT_H1,\
                        command=lambda: resizer.convert_button_click(selected_image_paths, output_folder_var, repetition_images_var))
convert_button.grid(row=4, column=0, padx=10, pady=10, columnspan=4)


app.mainloop()

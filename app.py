import os
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from CTkListbox import *
from src.utils import *
import customtkinter as ctk
from src.config import *
from src.components.imgConverter import Converter
from src.components.imgFrame import ImageFrame

# APPERANCE
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
        def __init__(self):
            super().__init__()

            # GUI
            self.resizer = Converter()
            self.imgFrame = ImageFrame()
            self.title("Image to Word Converter")
            self.resizable(False, False) # fixed window size

            # Variables to store folder paths
            self.inputImages = {
                'path': [],
                'shape': [],
                'copies': [],
                'px_width': [],
                'px_height': [],
                'xc': [],
                'yc': [],
                'selected': [],
            }
            
            # frame 1: parameters frame --------------------------------------------------
            self.param_frame = ctk.CTkFrame(self)
            self.param_frame.grid(row=0, column=0, padx=(15, 15), pady=(15, 0), sticky="nsew")

            # row 1 
            # Create and configure widgets for selecting output folder
            self.output_folder_var = ctk.StringVar(value=DEFAULT_OUTPUT)  # Set the desktop folder as the default value
            self.output_folder_label = ctk.CTkLabel(master=self.param_frame, text="Output:", font=CUSTOMFONT_H1)
            self.output_folder_label.grid(row=0, column=0, sticky="w", padx=PADX_START, pady=PADY_START)

            self.output_folder_entry = ctk.CTkEntry(master=self.param_frame, width=400, textvariable=self.output_folder_var, state="readonly",\
                                                     font=CUSTOMFONT_H1)
            self.output_folder_entry.grid(row=0, column=1, padx=PADX, pady=PADY_START, columnspan=3, sticky="w")

            self.select_output_folder_button = ctk.CTkButton(master=self.param_frame, text="Select folder", width=8, height=28, font=CUSTOMFONT_H1,\
                                                    command=lambda: select_folder(self.output_folder_var))
            self.select_output_folder_button.grid(row=0, column=5, sticky='w', padx=PADX_END, pady=PADY_START)

            # row 2
            # Add a label and entry for user input
            self.copies_label = ctk.CTkLabel(master=self.param_frame, text="Copies:", font=CUSTOMFONT_H1)
            self.copies_label.grid(row=1, column=0, padx=PADX_START, pady=PADY_END, sticky='w')

            self.copies_var = ctk.StringVar(value=DEFAULT_PARAMS['copies'])
            self.copies_entry = ctk.CTkEntry(master=self.param_frame, width=50, textvariable=self.copies_var, font=CUSTOMFONT_H1)
            self.copies_entry.grid(row=1, column=1, padx=PADX, pady=PADY_END, sticky="w")


            # Create a label for the shape selection
            self.shape_label = ctk.CTkLabel(master=self.param_frame, text="Shape:", font=CUSTOMFONT_H1)
            self.shape_label.grid(row=1, column=2, padx=PADX, pady=PADY_END, sticky='w')

            # Create a Combobox for shape selection
            self.shape_combobox = ctk.CTkComboBox(master=self.param_frame, values=list(IMG_SHAPES.keys()), font=CUSTOMFONT_H1)
            self.shape_combobox.grid(row=1, column=3, padx=PADX, pady=PADY_END, sticky="w")

            # frame 2: Button and list box
            self.imgbox_frame = ctk.CTkFrame(self)
            self.imgbox_frame.grid(row=1, column=0, padx=(15, 15), pady=(10, 0), sticky="nsew")

            # row 3
            self.select_folder_button = ctk.CTkButton(master=self.imgbox_frame, text="Choose images", width=120, height=40, font=CUSTOMFONT_H1,\
                                            command=lambda: self.imgFrame.add_images())
            self.select_folder_button.grid(row=2, column=0, padx=(10, 5), pady=(10, 10), sticky='w')

            # open_button = ctk.CTkButton( text="Open Images", command=open_images(app))
            # open_button.grid()

            # Create the Delete all images button
            self.delete_all_button = ctk.CTkButton(master=self.imgbox_frame, text="Delete All", width=120, height=40, font=CUSTOMFONT_H1, \
                                            command=lambda: self.imgFrame.delete_images(detype='all'))
            self.delete_all_button.grid(row=2, column=1, padx=(0, 5), pady=(10, 10), sticky="w")

            # Create a listbox with a specific height and width

            self.image_listbox = tk.Listbox(master=self.imgbox_frame, selectmode=tk.MULTIPLE, font=CUSTOMFONT_H0)
            self.image_listbox.grid(row=3, column=0, padx=10, pady=10, columnspan=6, sticky="nsew")

            # Initiate image frame for image management
            self.imgFrame.initiate_frame_obj(img_listbox=self.image_listbox, default_copies=self.copies_entry.get(),\
                                              default_shape=self.shape_combobox.get())
            self.image_listbox = self.imgFrame.img_listbox

            # Create a scrollbar for the listbox
            self.scrollbar = tk.Scrollbar(master=self.imgbox_frame, orient=tk.VERTICAL, command=self.image_listbox.yview)
            self.scrollbar.grid(row=3, column=6, sticky="nsw")
            self.image_listbox.configure(yscrollcommand=self.scrollbar.set)

            # row 4 --------------------------------------------------
            # Create the Convert button with the new function
            self.convert_button = ctk.CTkButton(master=self.imgbox_frame, text="Convert to Docx", height=40, width=120, font=CUSTOMFONT_H1,\
                                    command=lambda: self.resizer.convert_button_click(self.imgFrame.inputImages,\
                                                                                       self.output_folder_var, self.copies_entry))
            self.convert_button.grid(row=4, column=0, padx=10, pady=10)    


        # Function to update the selected shape
        def update_shape(self, event):
            selected_shape = self.shape_combobox.get()
            if selected_shape in IMG_SHAPES:
                # Use IMG_SHAPES[selected_shape] to access the selected shape's dimensions
                print(f"Selected Shape: {selected_shape}, Dimensions: {IMG_SHAPES[selected_shape]}")
            else:
                print("Invalid shape selected")
                
if __name__ == "__main__":
    app = App()
    app.mainloop()

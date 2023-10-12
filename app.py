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
import warnings
import time

# Filter out the specific warning message
warnings.filterwarnings("ignore")

# APPERANCE
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
        def __init__(self):
            super().__init__()

            # GUI
            self.converter = Converter()
            self.converter.initiate_converter(self)
            self.imgFrame = ImageFrame()
            self.imgFrame.initiate_frame_obj(self)
            self.title("Image to Word Converter")
            self.resizable(False, False) # fixed window size
            
            # row 0, frame 1: parameters frame ----------------------------------------------------------------------------------
            self.param_frame = ctk.CTkFrame(self)
            self.param_frame.grid(row=0, column=0, padx=(15, 15), pady=(15, 0), sticky="nsew")
            
            # Add a label and entry for user input
            self.copies_label = ctk.CTkLabel(master=self.param_frame, text="Copies:", font=CUSTOMFONT_H1)
            self.copies_label.grid(row=0, column=0, padx=PADX_ONI, pady=PADY_ONI, sticky='w')

            self.copies_var = ctk.StringVar()
            self.copies_entry = ctk.CTkEntry(master=self.param_frame, width=60, textvariable=self.copies_var, font=CUSTOMFONT_H1)
            self.copies_entry.grid(row=0, column=1, padx=0, pady=PADY_ONI, sticky="nsew")


            # Create a label for the shape selection
            self.shape_label = ctk.CTkLabel(master=self.param_frame, text="Shape:", font=CUSTOMFONT_H1)
            self.shape_label.grid(row=0, column=2, padx=PADX_ONI, pady=PADY_ONI, sticky='e')

            # Create a options for shape selection
            self.shape_var = ctk.StringVar()
            self.shape_options = ctk.CTkOptionMenu(master=self.param_frame, values=list(IMG_SHAPES.keys()), font=CUSTOMFONT_H1,\
                                                   variable=self.shape_var)
            self.shape_options.grid(row=0, column=3, padx=0, pady=PADY_ONI, sticky="w")

            # Create and configure widgets for selecting output folder
            self.output_folder_var = ctk.StringVar(value=DEFAULT_OUTPUT)  # Set the desktop folder as the default value
            self.output_folder_label = ctk.CTkLabel(master=self.param_frame, text="Output:", font=CUSTOMFONT_H1)
            self.output_folder_label.grid(row=0, column=4, sticky="w", padx=(40,15), pady=PADY_ONI)

            self.output_folder_entry = ctk.CTkEntry(master=self.param_frame, width=500, textvariable=self.output_folder_var,\
                                                     state="readonly", font=CUSTOMFONT_H1)
            self.output_folder_entry.grid(row=0, column=5, padx=0, pady=PADY_ONI, columnspan=3, sticky="w")

            self.select_output_folder_button = ctk.CTkButton(master=self.param_frame, text="Select folder", width=8, height=28, font=CUSTOMFONT_H1,\
                                                    command=self.select_output_click)
            self.select_output_folder_button.grid(row=0, column=9, sticky='w', padx=PADX_ONI, pady=PADY_ONI)


            # row 1 ----------------------------------------------------------------------------------
            self.add_images_button = ctk.CTkButton(master=self, text="Add images", width=120, height=40,\
                                                    font=CUSTOMFONT_H1, command=self.add_images_click)
            self.add_images_button.grid(row=1, column=0, padx=PADX_START, pady=PADY_START, sticky='w')


            # Create the Delete all images button
            self.delete_all_button = ctk.CTkButton(master=self, text="Delete All", width=120, height=40,\
                                                   font=CUSTOMFONT_H1, command=self.delete_click)
            self.delete_all_button.grid(row=1, column=0, padx=(120+40,5), pady=PADX_START, sticky="w")
    

            # row 2, frame 2: Images frame ----------------------------------------------------------------------------------
            # Trace for var change 
            self.copies_var.trace('w', self.var_change)
            self.shape_var.trace('w', self.var_change)

            self.scrollImageFrame = ctk.CTkScrollableFrame(self, width=CANVAS_WIDTH-150, height=CANVAS_HEIGHT)
            self.scrollImageFrame.grid(row=2, column=0, padx=(15, 15), pady=(15, 0), sticky="nsew")

            # row 3 ----------------------------------------------------------------------------------
            # Create the Convert button with the new function
            self.convert_button = ctk.CTkButton(master=self, text="Convert to Docx", height=40, width=120, font=CUSTOMFONT_H1,\
                                    command=self.convert_click)
            self.convert_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)    


        # frame functions    
        def ScrollableImageFrame(self):
            # Delete old widgets in frame
            for widget in self.scrollImageFrame.grid_slaves():
                # Remove the widget from the grid
                widget.destroy()    
            
            # Reset frame
            self.scrollImageFrame = ctk.CTkScrollableFrame(self, width=CANVAS_WIDTH-150, height=CANVAS_HEIGHT)
            self.scrollImageFrame.grid(row=2, column=0, padx=(15, 15), pady=(15, 0), sticky="nsew")

            # Create a grid of labels to display the resized images
            for i, (photo, name) in enumerate(zip(self.imgFrame.inputImages['Image'], self.imgFrame.inputImages['name'])):
                row = 2 * (i // IMAGES_PER_COLUMN)
                col = i % IMAGES_PER_COLUMN
                
                if len(name)>MAX_NAME_LENGTH:
                    name = name[:MAX_NAME_LENGTH] + "..." + name.split('.')[-1]
                
                image_label = ctk.CTkLabel(self.scrollImageFrame, image=photo)
                image_label.image = photo
                image_label.grid(row=row, column=col, padx=(10, 10), pady=(5, 5))

                name_label = ctk.CTkLabel(self.scrollImageFrame, text=name, font=CUSTOMFONT_H1)
                name_label.grid(row=row+1, column=col, padx=(10, 10), pady=(5, 20))  # Place the name label below the image label      

        # Trace the change for params
        def var_change(self, *args):
            self.imgFrame.update_params(ids=[i for i in range(len(self.imgFrame.inputImages['path']))],\
                                        update_copies=self.copies_var.get(), update_shape=self.shape_options.get())
            loggingInfo('[App] Change and update new parameters.')  


        # Buttons click
        def select_output_click(self):
            select_folder(self.output_folder_var)

        def add_images_click(self):
            self.imgFrame.add_images()
            self.ScrollableImageFrame()

        def convert_click(self):
            self.converter.convert_button_click(self.imgFrame.inputImages, self.output_folder_var)

        def delete_click(self):
            self.imgFrame.delete_images(detype='all')
            print(self.imgFrame.inputImages)
            self.ScrollableImageFrame()


if __name__ == "__main__":
    app = App()
    app.mainloop()

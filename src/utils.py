import os, sys
import tkinter as tk
from PIL import Image, ImageTk, ImageOps
from io import BytesIO
from tkinter import filedialog
import customtkinter as ctk
from PIL import Image
from src.logger import logging
from src.exception import CustomException
from src.config import *


def loggingInfo(text_to_print:str) -> logging.info:
    print(text_to_print)
    return logging.info(text_to_print)


# Function to handle folder selection
def select_folder(folder_var) -> None:
    """
    This function as button to select the folder (for output specifically)
    """
    try:
        folder_path = filedialog.askdirectory()
        if folder_path:
            folder_var.set(folder_path)
    except Exception as e:
        raise CustomException(e, sys)


# Function to crop an image to square
def crop_to_square(image_path:BytesIO) -> Image.Image:
        """
        This function crop an image into a square form 
        """
        img = Image.open(image_path)

        if img.width != img.height:
            min_dimension = min(img.width, img.height)
            left = (img.width - min_dimension) / 2
            top = (img.height - min_dimension) / 2
            right = (img.width + min_dimension) / 2
            bottom = (img.height + min_dimension) / 2
            img = img.crop((left, top, right, bottom))
        
        img = img.convert("RGB")

        return img



def open_images(root):
    file_paths = filedialog.askopenfilenames(filetypes=IMG_TYPES)
    if file_paths:
        images = []
        image_names = []

        for file_path in file_paths:
            image = Image.open(file_path)
            
            # Add padding for those images not square
            width, height = image.size
            if width > height:
                padding = (width - height) // 2
                image = ImageOps.expand(image, border=(0, padding, 0, padding), fill='white')
            elif height > width:
                padding = (height - width) // 2
                image = ImageOps.expand(image, border=(padding, 0, padding, 0), fill='white')
            

            # Resize the image to the fixed width and height
            image = image.resize((IMAGE_WIDTH, IMAGE_HEIGHT), Image.ANTIALIAS)
            
            photo = ImageTk.PhotoImage(image)
            images.append(photo)

            # Get the base filename (without path) for the image
            image_name = os.path.basename(file_path)
            image_names.append(image_name)

         # Create a Canvas widget for the scrollable area
        canvas = ctk.CTkCanvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        canvas.grid(row=0, column=0)

        # Create a Frame inside the Canvas to hold the images
        frame = ctk.CTkFrame(canvas)
        canvas.create_window((0, 0), window=frame, anchor='nw')

        # Create a grid of labels to display the resized images
        for i, (photo, name) in enumerate(zip(images, image_names)):
            row = 2 * (i // NUM_COLUMNS)
            col = i % NUM_COLUMNS
            
            if len(name)>MAX_NAME_LENGTH:
                name = name[:MAX_NAME_LENGTH] + "..." + name.split('.')[-1]
            
            image_label = ctk.CTkLabel(frame, image=photo)
            image_label.image = photo
            image_label.grid(row=row, column=col, padx=5, pady=5)

            name_label = ctk.CTkLabel(frame, text=name)
            name_label.grid(row=row+1, column=col, padx=5)  # Place the name label below the image label

         # Add a scrollbar for the Canvas to enable scrolling
        scrollbar = ctk.CTkScrollbar(root, orient='vertical', command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        canvas.config(yscrollcommand=scrollbar.set)

        # Bind the Canvas to the scrolling event
        def on_canvas_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        frame.bind("<Configure>", on_canvas_configure)
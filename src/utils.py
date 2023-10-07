import os
import tkinter as tk
from PIL import Image, ImageTk, ImageOps
from io import BytesIO
from tkinter import filedialog, messagebox, ttk
from PIL import Image
from src.logger import logging
import customtkinter as ctk
from src.config import *


def loggingInfo(text_to_print:str) -> logging.info:
    print(text_to_print)
    return logging.info(text_to_print)


def format_time(seconds:int) -> str:
    minutes, seconds = divmod(seconds, 60)
    if minutes == 0:
        results = f'{seconds:.3f} second(s)'
    else: results = f'{minutes:.0f} minute(s) {seconds:.3f} second(s)'
    return results


# Function to reset the listbox focus when an item is clicked
def reset_focus(event) -> None:
    event.widget.selection_clear(0, tk.END)
    event.widget.focus_set()


# Function to handle folder selection
def select_folder(folder_var, image_listbox) -> None:
    folder_path = filedialog.askopenfilenames(filetypes=IMG_TYPES)
    if folder_path:
        folder_var.set(folder_path)
        # Clear existing entries from the CTkListbox
        image_listbox.delete(0, image_listbox.size())  # Clear all existing entries
        
        # List image files in the selected folder and update the CTkListbox
        image_files = list_image_files(folder_path)
        for image_file in image_files:
            image_listbox.insert(tk.END, os.path.basename(image_file))


# Function to check if an image exceeds the size limit
def is_exceed_limit(image_file:str) -> bool:
    try:
        _ = Image.open(image_file)
        return True
    except Exception as e:
        return False


# Function to confirm with the user whether to continue with images exceeding the size limit
def confirm_large_images(exceeding_images:list) -> bool:
    if not exceeding_images:
        return True  # No images exceeded the size limit, continue with the process

    # Generate a message with the list of exceeding images
    message = f"Found images exceed the size limit and will be excluded.\n\n"
    message += "\n\nDo you want to continue?"

    response = messagebox.askquestion("Image Size Warning", message)
    return response.lower() == "yes"


# Function to list image files in a folder
def list_image_files(folder_path:str) -> list:
    """
        This function list out all the images with extension in IMG_EXTENSIONS in the input folder
    """
    
    image_files = []

    for filename in os.listdir(folder_path):
        if any(filename.lower().endswith(ext) for ext in IMG_EXTENSIONS):
            image_files.append(os.path.join(folder_path, filename))

    return image_files


# Function to crop an image to square
def crop_to_square(image_file:BytesIO) -> Image.Image:
        img = Image.open(image_file)

        if img.width != img.height:
            min_dimension = min(img.width, img.height)
            left = (img.width - min_dimension) / 2
            top = (img.height - min_dimension) / 2
            right = (img.width + min_dimension) / 2
            bottom = (img.height + min_dimension) / 2
            img = img.crop((left, top, right, bottom))
        
        img = img.convert("RGB")

        return img

# Function to add image files to the list of selected files
def add_image_files(selected_image_files, selected_files_listbox):
    file_paths = filedialog.askopenfilenames(
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp"), ("All Files", "*.*")]
    )
    for file_path in file_paths:
        selected_image_files.append(file_path)
        selected_files_listbox.insert(tk.END, os.path.basename(file_path))


def open_images(root):
    file_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.ppm *.pgm")])
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
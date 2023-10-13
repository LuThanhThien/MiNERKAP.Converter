import os, sys
import tkinter as tk
from PIL import Image, ImageTk, ImageOps
from io import BytesIO
from tkinter import filedialog
from tkinter import messagebox
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

def confirm_delete_images(detype:str, ids:list):
    try:
        if detype == 'all':
            message = "All images will be deleted. Do you want to continue?"

            response = messagebox.askquestion("Delete all images", message)
        elif detype == 'batch':
            message = f"{len(ids)} images will be deleted. Do you want to continue?"

            response = messagebox.askquestion("Delete images", message)
        return response.lower() == "yes"
    
    
    except Exception as e:
        raise CustomException(e, sys)
    
# Function to check if an image exceeds the size limit
def is_exceed_limit(image_path:str) -> bool:
    """
    This helps converting process avoid large resolution/size images
    """
    try:
        _ = Image.open(image_path)
        return True
    except Exception as e:
        return False


# Function to confirm with the user whether to continue with images exceeding the size limit
def confirm_large_images(exceeding_images:list) -> bool:
    """
    This function araise when there is an image exceeding limit size found.
    Give user options whether to continue with passing those images or stop the converting process.
    """
    try:
        if not exceeding_images:
            return True  # No images exceeded the size limit, continue with the process

        # Generate a message with the list of exceeding images
        message = f"Found images exceed the size limit and will be excluded.\n\n"
        message += "\n\nDo you want to continue?"

        response = messagebox.askquestion("Image Size Warning", message)
        return response.lower() == "yes"

    except Exception as e:
        raise CustomException(e, sys)


def crop_img(img:Image.Image, px_width, px_height, xc, yc) -> Image.Image:
        try:
            # Calculate the crop box coordinates
            left = xc - (px_width / 2)
            top = yc - (px_height / 2)
            right = xc + (px_width / 2)
            bottom = yc + (px_height / 2)
            # Crop the image
            cropped_img = img.crop((left, top, right, bottom))
            cropped_img = cropped_img.convert("RGB")

            return cropped_img
        except Exception as e:
            raise CustomException(e, sys)
        
def from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb   
import os
import tkinter as tk
from io import BytesIO
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from PIL import Image
import PIL
from docx import Document
from docx.shared import Mm
from datetime import datetime
from src.exception import CustomException
from src.logger import logging


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



import os, sys
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from docx import Document
from docx.shared import Mm
from datetime import datetime
from src.config import *
from src.exception import CustomException
from src.logger import logging
from src.utils import *
from src.config import IMG_EXTENSIONS

class Resize:
    def __init__(self) -> None:
        self.output_folder:str = None
        self.selected_image_paths:list = []
        self.repetition_images:int = None
        
        
    # Define a function to handle the Convert button click
    def convert_button_click(self, selected_image_paths, output_folder_var, repetition_images_var):
        self.output_folder = output_folder_var.get()
        self.selected_image_paths = selected_image_paths
        repetition_images_str = repetition_images_var.get()

        if not self.output_folder:
            messagebox.showwarning("Warning", f"Please, select the output folder!")
            return
        
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        if not self.selected_image_paths:
            messagebox.showwarning("Warning", f"No image has been selected!")
            return

        if not repetition_images_str:
            messagebox.showwarning("Warning", "Please enter a value for Repetition Lines.")
            return

        try:
            self.repetition_images = int(repetition_images_str)  
        except Exception as e:
            messagebox.showwarning("Warning", "Repetition Lines must be a valid integer.")
            return

        self.create_word_document()


    def create_word_document(self) -> None:
        doc = Document()
        exceeding_images = []


        loggingInfo(f"Converting {len(self.selected_image_paths)} images in process.")
        
        # Set page margins (0.5 inch for all borders)
        section = doc.sections[0]
        section.left_margin = Mm(12.7)  # 0.5 inch
        section.right_margin = Mm(12.7)  # 0.5 inch
        section.top_margin = Mm(12.7)  # 0.5 inch
        section.bottom_margin = Mm(12.7)  # 0.5 inch
        
        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        output_path = os.path.join(self.output_folder, f"{current_time}.docx")

        
        for image_path in self.selected_image_paths:
            
            is_exceed = is_exceed_limit(image_path)
            
            if not is_exceed and len(exceeding_images)!=0:
                exceeding_images.append(image_path)    
                continue
            
            if not is_exceed:         
                exceeding_images.append(image_path)   
                stop_sign = confirm_large_images(exceeding_images)

                if not stop_sign:
                    messagebox.showinfo("Info", "Operation canceled.")
                    loggingInfo("User cancaled converting process due to high resolution images.")
                    return
            
                continue
            
            # Crop the image to square and convert to RGB
            img = crop_to_square(image_path)
            
            if img is None:
                continue  # Skip this image and continue with the next one

            # Add the picture to the paragraph with repetitions
            img.save("temp_square_image.jpg")  # Save the square image temporarily
            
            # Repeat the image in the same line
            run = doc.add_paragraph().add_run()
            for _ in range(self.repetition_images):
                run.add_picture("temp_square_image.jpg", width=Mm(16), height=Mm(16))
                run.add_text(" ")
            
            
            os.remove("temp_square_image.jpg")  # Remove the temporary file
        
        if len(exceeding_images)>0:
            loggingInfo(f"Found {len(exceeding_images)} high resolution images")
        
        if len(exceeding_images) == len(self.selected_image_paths):
            messagebox.showwarning("Warning", "All images are exceeding the maximum size. \
                                   Please, choose another folder or resize your images!")
            loggingInfo("Converting process stopped. All images are high resolution.")
        else:    
            doc.save(output_path)
            messagebox.showinfo("Success", f"Document saved to:\n{output_path}")
            loggingInfo(f"Converted {len(self.selected_image_paths) - len(exceeding_images)} images completely. Document saved to:\n{output_path}")
        

    
            
    
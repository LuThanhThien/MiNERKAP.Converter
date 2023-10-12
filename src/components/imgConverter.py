import os, sys
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from docx import Document
from docx.shared import Mm, Pt
from docx.enum.text import WD_LINE_SPACING
from datetime import datetime
from src.config import *
from src.exception import CustomException
from src.logger import logging
from src.utils import *
from src.config import *
from src.components import imgIngestion, imgFrame


class Converter:
    def __init__(self) -> None:
        self.output_folder:str 
        self.root = None
        

    def initiate_converter(self, root):
        self.root = root

    # Define a function to handle the Convert button click
    def convert_button_click(self, inputImages, output_folder_var):
        try:
            self.output_folder = output_folder_var.get()


            if not self.output_folder:
                messagebox.showwarning("Warning", f"Please, select the output folder!")
                return
            
            if not os.path.exists(self.output_folder):
                os.makedirs(self.output_folder)

            if not inputImages['path']:
                messagebox.showwarning("Warning", f"No image has been selected!")
                return

            self.create_word_document(inputImages)

        except Exception as e:
            raise CustomException(e, sys)


    def create_word_document(self, inputImages:dict) -> None:
        try:
            doc = Document()

            loggingInfo(f"[ImageConverter] Converting {len(inputImages['path'])} images in process.")
            
            
            # Docx set up
            section = doc.sections[0]
            section.left_margin = Mm(12.7)  
            section.right_margin = Mm(12.7)  
            section.top_margin = Mm(12.7)  
            section.bottom_margin = Mm(12.7)  

            style = doc.styles['Normal']
            style.paragraph_format.space_before = Pt(0)  
            style.paragraph_format.space_after = Pt(3)  
            
            current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            output_path = os.path.join(self.output_folder, f"{current_time}.docx")

            
            for image_path, copies, shape in zip(inputImages['path'], inputImages['copies'], inputImages['shape']):
                copies = int(copies)
        
                # Crop the image to square and convert to RGB
                img = Image.open(image_path)

                iwidth, iheight = img.size
                iRatio = iwidth / iheight    
                xc, yc = iwidth//2, iheight//2

                # select min edge
                iheight = None if iRatio < 1 else iheight
                iwidth = None if iRatio > 1 else iwidth
    
                ingestor = imgIngestion.ImageIngestion()
                ingestor.initiate_image_obj(img, px_height=iheight, px_width=iwidth, xc=xc, yc=yc)

                img = ingestor.crop_by_shape(shape=shape)
                
                if img is None:
                    continue  # Skip this image and continue with the next one
                
                if shape != 'Combo':
                    # Add the picture to the paragraph with copies           
                    img.save("temp_image.jpg")  # Save the square image temporarily

                    # Repeat the image in the same line
                    run = doc.add_paragraph().add_run()
                    for _ in range(copies):
                        run.add_picture("temp_image.jpg", width=Mm(IMG_SHAPES[shape][1]), height=Mm(IMG_SHAPES[shape][0]))
                        run.add_text(" ")  
                    os.remove("temp_image.jpg")  # Remove the temporary file
                else:
                    for _ in range(copies):
                        for key, image in img.items():
                            image.save("temp_image.jpg")  # Save the square image temporarily
                            
                            if key != 'Win':
                                paragraph = doc.add_paragraph()
                                run = paragraph.add_run()
                                # Set line spacing for the paragraph
                                paragraph_format = paragraph.paragraph_format
                                paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE

                            run.add_picture("temp_image.jpg", height=Mm(IMG_SHAPES[key][0]))        
                            run.add_text(" ")
                            
                            os.remove("temp_image.jpg")  # Remove the temporary file
                
            doc.save(output_path)
            messagebox.showinfo("Success", f"Document saved to:\n{output_path}")
            loggingInfo(f"[ImageConverter] Converted {len(inputImages['path'])} images completely. Document saved to: {output_path}")
        
        except Exception as e:
            raise CustomException(e, sys)

    
            
    
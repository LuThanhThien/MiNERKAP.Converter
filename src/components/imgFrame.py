import os, sys
from PIL import Image
from src.logger import logging
from tkinter import messagebox
from src.exception import CustomException
from src.utils import *
from src.config import *


def confirm_delete_images(detype:str):
    try:
        if detype == 'all':
            # Generate a message with the list of exceeding images
            message = "All images will be deleted. Do you want to continue?"

            response = messagebox.askquestion("Delete all images", message)
        return response.lower() == "yes"
    
    except Exception as e:
        raise CustomException(e, sys)


class ImageFrame:
    def __init__(self) -> None:
        self.inputImages:dict = {
                'path': [],
                'shape': [],
                'copies': [],
                'px_width': [],
                'px_height': [],
                'xc': [],
                'yc': [],
                'selected': [],
            }
        self.img_listbox = None 
        self.default_shape:str
        self.default_copies:int


    def initiate_frame_obj(self, img_listbox, default_shape, default_copies):
        try:
            self.img_listbox = img_listbox

            if not default_copies:
                messagebox.showwarning("Warning", "Please enter a value for number of copies")
                return
            try:
                self.copies = int(default_copies)  
            except Exception as e:
                messagebox.showwarning("Warning", "Number of copies must be a valid integer.")
                raise CustomException(e, sys)
            
            self.default_copies = default_copies
            
            if default_shape not in IMG_SHAPES.keys():
                raise CustomException(f"Default shape must be in {IMG_SHAPES.keys()}")
                
            
            self.default_shape = default_shape
            loggingInfo("[ImageFrame] Initiated image frame completely.")

        except Exception as e:
            raise CustomException(e, sys)
    
    
    def initiate_image(self):
        try:
            self.inputImages['shape'].append(self.default_shape)
            self.inputImages['copies'].append(self.default_copies)
            self.inputImages['px_width'].append(IMG_SHAPES[self.inputImages['shape'][-1]][0])
            self.inputImages['px_height'].append(IMG_SHAPES[self.inputImages['shape'][-1]][1])
            self.inputImages['selected'].append(1)
            try:
                img = Image.open(self.inputImages['path'][-1])
                iwidth, iheight = img.size
                self.inputImages['xc'].append(iwidth//2) 
                self.inputImages['yc'].append(iheight//2)
            except Exception as e:
                self.inputImages['xc'].append(0) 
                self.inputImages['yc'].append(0)
                raise CustomException(e, sys)

        except Exception as e:
            raise CustomException(e, sys)
    
    def update_frame(self, default_):
        pass

    def add_images(self):
        """
        This function allow users to add images to the list
        """
        try:
            file_paths = filedialog.askopenfilenames(filetypes=IMG_TYPES)
            init_len = len(self.inputImages['path'])

            if file_paths:
                for path in file_paths: 
                    if path not in self.inputImages['path']:
                        self.inputImages['path'].append(path)
                        image_name = os.path.basename(path) 
                        self.initiate_image()
                        self.img_listbox.insert(tk.END, image_name)

            last_len = len(self.inputImages['path'])
            loggingInfo(f"[ImageFrame] Total new {last_len-init_len} image(s) added to image frame.")            
            print(self.inputImages)
        except Exception as e:
            raise CustomException(e, sys)
    
    def crop_window(self):
        pass

    def delete_images(self, detype:str):
        try:
            
            # if no images in list, do nothing
            if len(self.inputImages['path'])==0:
                return
            
            # assert deleting type
            if detype not in ['all', 'batch']:
                loggingInfo(f"[ImageFrame] Undefined delete type {detype}")
                raise CustomException(f"Delete type {detype} is not defined", sys)
            

            init_len = len(self.inputImages['path'])

            if detype == 'all':
                is_delete = confirm_delete_images(detype=detype)

                if is_delete:
                    loggingInfo(f"[ImageFrame] Deleting all images.")
                    self.inputImages['path'].clear()
                    self.img_listbox.delete(0, tk.END)

            elif detype == 'batch':
                del_img = []
                loggingInfo(f"[ImageFrame] Deleting {len(del_img)} selected images.")

            last_len = len(self.inputImages['path'])
            loggingInfo(f"[ImageFrame] Total {init_len-last_len} image(s) deleted from image frame.")

        except Exception as e:
            raise CustomException(e, sys)

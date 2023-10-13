import os, sys
from PIL import Image
from src.logger import logging
from src.exception import CustomException
from src.utils import *
from src.config import *
from PIL import Image, ImageTk
from customtkinter import CTkImage


class ImageFrame:
    def __init__(self) -> None:
        self.root = None
        self.inputImages:dict = {
                'path': [],
                'shape': [],
                'copies': [],
                'px_width': [],
                'px_height': [],
                'xc': [],
                'yc': [],
                'selected': [],
                'name': [],
                'Image': [],
            }
        self.gridImageFrames = []
        self.selectedIndices = []
        self.default_shape:str
        self.default_copies:int


    def initiate_frame_obj(self, root):
        try:
            self.root = root
            self.default_copies = DEFAULT_PARAMS['copies']
            self.default_shape = DEFAULT_PARAMS['shape']
            loggingInfo("[ImageFrame] Initiated image frame completely.")

        except Exception as e:
            raise CustomException(e, sys)
    
    
    def initiate_images(self):
        try:
            self.inputImages['shape'].append(self.default_shape)
            self.inputImages['copies'].append(self.default_copies)
            self.inputImages['px_width'].append(IMG_SHAPES[self.inputImages['shape'][-1]][0])
            self.inputImages['px_height'].append(IMG_SHAPES[self.inputImages['shape'][-1]][1])
            self.inputImages['selected'].append(0)
            self.inputImages['name'].append(os.path.basename(self.inputImages['path'][-1]))

            # open image for image frame
            
            image = Image.open(self.inputImages['path'][-1])

            # Add padding for those images not square
            width, height = image.size
            iRatio = width / height
            if width > height:
                image = image.resize((FRAME_WIDTH + 100, int((FRAME_WIDTH + 100) / iRatio)))
            elif height >= width:
                image = image.resize((int(iRatio * (FRAME_HEIGHT + 100)), FRAME_HEIGHT + 100))
            # Resize the image to the fixed width and height
            
            photo = ImageTk.PhotoImage(image)
            self.inputImages['Image'].append(photo)

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

    def add_images(self):
        """
        This function allow users to add images to the list
        """
        try:
            file_paths = filedialog.askopenfilenames(filetypes=IMG_TYPES)
            init_len = len(self.inputImages['path'])
            exceed_names = []
        
            if file_paths:
                for path in file_paths: 
                    is_exceed = is_exceed_limit(path)
                    if not is_exceed:
                        exceed_names.append(os.path.basename(path))
                        continue
                    if path not in self.inputImages['path']:
                            self.inputImages['path'].append(path)
                            self.initiate_images()       
           
                if len(exceed_names) > 0 and len(exceed_names) < len(file_paths):
                    messagebox.showwarning('Warning', """Some images were not loaded due to exceeding limit size error""")
                elif len(exceed_names) == len(file_paths):
                    messagebox.showwarning('Warning', 'All selected images are exceeding limit size! \n Please choose other images.')
                

            last_len = len(self.inputImages['path'])
            loggingInfo(f"[ImageFrame] Total new {last_len-init_len} image(s) added to image frame.")            
            # print(self.inputImages)
        except Exception as e:
            raise CustomException(e, sys)
    
    
    def update_params(self, ids, params:str=None, update_shape:str=None, update_copies:int=None):
        try:
            if params == None:
                return
            
            for i in ids:
                if params == 'shape' or params == 'all':
                    self.inputImages['shape'][i] = update_shape
                    self.inputImages['px_width'][i] = IMG_SHAPES[self.inputImages['shape'][i]][0]
                    self.inputImages['px_height'][i] = IMG_SHAPES[self.inputImages['shape'][i]][1]
                
                if params == 'copies' or params == 'all':
                    self.inputImages['copies'][i] = update_copies

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
                    for key in self.inputImages.keys():
                        self.inputImages[key].clear()

            elif detype == 'batch':
                del_img = []
                loggingInfo(f"[ImageFrame] Deleting {len(del_img)} selected images.")

            last_len = len(self.inputImages['path'])
            loggingInfo(f"[ImageFrame] Total {init_len-last_len} image(s) deleted from image frame.")

        except Exception as e:
            raise CustomException(e, sys)
        
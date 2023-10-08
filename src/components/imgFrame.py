import os, sys
from PIL import Image
from src.logger import logging
from src.exception import CustomException
from src.utils import *
from src.config import *


class ImageFrame:
    def __init__(self) -> None:
        self.img:Image.Image
        self.px_width:int
        self.px_height:int
        self.xc:int
        self.yc:int


    def initiate_img(self, img:Image.Image,
                  px_height:float, xc:int, yc:int) -> None:
        try:
            self.img = img
            self.px_height = px_height
            self.xc = xc
            self.yc = yc

            loggingInfo(f"[ImageFrame] Initiate image with pixel height [{px_height}], xc [{xc}] and yc [{yc}] completely.")
        
        except Exception as e:
            raise CustomException("[ImageFrame]" + e, sys)
        

    def crop_img(self) -> Image.Image:
        try:
            # Calculate the crop box coordinates
            left = self.xc - (self.px_width / 2)
            top = self.yc - (self.px_height / 2)
            right = self.xc + (self.px_width / 2)
            bottom = self.yc + (self.px_height / 2)

            # Crop the image
            cropped_img = self.img.crop((left, top, right, bottom))
            
            cropped_img = cropped_img.convert("RGB")

            return cropped_img
        
        except Exception as e:
            raise CustomException("[ImageFrame]" + e, sys)
    

    def crop_by_shape(self, shape:str) -> Image.Image:
        try:
            if shape not in SHAPE_RATIOS.keys():
                loggingInfo(f"[ImageFrame] Undefined shape input: {shape}.")
                raise AssertionError(f"[ImageFrame] Shape must be either one of these: {SHAPE_RATIOS.keys()}")
            
            self.px_width = SHAPE_RATIOS[shape] * self.px_height
            cropped_img = self.crop_img()
            loggingInfo(f"[ImageFrame] Crop image by shape of {shape} completely.")
            
            return cropped_img
        
        except Exception as e:
            raise CustomException("[ImageFrame]" + e, sys)

    
# if __name__=="__main__":
#     path = "..\\img\\bennett 1.jpg"
#     img = Image.open(path)

#     iwidth, iheight = img.size

#     print(iwidth, iheight)
#     xc, yc = iwidth//2, iheight//2

#     tool = ImageFrame()
    
#     tool.initiate_img(img, px_height=500, xc=xc, yc=yc)

#     crop_img = tool.crop_by_shape(shape='Space')
#     img.show()
#     crop_img.show()

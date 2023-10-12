import os
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
from src.config import *


def open_images(master):
    file_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.ppm *.pgm")])
    print(file_paths)
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
            image = image.resize((IMAGE_WIDTH, IMAGE_HEIGHT))
            photo = ImageTk.PhotoImage(image)
            images.append(photo)

            # Get the base filename (without path) for the image
            image_name = os.path.basename(file_path)
            image_names.append(image_name)


        # Create a grid of labels to display the resized images
        for i, (photo, name) in enumerate(zip(images, image_names)):
            row = 2 * (i // NUM_COLUMNS)
            col = i % NUM_COLUMNS
            
            if len(name)>MAX_NAME_LENGTH:
                name = name[:MAX_NAME_LENGTH] + "..." + name.split('.')[-1]
            
            image_label = ctk.CTkLabel(master, image=photo)
            image_label.image = photo
            image_label.grid(row=row, column=col, padx=5, pady=5)

            name_label = ctk.CTkLabel(master, text=name)
            name_label.grid(row=row+1, column=col, padx=5)  # Place the name label below the image label


        
root = ctk.CTk()
root.title("Add Images and Arrange in Grid")
root.resizable(False, False)

# APPERANCE
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")




select_output_folder_button = ctk.CTkButton(root, text="Select folder", font=CUSTOMFONT_H2, width=8, height=28, \
                                        command=lambda: open_images(imgbox_frame))
select_output_folder_button.grid(row=0, column=0, sticky='ns')

imgbox_frame = ctk.CTkScrollableFrame(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
imgbox_frame.grid(row=1, column=0, padx=(15, 15), pady=(15, 0), sticky="nsew")

root.mainloop()

#!/usr/bin/env python3

# import tkinter
# from tkinter import *

# master = tkinter.Tk()
# master.geometry("750x500")

# listbox = Listbox(master)
# listbox.place(x=3,y=0)

# enable = ['button 1', 'button 2', 'button 3']
# list_for_listbox = ["one", "two", "three", "four"]

# for item in list_for_listbox:
#     listbox.insert(END, item)
#     for y in enable:
#         globals()["var{}{}".format(item, y)] = BooleanVar()
#         globals()["checkbox{}{}".format(item, y)] = Checkbutton(master, text=y, variable=globals()["var{}{}".format(item, y)])

# def onselect(evt):
#     # Note here that Tkinter passes an event object to onselect()
#     w = evt.widget
#     x=0
#     index = int(w.curselection()[0])
#     value = w.get(index)
#     print ('You selected item %d: "%s"' % (index, value))

#     for y in enable:
#         for item in list_for_listbox:
#             globals()["checkbox{}{}".format(item, y)].place_forget()
#         globals()["checkbox{}{}".format(value, y)].place(x=300,y=0+x)
#         x+=50

# listbox.bind('<<ListboxSelect>>', onselect)

# print(enable)

# mainloop()
import os
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
from src.config import *
Image.MAX_IMAGE_PIXELS = 2000000000

def open_images():
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

        
root = ctk.CTk()
root.title("Add Images and Arrange in Grid")
root.resizable(False, False)

# APPERANCE
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


select_output_folder_button = ctk.CTkButton(root, text="Select folder", font=CUSTOMFONT_H2, width=8, height=28, \
                                        command=lambda: open_images())
select_output_folder_button.grid()

root.mainloop()

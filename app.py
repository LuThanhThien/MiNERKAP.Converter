import os, sys
from CTkListbox import *
from dist.src.utils import *
import customtkinter as ctk
from dist.src.config import *
from dist.src.logger import *
from dist.src.exception import *
from dist.src.components.imgConverter import *
from dist.src.components.imgFrame import *
from dist.src.components.imgIngestion import *
import warnings

# Filter out the specific warning message
warnings.filterwarnings("ignore")


# APPERANCE
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
        # MAIN APP ---------------------------------------------------------------------------------------------------------
        def __init__(self):
            super().__init__()

            # GUI
            self.converter = Converter()
            self.converter.initiate_converter(self)
            self.imgFrame = ImageFrame()
            self.imgFrame.initiate_frame_obj(self)
            self.title("MiNERKAP")
            self.resizable(False, False) # fixed window size

            # storage purposes
            self.gridImageFrame = [] # storage of each image frame
            self.selectedIndices = [] # index referencing for selected items
            self.info_frame = [] # storage if image info
            
            # row 0, frame 1: parameters frame ----------------------------------------------------------------------------------
            self.param_frame = ctk.CTkFrame(self)
            self.param_frame.grid(row=0, column=0, padx=(15, 15), pady=(15, 0), sticky="nsew")
            self.param_frame.bind("<Button-1>", lambda event: self.param_frame.focus_set())
            
            # Add a label and entry for user input
            self.copies_label = ctk.CTkLabel(master=self.param_frame, text="Copies:", font=CUSTOMFONT_H0)
            self.copies_label.grid(row=0, column=0, padx=PADX_ONI, pady=PADY_ONI, sticky='w')

            self.copies_var = ctk.StringVar()
            self.copies_display = ctk.StringVar()
            self.copies_entry = ctk.CTkEntry(master=self.param_frame, width=60, textvariable=self.copies_display, font=CUSTOMFONT_H0)
            self.copies_entry.grid(row=0, column=1, padx=0, pady=PADY_ONI, sticky="nsew")
            self.copies_entry.bind("<Return>", self.validate_copies)



            # Create a label for the shape selection
            self.shape_label = ctk.CTkLabel(master=self.param_frame, text="Shape:", font=CUSTOMFONT_H0)
            self.shape_label.grid(row=0, column=2, padx=PADX_ONI, pady=PADY_ONI, sticky='e')

            # Create a options for shape selection
            self.shape_var = ctk.StringVar()
            self.shape_display = ctk.StringVar()
            self.shape_options = ctk.CTkOptionMenu(master=self.param_frame, values=list(IMG_SHAPES.keys()), font=CUSTOMFONT_H0,\
                                                   variable=self.shape_display, command=self.validate_shape)
            self.shape_options.grid(row=0, column=3, padx=0, pady=PADY_ONI, sticky="w")   


            # Create and configure widgets for selecting output folder
            self.output_folder_var = ctk.StringVar(value=DEFAULT_OUTPUT)  # Set the desktop folder as the default value
            self.output_folder_label = ctk.CTkLabel(master=self.param_frame, text="Output:", font=CUSTOMFONT_H0)
            self.output_folder_label.grid(row=0, column=4, sticky="w", padx=(40,15), pady=PADY_ONI)

            self.output_folder_entry = ctk.CTkEntry(master=self.param_frame, width=500, height=30, textvariable=self.output_folder_var,\
                                                     state="readonly", font=CUSTOMFONT_H0)
            self.output_folder_entry.grid(row=0, column=5, padx=0, pady=PADY_ONI, columnspan=3, sticky="w")

            self.select_output_folder_button = ctk.CTkButton(master=self.param_frame, text="Select folder", width=8, height=30,\
                                                              font=CUSTOMFONT_H0, command=self.select_output_click)
            self.select_output_folder_button.grid(row=0, column=9, sticky='w', padx=PADX_ONI, pady=PADY_ONI)


            # row 1 ----------------------------------------------------------------------------------
            self.add_images_button = ctk.CTkButton(master=self, text="Add images", width=120, height=40,\
                                                    font=CUSTOMFONT_H0, command=self.add_images_click)
            self.add_images_button.grid(row=1, column=0, padx=(20,5), pady=PADY_START, sticky='w')


            # Create the Delete all images button
            self.delete_all_button = ctk.CTkButton(master=self, text="Delete All", width=120, height=40,\
                                                   font=CUSTOMFONT_H0, command=self.delete_click)
            self.delete_all_button.grid(row=1, column=0, padx=(120+40,5), pady=PADX_START, sticky="w")
    

            # row 1, frame 2: Images frame ----------------------------------------------------------------------------------
            # Trace for var change 
            self.copies_var.trace('w', self.copies_change)
            self.shape_var.trace('w', self.shape_change)

            self.scrollImageFrame = ctk.CTkScrollableFrame(self, width=CANVAS_WIDTH-120, height=CANVAS_HEIGHT)
            self.scrollImageFrame.grid(row=2, column=0, padx=(15, 15), pady=(15, 15), sticky="nsew")

            # row 3 ----------------------------------------------------------------------------------
            # Create the Convert button with the new function
            self.convert_button = ctk.CTkButton(master=self, text="Convert to Docx", height=45, width=130, font=CUSTOMFONT_H0,\
                                    command=self.convert_click)
            self.convert_button.grid(row=3, column=0, columnspan=2, padx=PADX, pady=PADY_END)    

            # initiate entry as disable
            self.copies_entry.configure(state='disabled')
            self.shape_options.configure(state='disabled')


        # IMAGE FRAME --------------------------------------------------------------------------------------------------
        def ScrollableImageFrame(self, ids=None):
            try:
                if ids == []:
                    # remove the widgets from the grid
                    for widget in self.scrollImageFrame.grid_slaves():
                        widget.destroy()   
                    
                    # reset frame
                    self.scrollImageFrame = ctk.CTkScrollableFrame(self, width=CANVAS_WIDTH-120, height=CANVAS_HEIGHT)
                    self.scrollImageFrame.grid(row=2, column=0, padx=(15, 15), pady=(15, 15), sticky="nsew")
                    return
                
                if ids == None:
                    ids = list(range(len(self.gridImageFrame)))

                self.bind("<Control-a>", self.select_all_images)
                self.scrollImageFrame.bind("<Button-1>", self.deselect_all_images)
                
                # Create a grid of labels to display the resized images
                for i in ids:
                    photo = self.imgFrame.inputImages['Image'][i]
                    name = self.imgFrame.inputImages['name'][i]
                    shape = self.imgFrame.inputImages['shape'][i]
                    copies = self.imgFrame.inputImages['copies'][i]

                    row = 2 * ((i) // FRAMES_PER_COLUMN)
                    col = (i) % FRAMES_PER_COLUMN
                    
                    if len(name)>MAX_NAME_LENGTH:
                        name = name[:MAX_NAME_LENGTH] + "..." + name.split('.')[-1]

                    # init frames
                    if i < len(self.gridImageFrame):
                        self.info_frame[i].destroy()
                        self.info_frame[i] = ctk.CTkFrame(self.scrollImageFrame, width=FRAME_WIDTH, height=60)
                    else:
                        self.gridImageFrame.append(ctk.CTkFrame(self.scrollImageFrame, width=FRAME_WIDTH, height=FRAME_HEIGHT,\
                                                                fg_color=from_rgb(FRAME_RGB)))
                        self.info_frame.append(ctk.CTkFrame(self.scrollImageFrame, width=FRAME_WIDTH, height=60))
                        
                    # grid image frame
                    self.gridImageFrame[i].grid(row=row, column=col, padx=(7, 7), pady=(10, 10), sticky='nsew')
                    self.gridImageFrame[i].grid_propagate(0)

                    # Configure the grid to expand so the image placed in center of frame
                    self.gridImageFrame[i].grid_rowconfigure(0, weight=1)
                    self.gridImageFrame[i].grid_columnconfigure(0, weight=1)

                    # display image in frame
                    image_label = ctk.CTkLabel(self.gridImageFrame[i], image=photo)
                    image_label.image = photo
                    image_label.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky='nsew')

                    # image infro
                    self.info_frame[i].grid(row=row+1, column=col, padx=(10, 10), pady=(5, 20))
                    self.info_frame[i].grid_propagate(0)
                    name_label = ctk.CTkLabel(self.info_frame[i], text=name, font=CUSTOMFONT_H0)
                    name_label.grid(row=0, column=0, padx=(2, 0), pady=(0, 0), sticky='w')  # Place the name label below the image label
                    shape_label = ctk.CTkLabel(self.info_frame[i], text=f'Shape: {shape} - Copies: {copies}', font=CUSTOMFONT_H2)
                    shape_label.grid(row=1, column=0, padx=(2, 0), pady=(2, 0), sticky='w')  # Place the name label below the image label

                    # Configure events
                    self.gridImageFrame[i].bind("<Enter>", lambda event, index=i: self.mouse_enter_frame(event, index))
                    self.gridImageFrame[i].bind("<Leave>", lambda event, index=i: self.mouse_leave_frame(event, index))
                    self.gridImageFrame[i].bind("<Button-1>", lambda event, index=i: self.on_image_click(event, index))
                    
                    image_label.bind("<Enter>", lambda event, index=i: self.mouse_enter_frame(event, index))
                    image_label.bind("<Leave>", lambda event, index=i: self.mouse_leave_frame(event, index))
                    image_label.bind("<Button-1>", lambda event, index=i: self.on_image_click(event, index))
                    
                    self.info_frame[i].bind("<Button-1>", self.deselect_all_images)
                    name_label.bind("<Button-1>", self.deselect_all_images)
                    shape_label.bind("<Button-1>", self.deselect_all_images)


            except Exception as e:
                raise CustomException(e, sys)


        # FRAME CONFIGURE ---------------------------------------------------------------------------------------------
        def on_image_click(self, event, image_index):
            # Check if Ctrl key is pressed
            
            if event.state & 4:  # Ctrl key is pressed
                if image_index in self.selectedIndices:
                    self.selectedIndices.remove(image_index)
                else:
                    self.selectedIndices.append(image_index)
            elif event.state & 1:  # Shift key is pressed
                try:
                    fixed_index = self.selectedIndices[-1]
                except:
                    self.selectedIndices.append(0)
                    fixed_index = self.selectedIndices[-1]
                start_index = min(fixed_index, image_index)
                end_index = max(fixed_index, image_index)
                self.selectedIndices.clear()
                for i in range(start_index, end_index + 1):
                    self.selectedIndices.append(i)
                self.selectedIndices.append(fixed_index)
            else:
                self.selectedIndices.clear()
                self.selectedIndices.append(image_index)

            # Update the appearance of selected images
            self.update_image_appearance()
        
        def select_all_images(self, event):
            self.selectedIndices = list(range(len(self.gridImageFrame)))
            self.update_image_appearance()

        def deselect_all_images(self, event):
            self.selectedIndices.clear()
            self.update_image_appearance()

        def mouse_enter_frame(self, event, i):
            if i not in self.selectedIndices:
                self.gridImageFrame[i].configure(fg_color=from_rgb(ENTER_FRAME_RGB))

        def mouse_leave_frame(self, event, i):
            if i not in self.selectedIndices:
                self.gridImageFrame[i].configure(fg_color=from_rgb(FRAME_RGB))

        def update_image_appearance(self):
            # Update the appearance of selected images (e.g., change background color)
            for i in range(len(self.gridImageFrame)):
                if i in self.selectedIndices:
                    # Modify the appearance for the selected image
                    self.gridImageFrame[i].configure(fg_color=from_rgb(SELECT_FRAME_RGB))
                else:
                    self.gridImageFrame[i].configure(fg_color=from_rgb(FRAME_RGB))
            self.display_params()
            
        # Display params of selected images 
        def display_params(self):
            copies_list = [self.imgFrame.inputImages['copies'][i] for i in self.selectedIndices]
            shape_list = [self.imgFrame.inputImages['shape'][i] for i in self.selectedIndices]

            unique_copies = set(copies_list)
            unique_shape = set(shape_list)

            if len(unique_copies) == 1:
                self.copies_display.set(value=list(unique_copies)[0])
            else: 
                self.copies_display.set(value='')
            if len(unique_shape) == 1:
                self.shape_display.set(value=list(unique_shape)[0])
            else:
                self.shape_display.set(value='')

            if len(self.selectedIndices) == 0:
                self.copies_entry.configure(state='disabled')
                self.shape_options.configure(state='disabled')
                self.copies_display.set(value='')
                self.shape_display.set(value='')
            else:
                self.copies_entry.configure(state='normal')
                self.shape_options.configure(state='normal')


        # UPDATE PARAMS --------------------------------------------------------------------------------------------------
        def copies_change(self, *args):
            self.imgFrame.update_params(ids=self.selectedIndices, params='copies', update_copies=int(self.copies_var.get()))
            self.ScrollableImageFrame(ids=self.selectedIndices)

        def shape_change(self, *args):
            self.imgFrame.update_params(ids=self.selectedIndices, params='shape', update_shape=self.shape_var.get())
            self.ScrollableImageFrame(ids=self.selectedIndices)

        # validate copies range
        def validate_copies(self, event):
            try:
                copies = int(self.copies_display.get())
                if COPY_RANGE[0] <= copies <= COPY_RANGE[1]:
                    self.copies_display.set(value=copies)
                    self.copies_var.set(value=copies)
                else:
                    messagebox.showerror("Invalid Input", "Copies should be an integer between 1 and 100")
                    self.display_params()
            except ValueError:
                messagebox.showerror("Invalid Input", "Copies should be an integer between 1 and 100")
                self.display_params()

        # validate shape
        def validate_shape(self, event):
            try:
                shape = self.shape_display.get()
                if shape in IMG_SHAPES.keys():
                    self.shape_display.set(value=shape)
                    self.shape_var.set(value=shape)
                else:
                    messagebox.showerror("Invalid Input", f"Shape should be any value in {IMG_SHAPES.keys()}")
            except ValueError:
                messagebox.showerror("Invalid Input", f"Shape should be any value in {IMG_SHAPES.keys()}")


        # BUTTON CLICK --------------------------------------------------------------------------------------------------
        def select_output_click(self):
            select_folder(self.output_folder_var)

        def add_images_click(self):
            id_start = len(self.imgFrame.inputImages['path'])
            self.imgFrame.add_images()
            id_end = len(self.imgFrame.inputImages['path'])
            self.ScrollableImageFrame(ids=range(id_start, id_end))

        def convert_click(self):
            self.converter.convert_button_click(self.imgFrame.inputImages, self.output_folder_var)

        def delete_click(self):
            ids = list(range(len(self.gridImageFrame)))
            is_delete, detype = self.imgFrame.delete_images(ids)
            if is_delete == True and detype == 'all':
                self.gridImageFrame.clear()
                self.info_frame.clear()
                self.ScrollableImageFrame(ids=[])


app = App()
app.mainloop()

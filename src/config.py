import os, sys

IMG_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".ppm", ".pgm"]

IMG_TYPES = [("Image files", ';'.join(["*"+ex for ex in IMG_EXTENSIONS]))] + [("All files", "*.*")]
print(IMG_TYPES)

# Font
CUSTOMFONT = ('Helvetia', 14)

# Fixed width and height for the displayed images
IMAGE_WIDTH = 200
IMAGE_HEIGHT = 200
NUM_COLUMNS = 5
MAX_NAME_LENGTH = 20

# canvas size
CANVAS_WIDTH = (IMAGE_HEIGHT + 10) * NUM_COLUMNS + 5
CANVAS_HEIGHT = 600


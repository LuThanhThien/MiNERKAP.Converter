import pyglet, os

# IMAGE PIPELINE
ICON_PATH = 'src//img//iconwhite.png'
IMG_EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".ppm", ".pgm"]

IMG_TYPES = [("Image files", ';'.join(["*"+ex for ex in IMG_EXTENSIONS]))] + [("All files", "*.*")]

# Shape: [height, width]
IMG_SHAPES = {
    'Square': [16, 16],
    'Tab': [16.5, 20.6],
    'Caps Lock': [16.5, 29.7],
    'Shift': [16.5, 37.1],
    'Ctrl': [16.5, 20.6],
    'Win': [16.5, 20.6],
    'Space': [16.5, 29.7*3],
    'Combo': None,
    }  

COMBO = [IMG_SHAPES['Tab'][0] + IMG_SHAPES['Caps Lock'][0] + IMG_SHAPES['Shift'][0] + IMG_SHAPES['Ctrl'][0],
         IMG_SHAPES['Ctrl'][1] + IMG_SHAPES['Win'][1]]
IMG_SHAPES['Combo'] = COMBO
COMBO_GRID = {
        'Tab': [0, 0], 'Caps Lock': [1, 0],
        'Shift': [2, 0], 'Ctrl': [3, 0],
        'Win': [3, 1],
    }

# ratio = width / height
SHAPE_RATIOS = {}
for shape, dimensions in IMG_SHAPES.items():
    if shape != 'Combo':
        height, width = dimensions
        ratio = width / height
        SHAPE_RATIOS[shape] = ratio
    else:
        SHAPE_RATIOS[shape] = COMBO[1] / COMBO[0]

DEFAULT_PARAMS = {
    'copies': 11,
    'shape': 'Square'
}
DEFAULT_OUTPUT = os.path.expanduser('~/Desktop')

# GUI
# Font
pyglet.font.add_file('src\\fonts\\Montserrat-Bold.ttf')
CUSTOMFONT_H2 = ('Montserrat-Bold', 12)
CUSTOMFONT_H1 = ('Montserrat-Bold', 14)
CUSTOMFONT_H0 = ('Montserrat-Bold', 16)

# padding widgets
PADX_START, PADX_END = (15, 5), (5, 15)
PADY_START, PADY_END = (15, 5), (5, 15)
PADX_ONI, PADY_ONI = (15, 15), (15, 15)

PADX = (0, 5)
PADY = (0, 5)

# IMAGES FRAME
# Fixed width and height for the displayed images
IMAGE_WIDTH = 300
IMAGE_HEIGHT = 300
IMAGES_PER_COLUMN = 5
MAX_NAME_LENGTH = 20

# frame size
CANVAS_WIDTH = (IMAGE_HEIGHT) * IMAGES_PER_COLUMN - 50
CANVAS_HEIGHT = 500


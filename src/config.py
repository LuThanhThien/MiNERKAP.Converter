import pyglet, os

# IMAGE PIPELINE
ICON_PATH = 'src//img//iconwhite.png'
IMG_EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".ppm", ".pgm"]

IMG_TYPES = [("Image files", ';'.join(["*"+ex for ex in IMG_EXTENSIONS]))] + [("All files", "*.*")]

# Copies
COPY_RANGE = [1,100]

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
pyglet.font.add_file('src\\fonts\\Montserrat-Medium.ttf')
CUSTOMFONT_H2 = ('Montserrat-Medium', 15)
CUSTOMFONT_H1 = ('Montserrat-Bold', 14)
CUSTOMFONT_H0 = ('Montserrat-Bold', 15)

# padding widgets
PADX_START, PADX_END = (10, 5), (5, 10)
PADY_START, PADY_END = (10, 5), (5, 10)
PADX_ONI, PADY_ONI = (10, 10), (10, 10)

PADX = (0, 5)
PADY = (0, 5)

# padding image color code
FRAME_RGB = (92, 90, 88)
ENTER_FRAME_RGB = (133, 121, 121)
SELECT_FRAME_RGB = (196, 101, 96)

# IMAGES FRAME
# Fixed width and height for the displayed images
FRAME_WIDTH = 300
FRAME_HEIGHT = 300
FRAMES_PER_COLUMN = 4
MAX_NAME_LENGTH = 35

# frame size
CANVAS_WIDTH = (FRAME_HEIGHT) * FRAMES_PER_COLUMN + 200
CANVAS_HEIGHT = 500


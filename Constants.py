CELL_SIZE = 21
NROWS = 31
NCOLUMNS = 31
SCREEN_WIDTH = CELL_SIZE * NCOLUMNS
SCREEN_HEIGHT = CELL_SIZE * NROWS
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
CENTER = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (125, 125, 125)
LIGHT_BLUE = (64, 128, 255)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)

MAP_WALL = (0, 0, 255, 255)
MAP_ROAD = (0, 0, 0, 255)
MAP_CROSSROAD = (0, 255, 0, 255)
MAP_PACMAN_START_POSITION = (255, 255, 0, 255)
MAP_GHOSTS_START_POSITION = (255, 0, 255, 255)
MAP_SPIRIT_DOOR = (255, 0, 0, 255)
MAP_REST_SPACE = (255, 255, 255, 255)

CELL_RECT_SIDE = 4

UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4
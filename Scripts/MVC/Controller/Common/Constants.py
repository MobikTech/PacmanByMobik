CELL_SIZE = 25
CELL_HALF_SIZE = CELL_SIZE / 2
FPS = 60
MAIN_DIRECTORY = 'D:\Projects\PYTHON\PacmanByMobik'


class GRID():
    ROWS_COUNT = 31
    COLUMNS_COUNT = 31
    SIZE = (COLUMNS_COUNT, ROWS_COUNT)
    CENTER = (int(COLUMNS_COUNT / 2), int(ROWS_COUNT / 2))


class RANDOM_MAP_SETTINGS():
    MAP_TOP_LEFT_CORNER = (1, 1)
    MAP_BOTTOM_RIGHT_CORNER = (29, 15)

    REST_SPACE_TOP_LEFT_CORNER = (1, 18)
    REST_SPACE_BOTTOM_RIGHT_CORNER = (29, 29)


class SCREEN():
    SCREEN_START_POINT = (0, 0)
    SCREEN_WIDTH = CELL_SIZE * GRID.COLUMNS_COUNT
    SCREEN_HEIGHT = CELL_SIZE * GRID.ROWS_COUNT
    SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
    SCREEN_CENTER = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)


class COLORS():
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    GRAY = (125, 125, 125)
    LIGHT_BLUE = (64, 128, 255)
    YELLOW = (225, 225, 0)
    PINK = (230, 50, 230)
    TRANSPARENT = (0, 0, 0, 0)


class CELL_TYPE():
    WALL = 'wall'
    ROAD = 'road'
    CROSSROAD = 'crossroad'
    PACMAN_START_POSITION = 'pacman start position'
    GHOSTS_START_POSITION = 'ghosts start position'
    REST_SPACE = 'empty space'


class DIRECTIONS():
    UP = 'up'
    RIGHT = 'right'
    DOWN = 'down'
    LEFT = 'left'


class VECTORS():
    VECTOR_UP = (0, -1)
    VECTOR_DOWN = (0, 1)
    VECTOR_RIGHT = (1, 0)
    VECTOR_LEFT = (-1, 0)

class SPRITE_TYPES():
    PACMAN = 1
    GHOST = 2
    COIN = 3
    CELL_WALL = 4
    CELL_ROAD = 5
    CELL_CROSSROAD = 6
    CELL_DOOR = 7

class GHOST_TYPE():
    RIKKO = 1
    PINKY = 2
    GREENKY = 3
    CLYNE = 4

class SEARCH_ALGORITHMES():
    BFS = 1
    ASTAR = 2

class AI_ALGORITHMES():
    MINIMAX = 1,
    EXPECTIMAX = 2
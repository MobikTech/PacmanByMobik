class GRID():
    ROWS_COUNT = 31
    COLUMNS_COUNT = 31
    SIZE = (COLUMNS_COUNT, ROWS_COUNT)
    CENTER = (int(COLUMNS_COUNT / 2), int(ROWS_COUNT / 2))


class CELL_TYPE():
    MAP_WALL = 'wall'
    MAP_ROAD = 'road'
    MAP_CROSSROAD = 'crossroad'
    MAP_PACMAN_START_POSITION = 'pacman start position'
    MAP_GHOSTS_START_POSITION = 'ghosts start position'


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

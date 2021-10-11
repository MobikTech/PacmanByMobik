from Scripts.Common.Constants import *

class MazeGenerator():
    SCREEN_WIDTH = None
    SCREEN_HEIGHT = None
    SCREEN_CENTER = None

    def __init__(self, screenWidth: int, screenHeight: int):
        MazeGenerator.SCREEN_WIDTH = screenWidth
        MazeGenerator.SCREEN_HEIGHT = screenHeight
        MazeGenerator.SCREEN_CENTER = (screenWidth / 2, screenHeight / 2)
        # self.colorMap: list[list[tuple[int, int, int, int]]] = None
        self.fullColorMap = dict()

    def initialize(self):
        for x in range(MazeGenerator.SCREEN_WIDTH):
            for y in range(MazeGenerator.SCREEN_HEIGHT):
                # self.colorMap[x][y] = CELL_TYPE.MAP_WALL
                self.fullColorMap[(x, y)] = CELL_TYPE.MAP_WALL

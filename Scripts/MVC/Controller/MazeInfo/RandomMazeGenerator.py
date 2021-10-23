from Scripts.MVC.Controller.Common.Constants import *
from Scripts.MVC.Model.Navigation.Coords import Coords


class RandomMazeGenerator():

    @staticmethod
    def initializeGrid():
        grid = dict()
        for x in range(GRID.COLUMNS_COUNT):
            for y in range(GRID.ROWS_COUNT):
                coords = Coords((x, y))
                if coords.getTuple() == (GRID.CENTER[0], GRID.CENTER[1] - 1):
                    grid[coords.getTuple()] = CELL_TYPE.GHOSTS_START_POSITION
                elif RandomMazeGenerator.inRestSpaceRect(coords):
                    grid[coords.getTuple()] = CELL_TYPE.REST_SPACE
                else:
                    grid[coords.getTuple()] = CELL_TYPE.WALL


        return grid

    @staticmethod
    def inMapRect(point: Coords):
        if point.x >= RANDOM_MAP_SETTINGS.MAP_TOP_LEFT_CORNER[0] and \
                point.x <= RANDOM_MAP_SETTINGS.MAP_BOTTOM_RIGHT_CORNER[0] and \
                point.y >= RANDOM_MAP_SETTINGS.MAP_TOP_LEFT_CORNER[1] and \
                point.y <= RANDOM_MAP_SETTINGS.MAP_BOTTOM_RIGHT_CORNER[1]:
            return True
        return False

    @staticmethod
    def inRestSpaceRect(point: Coords):
        if point.x >= RANDOM_MAP_SETTINGS.REST_SPACE_TOP_LEFT_CORNER[0] and \
                point.x <= RANDOM_MAP_SETTINGS.REST_SPACE_BOTTOM_RIGHT_CORNER[0] and \
                point.y >= RANDOM_MAP_SETTINGS.REST_SPACE_TOP_LEFT_CORNER[1] and \
                point.y <= RANDOM_MAP_SETTINGS.REST_SPACE_BOTTOM_RIGHT_CORNER[1]:
            return True
        return False

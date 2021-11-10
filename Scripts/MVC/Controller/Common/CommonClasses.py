import random

from Scripts.MVC.Controller.Common.Constants import *
from Scripts.MVC.Model.Navigation.Coords import Coords


class CoordsConverter():

    @staticmethod
    def worldToGrid(coords: Coords):
        x = int(coords.x / CELL_SIZE)
        y = int(coords.y / CELL_SIZE)
        return Coords((x, y))

    @staticmethod
    def gridToWorld(coords: Coords):
        x = int(coords.x * CELL_SIZE + CELL_SIZE / 2)
        y = int(coords.y * CELL_SIZE + CELL_SIZE / 2)
        return Coords((x, y))


class CoordsBehaviour():

    @staticmethod
    def inCellCenter(coordsWorld: Coords):
        OFFSET_ERROR = 1
        cellCenter = CoordsConverter.gridToWorld(CoordsConverter.worldToGrid(coordsWorld))
        if coordsWorld.x > cellCenter.x - OFFSET_ERROR and \
                coordsWorld.x < cellCenter.x + OFFSET_ERROR and \
                coordsWorld.y > cellCenter.y - OFFSET_ERROR and \
                coordsWorld.y < cellCenter.y + OFFSET_ERROR:
            return True


class DirectionManager():
    ALL_DIRECTIONS = [DIRECTIONS.UP,
                      DIRECTIONS.DOWN,
                      DIRECTIONS.RIGHT,
                      DIRECTIONS.LEFT]

    @staticmethod
    def getPossibleDirections(coords: Coords, grid: dict[tuple[int, int]]):
        possibleCellTypes = (CELL_TYPE.ROAD,
                             CELL_TYPE.CROSSROAD,
                             CELL_TYPE.PACMAN_START_POSITION)
        possibleDirections = list()
        for direction in DirectionManager.ALL_DIRECTIONS:
            if grid[coords.getOffsetted(direction, 1).getTuple()] in possibleCellTypes:
                possibleDirections.append(direction)
        return possibleDirections

    @staticmethod
    def getOppositeToDirection(direction):
        if direction == DIRECTIONS.UP:
            return DIRECTIONS.DOWN
        elif direction == DIRECTIONS.DOWN:
            return DIRECTIONS.UP
        elif direction == DIRECTIONS.RIGHT:
            return DIRECTIONS.LEFT
        elif direction == DIRECTIONS.LEFT:
            return DIRECTIONS.RIGHT
        raise NotImplementedError


    # todo remove
    @staticmethod
    def directionToNormalizedVector(direction: int):
        if direction == DIRECTIONS.UP:
            return VECTORS.VECTOR_UP
        elif direction == DIRECTIONS.DOWN:
            return VECTORS.VECTOR_DOWN
        elif direction == DIRECTIONS.RIGHT:
            return VECTORS.VECTOR_RIGHT
        elif direction == DIRECTIONS.LEFT:
            return VECTORS.VECTOR_LEFT
        raise Exception("Was received incorrect direction")


class Random():
    @staticmethod
    def getBool(probability: float):
        return random.random() < probability

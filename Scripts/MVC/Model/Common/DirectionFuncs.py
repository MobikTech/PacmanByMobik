from Scripts.MVC.Model.Common.Constants import *
from Scripts.MVC.Model.Navigation.Coords import Coords

ALL_DIRECTIONS = [DIRECTIONS.UP,
                  DIRECTIONS.DOWN,
                  DIRECTIONS.RIGHT,
                  DIRECTIONS.LEFT]


def directionToNormalizedVector(direction: str):
    if direction == DIRECTIONS.UP:
        return VECTORS.VECTOR_UP
    elif direction == DIRECTIONS.DOWN:
        return VECTORS.VECTOR_DOWN
    elif direction == DIRECTIONS.RIGHT:
        return VECTORS.VECTOR_RIGHT
    elif direction == DIRECTIONS.LEFT:
        return VECTORS.VECTOR_LEFT
    raise Exception("Was received incorrect direction")


def getPossibleDirections(coords: Coords, grid: dict[tuple[int, int]]):
    possibleCellTypes = (CELL_TYPE.MAP_ROAD,
                         CELL_TYPE.MAP_CROSSROAD,
                         CELL_TYPE.MAP_PACMAN_START_POSITION)
    possibleDirections = list()
    for direction in ALL_DIRECTIONS:
        if grid[coords.getOffsetted(direction, 1)] in possibleCellTypes:
            possibleDirections.append(direction)
    return possibleDirections

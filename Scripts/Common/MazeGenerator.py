import random

from Scripts.Common.CommonFuncs import *
from Scripts.Common.Constants import *
from Scripts.Common.CoordsConverter import *


class MazeGenerator():
    SCREEN_WIDTH = None
    SCREEN_HEIGHT = None
    SCREEN_CENTER = None

    CROSSROAD_APPEARANCE_CHANCE = 10

    def __init__(self, screenWidth: int, screenHeight: int):
        MazeGenerator.SCREEN_WIDTH = screenWidth
        MazeGenerator.SCREEN_HEIGHT = screenHeight
        MazeGenerator.SCREEN_CENTER = (screenWidth / 2, screenHeight / 2)
        # self.colorMap = list[list[tuple[int, int, int, int]]]
        # self.colorMap = [[CELL_TYPE.MAP_WALL for x in range(SCREEN_WIDTH)] for y in range(SCREEN_HEIGHT)]
        self.colorMap = self.initializeColorMap()
        self.fullColorMap = dict()

    def initializeColorMap(self):
        colorMap = [[CELL_TYPE.MAP_WALL for x in range(COLUMNS_COUNT)] for y in range(ROWS_COUNT)]
        gridCenter = worldToGridT(CENTER_WORLD_SPACE)
        crossroads = list()
        # gridCenter = (15, 15)
        for x in range(COLUMNS_COUNT):
            for y in range(ROWS_COUNT):
                if (x, y) == gridCenter:
                    colorMap[x][y] = CELL_TYPE.MAP_GHOSTS_START_POSITION
                elif x > 0 and x < COLUMNS_COUNT - 1 and y > gridCenter[1] + 1 and y < ROWS_COUNT - 1:
                    colorMap[x][y] = CELL_TYPE.MAP_REST_SPACE
                elif _inMapRect(gridCenter, x, y) and random.randint(1, MazeGenerator.CROSSROAD_APPEARANCE_CHANCE) == 1 and \
                        hasNeighbourCells((x, y), colorMap) == False:
                    crossroads.append((x, y))
                    colorMap[x][y] = CELL_TYPE.MAP_CROSSROAD
                else:
                    colorMap[x][y] = CELL_TYPE.MAP_WALL


        for crossroad in crossroads:
            makeRoadsToCrossroad(crossroad, colorMap, crossroads)

        return colorMap


def _inMapRect(gridCenter: Tuple[int, int], x: int, y: int):
    if x < COLUMNS_COUNT - 1 and x > 0 and \
    y < gridCenter[1] - 1 and y > 0:
        return True

def makeRoadsToCrossroad(crossroad: Tuple[int, int], colorMap: list[list[tuple[int, int, int, int]]], crossroads: list[Tuple[int, int]]):
    directions = getTwoRandomDirections()
    currentPosition = crossroad

    for direction in directions:
        currentPosition = getOffsettedPoint(currentPosition, direction, 1)
        while _inMapRect(CENTER_GRID_SPACE, currentPosition[0], currentPosition[1]):
            x, y = currentPosition
            if colorMap[x][y] == CELL_TYPE.MAP_CROSSROAD:
                break
            elif colorMap[x][y] == CELL_TYPE.MAP_ROAD:
                colorMap[x][y] = CELL_TYPE.MAP_CROSSROAD
                break
            elif hasOppositeNeighbourCells(currentPosition, direction, colorMap, crossroads):
                colorMap[x][y] = CELL_TYPE.MAP_CROSSROAD
                # crossroads.append(colorMap[x][y])
                # print("close crossroads")
                #try make cross to road
                break
            else:
                colorMap[x][y] = CELL_TYPE.MAP_ROAD
                currentPosition = getOffsettedPoint(currentPosition, direction, 1)
        currentPosition = crossroad

def hasOppositeNeighbourCells(point: Tuple[int, int], direction: int, colorMap: list[list[tuple[int, int, int, int]]], crossroads: list[Tuple[int, int]]):
    oppositeDirections = getOppositesToDirection(direction)
    for oppositeDirection in oppositeDirections:
        x, y = getOffsettedPoint(point, oppositeDirection, 1)
        if colorMap[x][y] == CELL_TYPE.MAP_ROAD:
            return True
        elif colorMap[x][y] == CELL_TYPE.MAP_CROSSROAD:
            # tryDeleteCrossroad((x, y), colorMap, crossroads)
            return True
    return False

def hasNeighbourCells(point: Tuple[int, int], colorMap: list[list[tuple[int, int, int, int]]]):
    for direction in [DIRECTIONS.UP, DIRECTIONS.DOWN, DIRECTIONS.RIGHT, DIRECTIONS.LEFT]:
        x, y = getOffsettedPoint(point, direction, 1)
        if colorMap[x][y] in [CELL_TYPE.MAP_ROAD, CELL_TYPE.MAP_CROSSROAD]:
            return True
    for doubleDirection in [(DIRECTIONS.UP, DIRECTIONS.RIGHT),
                      (DIRECTIONS.UP, DIRECTIONS.LEFT),
                      (DIRECTIONS.DOWN, DIRECTIONS.RIGHT),
                      (DIRECTIONS.DOWN, DIRECTIONS.LEFT)]:
        offsettedPoint = getOffsettedPoint(point, doubleDirection[0], 1)
        x, y = getOffsettedPoint(offsettedPoint, doubleDirection[1], 1)
        if colorMap[x][y] in [CELL_TYPE.MAP_ROAD, CELL_TYPE.MAP_CROSSROAD]:
            return True
    return False

def tryDeleteCrossroad(crossroad: Tuple[int, int], colorMap: list[list[tuple[int, int, int, int]]], crossroads: list[Tuple[int, int]]):
    if hasNeighbourCells(crossroad, colorMap) == False:
        crossroads.remove(crossroad)

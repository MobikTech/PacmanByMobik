import random

from Scripts.Common.CommonFuncs import *
from Scripts.Common.Constants import *
from Scripts.Common.CoordsConverter import *

STEP_LENGTH = 2
FAKE_NODES_COUNT = 15 * 7


class MazeGenerator2():

    def __init__(self):
        self.currentPoint = (1, 1)
        self.previousPoints = dict()
        self.previousPoints[self.currentPoint] = None

        self.colorMap = dict()
        self.initializeColorMap()
        self.colorMapList = colorMapToList(self.colorMap)

    def initializeColorMap(self):
        for x in range(GRID_COLUMNS_COUNT):
            for y in range(GRID_ROWS_COUNT):
                if (x, y) == GRID_CENTER:
                    self.colorMap[(x, y)] = CELL_TYPE.MAP_GHOSTS_START_POSITION
                elif x > 0 and x < GRID_COLUMNS_COUNT - 1 and \
                        y > GRID_CENTER[1] + 1 and y < GRID_ROWS_COUNT - 1:
                    self.colorMap[(x, y)] = CELL_TYPE.MAP_REST_SPACE
                else:
                    self.colorMap[(x, y)] = CELL_TYPE.MAP_WALL

        self.generateGameMap()
        # return self.colorMap

    def generateGameMap(self):
        self.colorMap[(self.currentPoint)] = CELL_TYPE.MAP_CROSSROAD
        while len(self.getPossibleMoves(self.currentPoint)) > 0:
            self.currentPoint = self.randomMove(self.currentPoint)
            self.colorMap[(self.currentPoint)] = CELL_TYPE.MAP_CROSSROAD

    def getPossibleMoves(self, point: Tuple[int, int]):
        possibleDirections = list()
        for direction in getNoneDirectionDictionary().keys():
            nextPoint = getOffsettedPoint(point, direction, STEP_LENGTH)
            if inMapRect(nextPoint) and self.colorMap[nextPoint] != CELL_TYPE.MAP_CROSSROAD:
                possibleDirections.append(direction)
        return possibleDirections

    def randomMove(self, currentPoint: Tuple[int, int]):
        chosenDirection = random.choice(self.getPossibleMoves(currentPoint))
        return self.move(currentPoint, chosenDirection)

    def move(self, currentPoint: Tuple[int, int], direction):
        newPoint = getOffsettedPoint(currentPoint, direction, STEP_LENGTH)
        self.previousPoints[newPoint] = currentPoint
        return newPoint

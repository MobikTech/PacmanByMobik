import random

from Scripts.Common.CommonFuncs import *
from Scripts.Common.Constants import *
from Scripts.Common.CoordsConverter import *


class MazeGenerator():
    CROSSROAD_APPEARANCE_CHANCE = 0.1

    def __init__(self):
        self.colorMap = self.initializeColorMap()
        self.needToAddRoads = True

    def initializeColorMap(self):
        colorMap = [[CELL_TYPE.MAP_WALL for x in range(GRID_COLUMNS_COUNT)]
                    for y in range(GRID_ROWS_COUNT)]

        crossroads = list()
        for x in range(GRID_COLUMNS_COUNT):
            for y in range(GRID_ROWS_COUNT):
                if (x, y) == GRID_CENTER:
                    colorMap[x][y] = CELL_TYPE.MAP_GHOSTS_START_POSITION
                elif x > 0 and x < GRID_COLUMNS_COUNT - 1 and \
                        y > GRID_CENTER[1] + 1 and y < GRID_ROWS_COUNT - 1:
                    colorMap[x][y] = CELL_TYPE.MAP_REST_SPACE


                elif inMapRect((x, y)) and \
                        getRandomBool(MazeGenerator.CROSSROAD_APPEARANCE_CHANCE) and \
                        not hasNeighbourCellsWithOffset((x, y),
                                                        colorMap,
                                                        [CELL_TYPE.MAP_ROAD,
                                                         CELL_TYPE.MAP_CROSSROAD],
                                                        4):
                    crossroads.append((x, y))
                    colorMap[x][y] = CELL_TYPE.MAP_CROSSROAD
                else:
                    colorMap[x][y] = CELL_TYPE.MAP_WALL

        # self._connectWithMap(colorMap, crossroads)
        return colorMap

    def _connectWithMap(self,
                        colorMap: list[list[tuple[int, int, int, int]]],
                        crossroads: list[Tuple[int, int]]):
        for crossroad in crossroads:
            currentPosition = crossroad
            self.needToAddRoads = True
            for direction in getTwoRandomDirections():
                newPosition = getOffsettedPoint(currentPosition, direction, 1)
                if not inMapRect(newPosition):
                    direction = getOppositeDirection(direction)
                if self.needToAddRoads == False:
                    break
                self._tryAddRoadsByDirection(crossroad,
                                             direction,
                                             colorMap,
                                             crossroads)

            # isDone = False
            # while not isDone:
            #     isDone = _tryAddRoadsByDirection(crossroad,
            #                                      direction,
            #                                      colorMap,
            #                                      crossroads)

        # while _inMapRect(CENTER_GRID_SPACE, currentPosition):
        #     x, y = currentPosition
        #     if colorMap[x][y] == CELL_TYPE.MAP_CROSSROAD:
        #         break
        #     elif colorMap[x][y] == CELL_TYPE.MAP_ROAD:
        #         colorMap[x][y] = CELL_TYPE.MAP_CROSSROAD
        #         break
        #     elif hasOppositeNeighbourCells(currentPosition, direction, colorMap, crossroads):
        #         colorMap[x][y] = CELL_TYPE.MAP_CROSSROAD
        #         # crossroads.append(colorMap[x][y])
        #         # print("close crossroads")
        #         # try make cross to road
        #         break
        #     else:
        #         colorMap[x][y] = CELL_TYPE.MAP_ROAD
        #         currentPosition = getOffsettedPoint(currentPosition, direction, 1)
        # currentPosition = crossroad

    def _tryAddRoadsByDirection(self, crossroad, direction1, colorMap, crossroads):
        canAddRoads = True
        currentPosition = crossroad
        direction = direction1

        if isConnectedWithRoads(crossroad, colorMap):
            return True
        # if hasNeighbourCells(crossroad, colorMap, [CELL_TYPE.MAP_CROSSROAD]):
        #     self.needToAddRoads = False
        #     colorMap[crossroad[0]][crossroad[1]] = CELL_TYPE.MAP_WALL
        #     return False
        while canAddRoads:
            x, y = newPosition = getOffsettedPoint(currentPosition, direction, 1)
            # neighboursCells = getNeighboursWithoutPrevious(newPosition, colorMap, direction)

            if not inMapRect(newPosition):
                if currentPosition == crossroad:
                    return False
                colorMap[currentPosition[0]][currentPosition[1]] = CELL_TYPE.MAP_CROSSROAD
                # for oppositeDirection in getOppositesToDirection(direction):
                #     self._tryAddRoadsByDirection(currentPosition,
                #                             oppositeDirection,
                #                             colorMap,
                #                             crossroads)
                return True
            elif colorMap[x][y] == CELL_TYPE.MAP_CROSSROAD:
                # Z-like connection handler
                if currentPosition == crossroad:

                    newPointConnections = getNoneDirectionDictionary()
                    oppositesConnectionsCount = 0
                    for oppositeDirection in getAnotherDirections(getOppositeDirection(direction)):
                        newX, newY = getOffsettedPoint((x, y), oppositeDirection, 1)
                        if colorMap[newX][newY] in [CELL_TYPE.MAP_ROAD,
                                                    CELL_TYPE.MAP_CROSSROAD]:
                            newPointConnections[oppositeDirection] = (newX, newY)
                    singleOppositeDirection = None
                    for dir in getOppositesToDirection(direction):
                        if newPointConnections[dir] != None:
                            oppositesConnectionsCount += 1
                            singleOppositeDirection = dir
                    if oppositesConnectionsCount == 0:
                        colorMap[x][y] = CELL_TYPE.MAP_ROAD
                        currentPosition = newPosition
                    elif oppositesConnectionsCount == 1:
                        x2, y2 = getOffsettedPoint(currentPosition, singleOppositeDirection, 1)
                        colorMap[x2][y2] = CELL_TYPE.MAP_ROAD
                        currentPosition = (x2, y2)
                        direction = singleOppositeDirection
                    elif oppositesConnectionsCount == 2:
                        colorMap[currentPosition[0]][currentPosition[1]] = CELL_TYPE.MAP_ROAD
                        direction = getOppositeDirection(direction)
                        self.needToAddRoads = False

                    return True
                colorMap[currentPosition[0]][currentPosition[1]] = CELL_TYPE.MAP_ROAD
                return True
            # elif colorMap[x][y] == CELL_TYPE.MAP_ROAD:
            #     xNew, yNew = getOffsettedPoint(newPosition, direction, 1)
            #     if currentPosition != crossroad and \
            #         colorMap[xNew][yNew] != CELL_TYPE.MAP_CROSSROAD:
            #         colorMap[x][y] = CELL_TYPE.MAP_CROSSROAD
            #         return True
            #     colorMap[x][y] = CELL_TYPE.MAP_ROAD
            #     return True
            # elif hasCellTypeNeighboursWithoutCurrent(newPosition,
            #                                           colorMap,
            #                                           direction,
            #                                           CELL_TYPE.MAP_CROSSROAD):
            #     # tryRemoveSideCrossroads(newPosition, colorMap, direction, crossroads)
            #     colorMap[x][y] = CELL_TYPE.MAP_CROSSROAD
            #     return True
            # elif hasCellTypeNeighboursWithoutCurrent(newPosition,
            #                                          colorMap,
            #                                          direction,
            #                                          CELL_TYPE.MAP_ROAD):
            #     colorMap[x][y] = CELL_TYPE.MAP_CROSSROAD
            #     return True

            colorMap[x][y] = CELL_TYPE.MAP_ROAD
            currentPosition = newPosition


def hasCellTypeNeighboursWithoutCurrent(point, colorMap, direction, cellType):
    neighbours = list()
    for newDirection in getAnotherDirections(getOppositeDirection(direction)):
        x, y = getOffsettedPoint(point, newDirection, 1)
        if colorMap[x][y] == cellType:
            neighbours.append((x, y))
    if len(neighbours) > 0:
        return neighbours
    return None


def getNeighboursWithoutPrevious(point, colorMap, direction):
    neighbours = {DIRECTIONS.UP: None,
                  DIRECTIONS.DOWN: None,
                  DIRECTIONS.RIGHT: None,
                  DIRECTIONS.LEFT: None, }
    for newDirection in getAnotherDirections(getOppositeDirection(direction)):
        x, y = getOffsettedPoint(point, newDirection, 1)
        if colorMap[x][y] in [CELL_TYPE.MAP_ROAD,
                              CELL_TYPE.MAP_CROSSROAD]:
            neighbours[direction] = (x, y)
    return neighbours


def tryRemoveSideCrossroads(point, colorMap, direction, crossroads: list):
    for direction in getAnotherDirections(direction):
        x, y = offsettedPoint = getOffsettedPoint(point, direction, 1)
        if colorMap[x][y] == CELL_TYPE.MAP_CROSSROAD:
            if isConnectedWithRoad(offsettedPoint, colorMap) == False:
                crossroads.remove(offsettedPoint)
                colorMap[x][y] = CELL_TYPE.MAP_WALL


def isConnectedWithRoads(point, colorMap):
    verticalDirections = [DIRECTIONS.UP, DIRECTIONS.DOWN]
    horizontalDirections = [DIRECTIONS.RIGHT, DIRECTIONS.LEFT]
    verticalFlag = False
    horizontalFlag = False
    for direction in verticalDirections:
        x, y = getOffsettedPoint(point, direction, 1)
        if colorMap[x][y] == CELL_TYPE.MAP_ROAD:
            verticalFlag = True
    for direction in horizontalDirections:
        x, y = getOffsettedPoint(point, direction, 1)
        if colorMap[x][y] == CELL_TYPE.MAP_ROAD:
            horizontalFlag = True
    return verticalFlag and horizontalFlag


def hasOppositeNeighbourCells(point: Tuple[int, int],
                              direction: int,
                              colorMap: list[list[tuple[int, int, int, int]]],
                              crossroads: list[Tuple[int, int]]):
    oppositeDirections = getOppositesToDirection(direction)
    for oppositeDirection in oppositeDirections:
        x, y = getOffsettedPoint(point, oppositeDirection, 1)
        if colorMap[x][y] == CELL_TYPE.MAP_ROAD:
            return True
        elif colorMap[x][y] == CELL_TYPE.MAP_CROSSROAD:
            # tryDeleteCrossroad((x, y), colorMap, crossroads)
            return True
    return False


def hasNeighbourCells(point: Tuple[int, int],
                      colorMap: list[list[tuple[int, int, int, int]]],
                      cellTypes, offset):
    for direction in [DIRECTIONS.UP,
                      DIRECTIONS.DOWN,
                      DIRECTIONS.RIGHT,
                      DIRECTIONS.LEFT]:
        x, y = getOffsettedPoint(point, direction, offset)
        if colorMap[x][y] in cellTypes:
            return True
    for doubleDirection in [(DIRECTIONS.UP, DIRECTIONS.RIGHT),
                            (DIRECTIONS.UP, DIRECTIONS.LEFT),
                            (DIRECTIONS.DOWN, DIRECTIONS.RIGHT),
                            (DIRECTIONS.DOWN, DIRECTIONS.LEFT)]:
        offsettedPoint = getOffsettedPoint(point, doubleDirection[0], offset)
        x, y = getOffsettedPoint(offsettedPoint, doubleDirection[1], offset)
        if colorMap[x][y] in cellTypes:
            return True
    return False


def hasNeighbourCellsWithOffset(point: Tuple[int, int],
                                colorMap: list[list[tuple[int, int, int, int]]],
                                cellTypes,
                                radiusInCells):
    offset = radiusInCells
    while offset > 0:
        if hasNeighbourCells(point, colorMap, cellTypes, offset):
            return True
        offset -= 1
    return False


def tryDeleteCrossroad(crossroad: Tuple[int, int],
                       colorMap: list[list[tuple[int, int, int, int]]],
                       crossroads: list[Tuple[int, int]]):
    if hasNeighbourCells(crossroad, colorMap) == False:
        crossroads.remove(crossroad)

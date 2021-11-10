from Scripts.Old.Common.CommonFuncs import *
from Scripts.Old.Common.CoordsConverter import *


class MazeGenerator():
    # SCREEN_WIDTH = None
    # SCREEN_HEIGHT = None
    # SCREEN_CENTER = None

    CROSSROAD_APPEARANCE_CHANCE = 10

    def __init__(self):
        MazeGenerator.SCREEN_CENTER = (screenWidth / 2, screenHeight / 2)
        self.colorMap = self.initializeColorMap()

    def initializeColorMap(self):
        colorMap = [[CELL_TYPE.WALL for x in range(COLUMNS_COUNT)] for y in range(ROWS_COUNT)]

        # turnCount = 0
        # currentPosition = (CENTER_GRID_SPACE[0], CENTER_GRID_SPACE[0] - 1)
        # currentDirection = DIRECTIONS.UP
        #
        # while turnCount < 30:
        #     x, y = currentPosition
        #     colorMap[x][y] = CELL_TYPE.MAP_ROAD
        #     if random.randint(1, 5) == 1:
        #         currentDirection = random.choice(getOppositesToDirection(currentDirection))
        #         turnCount += 1
        #
        #
        #
        #     newPosition = getOffsettedPoint(currentPosition, currentDirection, 1)
        #     if _inMapRect(CENTER_GRID_SPACE, newPosition[0], newPosition[1]) == False:
        #         currentDirection
        #     currentPosition = newPosition

        crossroads = list()
        for x in range(COLUMNS_COUNT):
            for y in range(ROWS_COUNT):
                if (x, y) == CENTER_GRID_SPACE:
                    colorMap[x][y] = CELL_TYPE.GHOSTS_START_POSITION
                elif x > 0 and x < COLUMNS_COUNT - 1 and y > CENTER_GRID_SPACE[1] + 1 and y < ROWS_COUNT - 1:
                    colorMap[x][y] = CELL_TYPE.MAP_REST_SPACE


                elif    inMapRect(CENTER_GRID_SPACE, (x, y)) and \
                        random.randint(1, MazeGenerator.CROSSROAD_APPEARANCE_CHANCE) == 1 and \
                        hasNeighbourCells((x, y), colorMap) == False:
                    crossroads.append((x, y))
                    colorMap[x][y] = CELL_TYPE.CROSSROAD
                else:
                    colorMap[x][y] = CELL_TYPE.WALL

        for crossroad in crossroads:
            _addRoadsToCrossroad(crossroad, colorMap, crossroads)

        return colorMap




def _addRoadsToCrossroad(crossroad: Tuple[int, int], colorMap: list[list[tuple[int, int, int, int]]],
                        crossroads: list[Tuple[int, int]]):
    directions = getTwoRandomDirections()
    currentPosition = crossroad

    for direction in directions:
        newPosition = getOffsettedPoint(currentPosition, direction, 1)
        if inMapRect(CENTER_GRID_SPACE, newPosition) == False:
            direction = getOppositeDirection(direction)
        _tryAddRoadsByDirection(crossroad, direction, colorMap, crossroads)



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


def _tryAddRoadsByDirection(crossroad, direction, colorMap, crossroads):
    canAddRoads = True
    currentPosition = crossroad

    while canAddRoads:
        newPosition = getOffsettedPoint(currentPosition, direction, 1)
        x, y = newPosition

        if inMapRect(CENTER_GRID_SPACE, newPosition) == False:
            crossroads.append(colorMap[currentPosition[0]][currentPosition[1]])
            colorMap[currentPosition[0]][currentPosition[1]] = CELL_TYPE.CROSSROAD
            _tryAddRoadsByDirection(currentPosition, getOppositesToDirection(direction), colorMap, crossroads)
            break
        elif colorMap[x][y] == CELL_TYPE.CROSSROAD:
            break
        # elif hasCrossroadNeighboursWithoutCurrent(newPosition, colorMap, direction):
        #     tryRemoveSideCrossroads(newPosition, colorMap, direction, crossroads)
        #     colorMap[x][y] = CELL_TYPE.MAP_CROSSROAD
        #     break
        else:
            colorMap[x][y] = CELL_TYPE.ROAD
            currentPosition = newPosition



    # while _inMapRect(CENTER_GRID_SPACE, currentPosition):
    #
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
    # pass


def hasCrossroadNeighboursWithoutCurrent(point, colorMap, direction):
    for direction in getAnotherDirections(direction):
        x, y = getOffsettedPoint(point, direction, 1)
        if colorMap[x][y] == CELL_TYPE.CROSSROAD:
            return True
    return False

def tryRemoveSideCrossroads(point, colorMap, direction, crossroads: list):
    for direction in getAnotherDirections(direction):
        x, y = offsettedPoint = getOffsettedPoint(point, direction, 1)
        if colorMap[x][y] == CELL_TYPE.CROSSROAD:
            if isConnectedWithRoad(offsettedPoint, colorMap) == False:
                crossroads.remove(offsettedPoint)
                colorMap[x][y] = CELL_TYPE.WALL

def isConnectedWithRoad(point, colorMap):
    for direction in [DIRECTIONS.UP, DIRECTIONS.DOWN, DIRECTIONS.RIGHT, DIRECTIONS.LEFT]:
        x, y = getOffsettedPoint(point, direction, 1)
        if colorMap[x][y] == CELL_TYPE.ROAD:
            return True
    return False






def hasOppositeNeighbourCells(point: Tuple[int, int], direction: int, colorMap: list[list[tuple[int, int, int, int]]],
                              crossroads: list[Tuple[int, int]]):
    oppositeDirections = getOppositesToDirection(direction)
    for oppositeDirection in oppositeDirections:
        x, y = getOffsettedPoint(point, oppositeDirection, 1)
        if colorMap[x][y] == CELL_TYPE.ROAD:
            return True
        elif colorMap[x][y] == CELL_TYPE.CROSSROAD:
            # tryDeleteCrossroad((x, y), colorMap, crossroads)
            return True
    return False

def hasNeighbourCells(point: Tuple[int, int], colorMap: list[list[tuple[int, int, int, int]]]):
    for direction in [DIRECTIONS.UP, DIRECTIONS.DOWN, DIRECTIONS.RIGHT, DIRECTIONS.LEFT]:
        x, y = getOffsettedPoint(point, direction, 1)
        if colorMap[x][y] in [CELL_TYPE.ROAD, CELL_TYPE.CROSSROAD]:
            return True
    for doubleDirection in [(DIRECTIONS.UP, DIRECTIONS.RIGHT),
                            (DIRECTIONS.UP, DIRECTIONS.LEFT),
                            (DIRECTIONS.DOWN, DIRECTIONS.RIGHT),
                            (DIRECTIONS.DOWN, DIRECTIONS.LEFT)]:
        offsettedPoint = getOffsettedPoint(point, doubleDirection[0], 1)
        x, y = getOffsettedPoint(offsettedPoint, doubleDirection[1], 1)
        if colorMap[x][y] in [CELL_TYPE.ROAD, CELL_TYPE.CROSSROAD]:
            return True
    return False


def tryDeleteCrossroad(crossroad: Tuple[int, int], colorMap: list[list[tuple[int, int, int, int]]],
                       crossroads: list[Tuple[int, int]]):
    if hasNeighbourCells(crossroad, colorMap) == False:
        crossroads.remove(crossroad)

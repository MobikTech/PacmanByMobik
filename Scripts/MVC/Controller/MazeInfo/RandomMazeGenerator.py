import random

from Scripts.MVC.Controller.Common.CommonClasses import DirectionManager, Random
from Scripts.MVC.Controller.Common.Constants import *
from Scripts.MVC.Model.Navigation.Coords import Coords


class RandomMazeGenerator():

    @staticmethod
    def initializeGrid():
        grid = dict()
        for x in range(GRID.COLUMNS_COUNT):
            for y in range(GRID.ROWS_COUNT):
                coords = Coords((x, y))
                if coords.getTuple() == (GRID.CENTER[0], GRID.CENTER[1] + 1):
                    grid[coords.getTuple()] = CELL_TYPE.GHOSTS_START_POSITION
                elif RandomMazeGenerator.inRestSpaceRect(coords):
                    grid[coords.getTuple()] = CELL_TYPE.REST_SPACE
                else:
                    grid[coords.getTuple()] = CELL_TYPE.WALL

        GenerationFuncs.createGameMap(grid)
        RandomMazeGenerator.__addCrossroads(grid)
        RandomMazeGenerator.__addPlayerStartPosition(grid)
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

    @staticmethod
    def getWalls(grid):
        wallsList = list()
        for x in range(RANDOM_MAP_SETTINGS.MAP_TOP_LEFT_CORNER[0], RANDOM_MAP_SETTINGS.MAP_BOTTOM_RIGHT_CORNER[0] + 1):
            for y in range(RANDOM_MAP_SETTINGS.MAP_TOP_LEFT_CORNER[1],
                           RANDOM_MAP_SETTINGS.MAP_BOTTOM_RIGHT_CORNER[1] + 1):
                if grid[(x, y)] == CELL_TYPE.WALL:
                    wallsList.append(Coords((x, y)))
        return wallsList

    @staticmethod
    def getRoads(grid):
        roadsList = list()
        for x in range(RANDOM_MAP_SETTINGS.MAP_TOP_LEFT_CORNER[0], RANDOM_MAP_SETTINGS.MAP_BOTTOM_RIGHT_CORNER[0] + 1):
            for y in range(RANDOM_MAP_SETTINGS.MAP_TOP_LEFT_CORNER[1],
                           RANDOM_MAP_SETTINGS.MAP_BOTTOM_RIGHT_CORNER[1] + 1):
                if grid[(x, y)] == CELL_TYPE.ROAD:
                    roadsList.append(Coords((x, y)))
        return roadsList

    @staticmethod
    def __addCrossroads(grid):
        for road in RandomMazeGenerator.getRoads(grid):
            if RandomMazeGenerator.__shouldItBeCrossroad(road, grid):
                grid[road.getTuple()] = CELL_TYPE.CROSSROAD

        grid[GRID.CENTER] = CELL_TYPE.CROSSROAD

    @staticmethod
    def __shouldItBeCrossroad(coords, grid):
        toRoadDirections = list()
        for direction in GenerationFuncs.getPossibleDirections(coords):
            offsettedPoint = coords.getOffsetted(direction, 1)
            if grid[offsettedPoint.getTuple()] in [CELL_TYPE.ROAD, CELL_TYPE.CROSSROAD]:
                toRoadDirections.append(direction)
        if len(toRoadDirections) == 2 and \
                toRoadDirections[0] == DirectionManager.getOppositeToDirection(toRoadDirections[1]):
            return False
        return True

    @staticmethod
    def __addPlayerStartPosition(grid):
        currentCell_Y = 0
        while grid[(GRID.CENTER[0], currentCell_Y)] != CELL_TYPE.ROAD:
            currentCell_Y += 1
        grid[(GRID.CENTER[0], currentCell_Y)] = CELL_TYPE.PACMAN_START_POSITION


class GenerationFuncs():

    @staticmethod
    def createGameMap(grid: dict[tuple[int, int]]):
        firstPoint = Coords((RANDOM_MAP_SETTINGS.MAP_TOP_LEFT_CORNER))
        GenerationFuncs.__buildRandomCrossing(firstPoint, grid)
        GenerationFuncs.__makeConsistent(grid)

    @staticmethod
    def __buildRandomCrossing(coords: Coords, grid):
        possibleDirections = GenerationFuncs.getPossibleDirections(coords)
        random.shuffle(possibleDirections)
        for direction in possibleDirections:
            if GenerationFuncs.__canMakeRoad(coords, direction, grid):
                newPoint = GenerationFuncs.__connectNewRoad(coords, direction, grid)
                GenerationFuncs.__buildRandomCrossing(newPoint, grid)

    @staticmethod
    def getPossibleDirections(coords: Coords):
        possibleDirections = list()
        for direction in DirectionManager.ALL_DIRECTIONS:
            if RandomMazeGenerator.inMapRect(coords.getOffsetted(direction, 1)):
                possibleDirections.append(direction)
        return possibleDirections

    @staticmethod
    def __canMakeRoad(point: Coords, direction, grid):
        STEP_OFFSET = 2
        if grid[point.getOffsetted(direction, STEP_OFFSET).getTuple()] != CELL_TYPE.ROAD:
            return True
        return False

    @staticmethod
    def __connectNewRoad(coords: Coords, direction, grid):
        newCoords = coords.getOffsetted(direction, 1)
        grid[newCoords.getTuple()] = CELL_TYPE.ROAD
        newCoords = coords.getOffsetted(direction, 2)
        grid[newCoords.getTuple()] = CELL_TYPE.ROAD
        return newCoords

    @staticmethod
    def __makeConsistent(grid):
        CHANCE_OF_WALL_REMOVING = 0.15
        wallsList = RandomMazeGenerator.getWalls(grid)
        for wallCoords in wallsList:
            if GenerationFuncs.__couldBeRemoved(wallCoords, grid) and \
                    Random.getBool(CHANCE_OF_WALL_REMOVING):
                grid[wallCoords.getTuple()] = CELL_TYPE.ROAD

    @staticmethod
    def __couldBeRemoved(wallCoords: Coords, grid):
        toRoadDirections = list()
        for direction in GenerationFuncs.getPossibleDirections(wallCoords):
            offsettedPoint = wallCoords.getOffsetted(direction, 1)
            if grid[offsettedPoint.getTuple()] == CELL_TYPE.ROAD:
                toRoadDirections.append(direction)

        if len(toRoadDirections) == 2 and \
                toRoadDirections[0] == DirectionManager.getOppositeToDirection(toRoadDirections[1]):
            return True
        return False

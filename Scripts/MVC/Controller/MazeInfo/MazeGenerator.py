import random
import pygame
from pygame.image import load
from Scripts.MVC.Controller.Common.Constants import *
from Scripts.MVC.Controller.MazeInfo.RandomMazeGenerator import RandomMazeGenerator
from Scripts.MVC.Controller.MazeInfo.SurfaceMaker import SurfaceMaker
from Scripts.MVC.Model.Navigation.Coords import Coords
from Scripts.MVC.Model.Navigation.Nodes import Node, NodeInfo
from Scripts.MVC.Controller.Common.CommonClasses import DirectionManager


class MazeGenerator():
    def __init__(self):
        self.grid = dict()

        self.playerStartPosition = None
        self.playerStartDirection = None

        self.ghostsStartPosition = None
        self.ghostsStartDirection = None

        self.roadsPositions = list()
        self.nodeDictionary = dict()

        self.backgroundImage = None

        # self.__setGridFromFile('pacman_map_1_31x31.png')
        self.__setGridRandomly()
        self.__scanGrid()
        self.__defineNodesNeighbours()
        self.__setBackground()

    def __setGridFromFile(self, fileName: str):
        self.grid = getColorMap(load(MAIN_DIRECTORY + '\Sprites\\' + fileName))

    def __setGridRandomly(self):
        self.grid = RandomMazeGenerator.initializeGrid()

    def __scanGrid(self):
        for x in range(GRID.COLUMNS_COUNT):
            for y in range(GRID.ROWS_COUNT):
                currentCell = self.grid[(x, y)]
                if currentCell == CELL_TYPE.PACMAN_START_POSITION:
                    self.playerStartPosition = Coords((x, y))
                    self.playerStartDirection = random.choice(
                        DirectionManager.getPossibleDirections(self.playerStartPosition, self.grid))
                elif currentCell == CELL_TYPE.GHOSTS_START_POSITION:
                    self.ghostsStartPosition = Coords((x, y))
                    self.ghostsStartDirection = random.choice(
                        DirectionManager.getPossibleDirections(self.ghostsStartPosition, self.grid))
                elif currentCell == CELL_TYPE.ROAD:
                    self.roadsPositions.append((x, y))
                elif currentCell == CELL_TYPE.CROSSROAD:
                    self.nodeDictionary[(x, y)] = Node((x, y))

    def __defineNodesNeighbours(self):
        for node in self.nodeDictionary.values():
            for direction in node.neighborsNodeInfo.keys():
                offsettedPoint = node.coords.getOffsetted(direction, 1).getTuple()
                if self.grid[offsettedPoint] in (CELL_TYPE.ROAD,
                                                 CELL_TYPE.CROSSROAD,
                                                 CELL_TYPE.PACMAN_START_POSITION):
                    currentDistance = 1
                    while self.grid[node.coords.getOffsetted(direction, currentDistance).getTuple()] != CELL_TYPE.CROSSROAD:
                        currentDistance += 1
                    node.neighborsNodeInfo[direction] = NodeInfo(
                        self.nodeDictionary[node.coords.getOffsetted(direction, currentDistance).getTuple()],
                        currentDistance)

    def __setBackground(self):
        self.backgroundImage = SurfaceMaker.getSurface(self.grid)


def getColorMap(pixelColorImage: pygame.Surface):
    pixelMap = pygame.pixelarray.PixelArray(pixelColorImage)
    x, y = pixelMap.shape
    colorMap = dict()
    for i in range(x):
        for k in range(y):
            colorMap[(i, k)] = SurfaceMaker.getCellType(pixelColorImage.unmap_rgb(pixelMap[i][k]))
    return colorMap

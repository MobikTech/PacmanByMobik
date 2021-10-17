import random
import pygame
from pygame.image import load
from Scripts.MVC.Controller.Common.Constants import *
from Scripts.MVC.Model.Navigation.Coords import Coords
from Scripts.MVC.Model.Navigation.Nodes import Node, NodeInfo
from Scripts.MVC.Model.Common.DirectionFuncs import getPossibleDirections


class MazeGenerator():
    def __init__(self):
        self.grid: dict[tuple[int, int]] = dict()

        self.playerStartPosition = None
        self.playerStartDirection = None

        self.ghostsStartPosition = None
        self.ghostsStartDirection = None

        self.roadsPositions = list()
        self.nodeDictionary = dict()

        self.__setGridFromFile('pacman_map_1_31x31.png')
        # self.__setGridRandomly()
        self.__scanGrid()
        self.__defineNodesNeighbours()

    def __setGridFromFile(self, fileName):
        self.grid = getColorMap(load(MAIN_DIRECTORY + '\Sprites\\' + fileName))

    def __setGridRandomly(self):
        pass

    def __scanGrid(self):
        for x in range(GRID.COLUMNS_COUNT):
            for y in range(GRID.ROWS_COUNT):
                currentCellColor = self.grid[(x, y)]
                if currentCellColor == CELL_TYPE.MAP_PACMAN_START_POSITION:
                    self.playerStartPosition = Coords((x, y))
                    self.playerStartDirection = random.choice(
                        getPossibleDirections(self.playerStartPosition, self.grid))
                elif currentCellColor == CELL_TYPE.MAP_GHOSTS_START_POSITION:
                    self.ghostsStartPosition = Coords((x, y))
                    self.ghostsStartDirection = random.choice(
                        getPossibleDirections(self.ghostsStartPosition, self.grid))
                elif currentCellColor == CELL_TYPE.MAP_ROAD:
                    self.roadsPositions.append(Coords((x, y)))
                elif currentCellColor == CELL_TYPE.MAP_CROSSROAD:
                    self.nodeDictionary[(x, y)] = Node((x, y))

    def __defineNodesNeighbours(self):
        for node in self.nodeDictionary.values():
            for direction in node.neighborsNodeInfo.keys():
                offsettedPoint = node.coords.getOffsetted(direction, 1)
                if self.grid[offsettedPoint] in (CELL_TYPE.MAP_ROAD,
                                                 CELL_TYPE.MAP_CROSSROAD,
                                                 CELL_TYPE.MAP_PACMAN_START_POSITION):
                    currentDistance = 1
                    while self.grid[node.coords.getOffsetted(direction, currentDistance)] != CELL_TYPE.MAP_CROSSROAD:
                        currentDistance += 1
                    node.neighborsNodeInfo[direction] = NodeInfo(
                        self.nodeDictionary[node.coords.getOffsetted(direction, currentDistance)],
                        currentDistance)


def getColorMap(pixelColorImage: pygame.Surface):
    pixelMap = pygame.pixelarray.PixelArray(pixelColorImage)
    x, y = pixelMap.shape
    colorMap = dict()
    for i in range(x):
        for k in range(y):
            colorMap[(x, y)] = pixelColorImage.unmap_rgb(pixelMap[i][k])
    return colorMap

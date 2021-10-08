from pygame import Surface

from Scripts.Common.CommonFuncs import *
from Scripts.Entities.Sprites.CoinSprite import CoinSprite
from Node import Node
from Scripts.Common.CoordsConverter import *


# Map-making inctructions:
# yellow (255, 255, 0, 255) - pacman start point
# pink (255, 0, 255, 255) - ghosts spawn point
# black (0, 0, 0, 255) - roads
# green (0, 255, 0, 255) - crossroads
# blue (0, 0, 255, 255) - walls
# white (255, 255, 255, 255) - non-active space(for example, for UI)
# red (255, 0, 0, 255) - door for spirit house


class Map(object):
    def __init__(self,
                 colorMap: list[list[tuple[int, int, int, int]]],
                 backgroundImage: Surface):
        self.colorMap = colorMap

        # refactor: add random generation of background image
        self.background = backgroundImage
        self.background.get_rect().center = CENTER

        self.playerStartWorldPosition = None
        self.ghostsStartWorldPosition = None
        self.nodeDictionary = dict()
        self.roadList = list(Tuple[int, int])
        # remove
        self.crossroadList = self.nodeDictionary.keys()

        self.scanColorMap()
        self.defineNodesNeighbours()

    def scanColorMap(self):

        for x in range(COLUMNS_COUNT):
            for y in range(ROWS_COUNT):
                currentCellColor = self.colorMap[x][y]
                if currentCellColor == CELL_TYPE.MAP_PACMAN_START_POSITION:
                    self.playerStartWorldPosition = gridToWorld(x, y)
                elif currentCellColor == CELL_TYPE.MAP_GHOSTS_START_POSITION:
                    self.ghostsStartWorldPosition = gridToWorld(x, y)
                elif currentCellColor == CELL_TYPE.MAP_ROAD:
                    self.roadList.append((x, y))
                elif currentCellColor == CELL_TYPE.MAP_CROSSROAD:
                    self.nodeDictionary[(x, y)] = Node((x, y))
        pass

    def defineNodesNeighbours(self):
        for node in self.nodeDictionary.values():
            for direction in node.neighbourNodes.keys():
                if (node.gridPosition + directionToVector(direction)) in (CELL_TYPE.MAP_ROAD,
                                                                          CELL_TYPE.MAP_CROSSROAD,
                                                                          CELL_TYPE.MAP_PACMAN_START_POSITION):
                    currentGridPosition = (node.gridPosition + directionToVector(direction))
                    currentDistance = 1
                    while node.gridPosition != CELL_TYPE.MAP_CROSSROAD:
                        currentGridPosition += directionToVector(direction)
                        currentDistance += 1
                    node.neighbourNodes[direction] = (self.nodeDictionary[currentGridPosition], currentDistance)
                    # node.neighbourNodesDistances[direction] = currentDistance

    # # refactor
    # def resetVisited(self):
    #     for node in self.nodeDictionary:
    #         self.nodeDictionary[node].isVisited = False
    # # refactor
    # def resetDistances(self):
    #     for node in self.nodeDictionary:
    #         self.nodeDictionary[node].distanceToThis = None


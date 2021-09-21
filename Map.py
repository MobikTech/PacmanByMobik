import pygame
from Constants import *
from CommonFuncs import *
from Coin import Coin
from Node import Node


# Map-making inctructions:
# yellow (255, 255, 0, 255) - pacman start point
# pink (255, 0, 255, 255) - ghosts spawn point
# black (0, 0, 0, 255) - roads
# green (0, 255, 0, 255) - crossroads
# blue (0, 0, 255, 255) - walls
# white (255, 255, 255, 255) - non-active space(for example, for UI)
# red (255, 0, 0, 255) - door for spirit house

class Map(object):
    def __init__(self, image: pygame.Surface, background: pygame.Surface):
        self.mapImage = image
        self.background = background
        self.colorMap = self.getColorMap(image)
        self.background.get_rect().center = CENTER
        self.playerStartPosition = None
        self.ghostsStartPosition = None
        # self.mapScan(gameCtr)
        self.nodeDictionary = dict()


    def getColorMap(self, image:pygame.Surface):
        map1 = pygame.pixelarray.PixelArray(image)
        x, y = map1.shape
        colorMap = [[0 for x in range(x)] for y in range(y)]
        for i in range(x):
            for k in range(y):
                colorMap[i][k] = image.unmap_rgb(map1[i][k])
        return colorMap

    def resetVisited(self):
        for node in self.nodeDictionary:
            self.nodeDictionary[node].isVisited = False

    def mapScan(self, gameCtr):
        map = self.colorMap
        for x in range(NCOLUMNS):
            for y in range(NROWS):
                if map[x][y] == MAP_PACMAN_START_POSITION:
                    self.playerStartPosition = gridToWorld(x, y)
                elif map[x][y] == MAP_GHOSTS_START_POSITION:
                    self.ghostsStartPosition = gridToWorld(x, y)
                elif map[x][y] == MAP_ROAD or map[x][y] == MAP_CROSSROAD:
                    gameCtr.coinsMap[x][y] = Coin(gameCtr.sprites_group, gridToWorld(x, y))
                    # gameCtr.coinsMap[x][y] = Coin(pygame.sprite.Group(), gridToWorld(x, y))
                    gameCtr.coinAmount += 1

                if map[x][y] == MAP_CROSSROAD:
                    if (x, y) not in self.nodeDictionary:
                        node = self.nodeDictionary[(x, y)] = Node((x, y))
                        neighbors = self._findNeighbors((x, y))

                        node.topN = neighbors[0][0]
                        node.toTopDistance = neighbors[0][1]

                        node.rightN = neighbors[1][0]
                        node.toRightDistance = neighbors[1][1]

                        node.bottomN = neighbors[2][0]
                        node.toBottomDistance = neighbors[2][1]

                        node.leftN = neighbors[3][0]
                        node.toLeftDistance = neighbors[3][1]

                        # (top, topDistance), (right, rightDistance), (bottom, bottomDistance), (left, leftDistance)
                        # for neighbor in neighbors:
                        #     if neighbor not in self.nodeDictionary:
                        #         self.nodeDictionary[neighbor] = Node(neighbor)
        for node in self.nodeDictionary.values():
            if node.topN != None:
                node.topN = self.nodeDictionary[node.topN]
            if node.rightN != None:
                node.rightN = self.nodeDictionary[node.rightN]
            if node.bottomN != None:
                node.bottomN = self.nodeDictionary[node.bottomN]
            if node.leftN != None:
                node.leftN = self.nodeDictionary[node.leftN]

    def _findNeighbors(self, gridPos: Tuple[int, int]):
        top = None
        right = None
        bottom = None
        left = None
        topDistance = 0
        rightDistance = 0
        bottomDistance = 0
        leftDistance = 0

        currPos = (gridPos[0], gridPos[1])
        while(self.colorMap[currPos[0]][currPos[1] - 1] != MAP_WALL):
            currPos = (currPos[0], currPos[1] - 1)
            topDistance += 1
            if self.colorMap[currPos[0]][currPos[1]] == MAP_CROSSROAD:
                top = (currPos[0], currPos[1])
                break

        currPos = (gridPos[0], gridPos[1])
        while (self.colorMap[currPos[0] + 1][currPos[1]] != MAP_WALL):
            currPos = (currPos[0] + 1, currPos[1])
            rightDistance += 1
            if self.colorMap[currPos[0]][currPos[1]] == MAP_CROSSROAD:
                right = (currPos[0], currPos[1])
                break

        currPos = (gridPos[0], gridPos[1])
        while (self.colorMap[currPos[0]][currPos[1] + 1] != MAP_WALL):
            currPos = (currPos[0], currPos[1] + 1)
            bottomDistance += 1
            if self.colorMap[currPos[0]][currPos[1]] == MAP_CROSSROAD:
                bottom = (currPos[0], currPos[1])
                break

        currPos = (gridPos[0], gridPos[1])
        while (self.colorMap[currPos[0] - 1][currPos[1]] != MAP_WALL):
            currPos = (currPos[0] - 1, currPos[1])
            leftDistance += 1
            if self.colorMap[currPos[0]][currPos[1]] == MAP_CROSSROAD:
                left = (currPos[0], currPos[1])
                break

        return (top, topDistance), (right, rightDistance), (bottom, bottomDistance), (left, leftDistance)

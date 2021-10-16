import random

import pygame
from pygame.sprite import collide_rect
from pygame.surface import Surface
from Scripts.Common.Constants import *
from typing import Tuple

from Scripts.Common.SearchAlgorithmes import aStar
from Scripts.Entities.SpriteEntity import SpriteEntity

from Scripts.Common.CoordsConverter import *
from Scripts.Map.Map import Map
from Scripts.Map.Node import Node


def inCellCenter(point: Tuple[int, int], offsetError):
    OFFSET_ERROR = 1
    cellCenter = gridToWorldT(worldToGridT(point))
    if point[0] > cellCenter[0] - offsetError and \
            point[0] < cellCenter[0] + offsetError and \
            point[1] > cellCenter[1] - offsetError and \
            point[1] < cellCenter[1] + offsetError:
        return True
    return False


def checkToCollision(sprite1: SpriteEntity, sprite2: SpriteEntity):
    return collide_rect(sprite1.sprite, sprite2.sprite)


def findNearestNodeTo(gridPosition, map):
    nodes = map.nodeDictionary
    # if inMapRect(CENTER_GRID_SPACE, gridPosition) == False:
    #     raise Exception('position over the grid of playable map')
    x, y = gridPosition
    if map.colorMap[x][y] == CELL_TYPE.MAP_CROSSROAD:
        return nodes[gridPosition]

    rayLength = 1
    directionsList = [DIRECTIONS.UP, DIRECTIONS.DOWN, DIRECTIONS.RIGHT, DIRECTIONS.LEFT]
    while True:
        for direction in directionsList:
            newPoint = getOffsettedPoint(gridPosition, direction, rayLength)
            if map.colorMap[newPoint[0]][newPoint[1]] == CELL_TYPE.MAP_WALL:
                directionsList.remove(direction)
                continue
            elif map.colorMap[newPoint[0]][newPoint[1]] == CELL_TYPE.MAP_CROSSROAD:
                return nodes[newPoint]
        rayLength += 1


def DrawPath(path: list, color, surface):
    POINT_SIZE = 4
    currentIndex = 0
    for node in path:
        if currentIndex == len(path) - 1:
            pygame.draw.circle(surface, color, gridToWorldT(node.gridPosition), POINT_SIZE)
            return
        nextNode = path[currentIndex + 1]
        directionToNextNode = getDirectionToNeighbour(node.gridPosition, nextNode.gridPosition)
        currentPosition = node.gridPosition
        while currentPosition != nextNode.gridPosition:
            pygame.draw.circle(surface, color, gridToWorldT(currentPosition), POINT_SIZE)
            currentPosition = getOffsettedPoint(currentPosition, directionToNextNode, 1)
        currentIndex += 1

        #
        # if prevNode == None:
        #     pygame.draw.circle(surface, color, gridToWorldT(node.gridPosition), POINT_SIZE)
        # else:
        #     currCoords = node.gridPosition
        #     while currCoords != prevNode.gridPosition:
        #         if node.topN == prevNode:
        #             currCoords = (currCoords[0], currCoords[1] - 1)
        #         elif node.rightN == prevNode:
        #             currCoords = (currCoords[0] + 1, currCoords[1])
        #         elif node.bottomN == prevNode:
        #             currCoords = (currCoords[0], currCoords[1] + 1)
        #         elif node.leftN == prevNode:
        #             currCoords = (currCoords[0] - 1, currCoords[1])
        #         pygame.draw.circle(surface, color, gridToWorldT(currCoords), pointSize)
        # prevNode = node


def getDirectionToNeighbour(startPoint: Tuple[int, int], endPoint: Tuple[int, int]):
    xS, yS = startPoint
    xE, yE = endPoint
    if yE < yS and xE == xS:
        return DIRECTIONS.UP
    if yE > yS and xE == xS:
        return DIRECTIONS.DOWN
    if xE > xS and yE == yS:
        return DIRECTIONS.RIGHT
    if xE < xS and yE == yS:
        return DIRECTIONS.LEFT


def moveSpriteEntity(sprite: SpriteEntity, direction: int, length: int):
    if direction == DIRECTIONS.UP:
        sprite.rect.y -= length
    elif direction == DIRECTIONS.DOWN:
        sprite.rect.y += length
    elif direction == DIRECTIONS.RIGHT:
        sprite.rect.x += length
    elif direction == DIRECTIONS.LEFT:
        sprite.rect.x -= length


# remove
def getDirection(pressedKey: int):
    if pressedKey == pygame.K_w:
        return DIRECTIONS.UP
    elif pressedKey == pygame.K_s:
        return DIRECTIONS.DOWN
    elif pressedKey == pygame.K_d:
        return DIRECTIONS.RIGHT
    elif pressedKey == pygame.K_a:
        return DIRECTIONS.LEFT


def defineDirection(pressedKeys):
    if pressedKeys[pygame.K_w]:
        return DIRECTIONS.UP
    elif pressedKeys[pygame.K_s]:
        return DIRECTIONS.DOWN
    elif pressedKeys[pygame.K_d]:
        return DIRECTIONS.RIGHT
    elif pressedKeys[pygame.K_a]:
        return DIRECTIONS.LEFT
    return None
    # raise Exception("Was pressed wrong key")


def getOppositeDirection(direction):
    if direction == DIRECTIONS.UP:
        return DIRECTIONS.DOWN
    elif direction == DIRECTIONS.DOWN:
        return DIRECTIONS.UP
    elif direction == DIRECTIONS.RIGHT:
        return DIRECTIONS.LEFT
    elif direction == DIRECTIONS.LEFT:
        return DIRECTIONS.RIGHT


def getColorMap(pixelColorImage: Surface):
    pixelMap = pygame.pixelarray.PixelArray(pixelColorImage)
    x, y = pixelMap.shape
    colorMap = [[0 for x in range(x)] for y in range(y)]
    for i in range(x):
        for k in range(y):
            colorMap[i][k] = pixelColorImage.unmap_rgb(pixelMap[i][k])
    return colorMap


def directionToNormalizedVector(direction: int):
    if direction == DIRECTIONS.UP:
        return VECTORS.VECTOR_UP
    elif direction == DIRECTIONS.DOWN:
        return VECTORS.VECTOR_DOWN
    elif direction == DIRECTIONS.RIGHT:
        return VECTORS.VECTOR_RIGHT
    elif direction == DIRECTIONS.LEFT:
        return VECTORS.VECTOR_LEFT
    raise Exception("Was received incorrect direction")


def getCellType(colorMap: list[list[tuple[int, int, int, int]]], gridPosition):
    return colorMap[gridPosition[0]][gridPosition[1]]


def getNextCellType(sprite: SpriteEntity, colorMap: list[list[tuple[int, int, int, int]]], direction: int):
    nextCellPosition = worldToGridT(getOffsettedPoint(sprite.rect.center, direction, CELL_HALF_SIZE + 1))
    return getCellType(colorMap, nextCellPosition)


def getPossibleDirections(sprite: SpriteEntity, colorMap: list[list[tuple[int, int, int, int]]]):
    possibleCellTypes = (CELL_TYPE.MAP_ROAD,
                         CELL_TYPE.MAP_CROSSROAD,
                         CELL_TYPE.MAP_PACMAN_START_POSITION)
    possibleDirections = list()
    for direction in (DIRECTIONS.UP,
                      DIRECTIONS.DOWN,
                      DIRECTIONS.RIGHT,
                      DIRECTIONS.LEFT):
        if getNextCellType(sprite, colorMap, direction) in possibleCellTypes:
            possibleDirections.append(direction)
    return possibleDirections


def getOffsettedPoint(point: Tuple[int, int],
                      direction: int,
                      offset: int):
    vector = directionToNormalizedVector(direction)
    directedOffset = (vector[0] * offset, vector[1] * offset)
    return (point[0] + directedOffset[0], point[1] + directedOffset[1])


def getTwoRandomDirections():
    verticalDirection = random.choice([DIRECTIONS.UP, DIRECTIONS.DOWN])
    horizontalDirection = random.choice([DIRECTIONS.RIGHT, DIRECTIONS.LEFT])
    return [verticalDirection, horizontalDirection]


def getOppositesToDirection(direction: int):
    if direction in [DIRECTIONS.UP, DIRECTIONS.DOWN]:
        return [DIRECTIONS.RIGHT, DIRECTIONS.LEFT]
    elif direction in [DIRECTIONS.RIGHT, DIRECTIONS.LEFT]:
        return [DIRECTIONS.UP, DIRECTIONS.DOWN]


# def getRandomAnotherDirection(direction: int):
#     allDirections = [DIRECTIONS.UP, DIRECTIONS.DOWN, DIRECTIONS.RIGHT, DIRECTIONS.LEFT]
#     allDirections.remove(direction)
#     return random.choice(allDirections)

def getAnotherDirections(direction: int):
    allDirections = [DIRECTIONS.UP, DIRECTIONS.DOWN, DIRECTIONS.RIGHT, DIRECTIONS.LEFT]
    allDirections.remove(direction)
    return allDirections


def inMapRect(gridCenter: Tuple[int, int], position: Tuple[int, int]):
    x, y = position
    if x < COLUMNS_COUNT - 1 and x > 0 and \
            y < gridCenter[1] - 1 and y > 0:
        return True
    return False

def getCoinsPositions(coins: dict):
    coinList = list()
    for position in coins.keys():
        if coins[position] != None:
            coinList.append(position)
    return coinList

def getPathToTarget(startPoint: Tuple[int, int], target: Tuple[int, int], map: Map):
    startNearestNeighbour = findNearestNodeTo(startPoint, map)
    targetNearestNeighbour = findNearestNodeTo(target, map)
    currentPath = aStar(
        startNearestNeighbour,
        targetNearestNeighbour,
        COLORS.WHITE,
        self.layer1)
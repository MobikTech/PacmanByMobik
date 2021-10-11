import pygame
from pygame.sprite import collide_rect
from pygame.surface import Surface
from Scripts.Common.Constants import *
from typing import Tuple
from Scripts.Entities.SpriteEntity import SpriteEntity

from Scripts.Common.CoordsConverter import *


def inCellCenter(point: Tuple[int, int], offsetError):
    OFFSET_ERROR = 1
    cellCenter = gridToWorldT(worldToGridT(point))
    if point[0] > cellCenter[0] - offsetError and \
            point[0] < cellCenter[0] + offsetError and \
            point[1] > cellCenter[1] - offsetError and \
            point[1] < cellCenter[1] + offsetError:
        return True
    return False


# def checkCollision(entity1, entity2):
#     col = pygame.sprite.collide_rect(entity1.sprite, entity2.sprite)
#     if col == True:
#         entity1.collideGhost()
#         entity2.collidePlayer()
#         return True

def checkToCollision(sprite1: SpriteEntity, sprite2: SpriteEntity):
    return collide_rect(sprite1.sprite, sprite2.sprite)

# def findNearestNodeTo(worldPos, map):
#     gridPos = worldToGridT(worldPos)
#     nodes = map.nodeDictionary
#     # Пускает во все 4 стороны лучи, и возвращает узел, который встретился первым
#     if gridPos in nodes:
#         return nodes[gridPos]
#
#     rayLength = 0
#     top = True
#     right = True
#     bottom = True
#     left = True
#
#     while True:
#         if top and map.colorMap[gridPos[0]][gridPos[1] - rayLength] == MAP_WALL:
#             top = False
#         elif right and map.colorMap[gridPos[0] + rayLength][gridPos[1]] == MAP_WALL:
#             right = False
#         elif bottom and map.colorMap[gridPos[0]][gridPos[1] + rayLength] == MAP_WALL:
#             bottom = False
#         elif left and map.colorMap[gridPos[0] - rayLength][gridPos[1]] == MAP_WALL:
#             left = False
#
#         if top and map.colorMap[gridPos[0]][gridPos[1] - rayLength] == MAP_CROSSROAD:
#             return nodes[(gridPos[0], gridPos[1] - rayLength)]
#
#         elif right and map.colorMap[gridPos[0] + rayLength][gridPos[1]] == MAP_CROSSROAD:
#             return nodes[(gridPos[0] + rayLength, gridPos[1])]
#
#         elif bottom and map.colorMap[gridPos[0]][gridPos[1] + rayLength] == MAP_CROSSROAD:
#             return nodes[(gridPos[0], gridPos[1] + rayLength)]
#
#         elif left and map.colorMap[gridPos[0] - rayLength][gridPos[1]] == MAP_CROSSROAD:
#             return nodes[(gridPos[0] - rayLength, gridPos[1])]
#         rayLength += 1


def DrawPath(path: list, color, screen):
    prevNode = None
    pointSize = 4
    for node in path:
        if prevNode == None:
            pygame.draw.circle(screen, color, gridToWorldT(node.gridPosition), pointSize)
        else:
            currCoords = node.gridPosition
            while currCoords != prevNode.gridPosition:
                if node.topN == prevNode:
                    currCoords = (currCoords[0], currCoords[1] - 1)
                elif node.rightN == prevNode:
                    currCoords = (currCoords[0] + 1, currCoords[1])
                elif node.bottomN == prevNode:
                    currCoords = (currCoords[0], currCoords[1] + 1)
                elif node.leftN == prevNode:
                    currCoords = (currCoords[0] - 1, currCoords[1])
                pygame.draw.circle(screen, color, gridToWorldT(currCoords), pointSize)
        prevNode = node


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
                      offsetInPixels: int):
    vector = directionToNormalizedVector(direction)
    directedOffset = (vector[0] * offsetInPixels, vector[1] * offsetInPixels)
    return (point[0] + directedOffset[0], point[1] + directedOffset[1])

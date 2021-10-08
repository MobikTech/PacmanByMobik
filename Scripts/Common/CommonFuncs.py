import pygame
from pygame.surface import Surface

from Constants import *
from typing import Tuple

from Scripts.Entities.SpriteEntity import SpriteEntity


def inSomeRect(point: Tuple[int, int],
               rectCenter: Tuple[int, int],
               rectSide: int):
    if point[0] > rectCenter[0] - rectSide / 2 and point[0] < rectCenter[0] + rectSide / 2 and \
            point[1] > rectCenter[1] - rectSide / 2 and point[1] < rectCenter[1] + rectSide / 2:
        return True
    return False


def raycast(source: Tuple[int, int], map):
    cell = worldToGridT(source)

    if source != gridToWorldT(cell):
        return list()
    # if inSomeRect(source, gridToWorldT(cell), 4) == False:
    #     return list()
    directions = list()
    if map.colorMap[cell[0]][cell[1] - 1] in (MAP_ROAD, MAP_CROSSROAD, MAP_PACMAN_START_POSITION):
        directions.append(UP)
    if map.colorMap[cell[0]][cell[1] + 1] in (MAP_ROAD, MAP_CROSSROAD, MAP_PACMAN_START_POSITION):
        directions.append(DOWN)
    if map.colorMap[cell[0] + 1][cell[1]] in (MAP_ROAD, MAP_CROSSROAD, MAP_PACMAN_START_POSITION):
        directions.append(RIGHT)
    if map.colorMap[cell[0] - 1][cell[1]] in (MAP_ROAD, MAP_CROSSROAD, MAP_PACMAN_START_POSITION):
        directions.append(LEFT)
    return directions


def checkCollision(SpriteEntity1, entity2):
    col = pygame.sprite.collide_rect(entity1.sprite, entity2.sprite)
    if col == True:
        entity1.collideGhost()
        entity2.collidePlayer()
        return True


def findNearestNodeTo(worldPos, map):
    gridPos = worldToGridT(worldPos)
    nodes = map.nodeDictionary
    # Пускает во все 4 стороны лучи, и возвращает узел, который встретился первым
    if gridPos in nodes:
        return nodes[gridPos]

    rayLength = 0
    top = True
    right = True
    bottom = True
    left = True

    while True:
        if top and map.colorMap[gridPos[0]][gridPos[1] - rayLength] == MAP_WALL:
            top = False
        elif right and map.colorMap[gridPos[0] + rayLength][gridPos[1]] == MAP_WALL:
            right = False
        elif bottom and map.colorMap[gridPos[0]][gridPos[1] + rayLength] == MAP_WALL:
            bottom = False
        elif left and map.colorMap[gridPos[0] - rayLength][gridPos[1]] == MAP_WALL:
            left = False

        if top and map.colorMap[gridPos[0]][gridPos[1] - rayLength] == MAP_CROSSROAD:
            return nodes[(gridPos[0], gridPos[1] - rayLength)]

        elif right and map.colorMap[gridPos[0] + rayLength][gridPos[1]] == MAP_CROSSROAD:
            return nodes[(gridPos[0] + rayLength, gridPos[1])]

        elif bottom and map.colorMap[gridPos[0]][gridPos[1] + rayLength] == MAP_CROSSROAD:
            return nodes[(gridPos[0], gridPos[1] + rayLength)]

        elif left and map.colorMap[gridPos[0] - rayLength][gridPos[1]] == MAP_CROSSROAD:
            return nodes[(gridPos[0] - rayLength, gridPos[1])]
        rayLength += 1


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

def getColorMap(pixelColorImage: Surface):
    pixelMap = pygame.pixelarray.PixelArray(pixelColorImage)
    x, y = pixelMap.shape
    colorMap = [[0 for x in range(x)] for y in range(y)]
    for i in range(x):
        for k in range(y):
            colorMap[i][k] = pixelColorImage.unmap_rgb(pixelMap[i][k])
    return colorMap

def directionToVector(direction: int):
    if direction == DIRECTIONS.UP:
        return VECTORS.VECTOR_UP
    if direction == DIRECTIONS.DOWN:
        return VECTORS.VECTOR_DOWN
    if direction == DIRECTIONS.RIGHT:
        return VECTORS.VECTOR_RIGHT
    if direction == DIRECTIONS.LEFT:
        return VECTORS.VECTOR_LEFT

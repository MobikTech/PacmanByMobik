import pygame
from Constants import *
from typing import Tuple

def worldToGrid(worldXPos: int, worldYPos: int):
    x = int(worldXPos / CELL_SIZE)
    y = int(worldYPos / CELL_SIZE)
    return (x, y)

def worldToGridT(worldPos:Tuple[int, int]):
    x = int(worldPos[0] / CELL_SIZE)
    y = int(worldPos[1] / CELL_SIZE)
    return (x, y)

def gridToWorld(gridXPos: int, gridYPos: int):
    x = int(gridXPos * CELL_SIZE + CELL_SIZE/2)
    y = int(gridYPos * CELL_SIZE + CELL_SIZE/2)
    return (x, y)

def gridToWorldT(gridPos:Tuple[int, int]):
    x = int(gridPos[0] * CELL_SIZE + CELL_SIZE/2)
    y = int(gridPos[1] * CELL_SIZE + CELL_SIZE/2)
    return (x, y)

def inSomeRect(point:Tuple[int, int], rectCenter:Tuple[int, int], rectSide:int):
    if point[0] > rectCenter[0] - rectSide/2 and point[0] < rectCenter[0] + rectSide/2 and \
        point[1] > rectCenter[1] - rectSide/2 and point[1] < rectCenter[1] + rectSide/2:
        return True
    return False

def raycast(source:Tuple[int, int], map):
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

def checkCollision(entity1, entity2):
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

    # node = None
    # topD = 0
    # rightD = 0
    # bottomD = 0
    # leftD = 0
    #
    # currPos = worldToGridT(worldPos)
    # while (map.colorMap[currPos[0]][currPos[1] - 1] not in (MAP_WALL, MAP_GHOSTS_START_POSITION, MAP_REST_SPACE)):
    #     currPos = (currPos[0], currPos[1] - 1)
    #     topD += 1
    #     if map.colorMap[currPos[0]][currPos[1]] in (MAP_CROSSROAD, MAP_PACMAN_START_POSITION):
    #         break
    # currPos = worldToGridT(worldPos)
    # while (map.colorMap[currPos[0] + 1][currPos[1]] not in (MAP_WALL, MAP_GHOSTS_START_POSITION, MAP_REST_SPACE)):
    #     currPos = (currPos[0] + 1, currPos[1])
    #     rightD += 1
    #     if map.colorMap[currPos[0]][currPos[1]] in (MAP_CROSSROAD, MAP_PACMAN_START_POSITION):
    #         break
    # currPos = worldToGridT(worldPos)
    # while (map.colorMap[currPos[0]][currPos[1] + 1] not in (MAP_WALL, MAP_GHOSTS_START_POSITION, MAP_REST_SPACE)):
    #     currPos = (currPos[0], currPos[1] + 1)
    #     bottomD += 1
    #     if map.colorMap[currPos[0]][currPos[1]] in (MAP_CROSSROAD, MAP_PACMAN_START_POSITION):
    #         break
    # currPos = worldToGridT(worldPos)
    # while (map.colorMap[currPos[0] - 1][currPos[1]] not in (MAP_WALL, MAP_GHOSTS_START_POSITION, MAP_REST_SPACE)):
    #     currPos = (currPos[0] - 1, currPos[1])
    #     leftD += 1
    #     if map.colorMap[currPos[0]][currPos[1]] in (MAP_CROSSROAD, MAP_PACMAN_START_POSITION):
    #         break
    #
    # minDistance = 100
    # minDir = None
    # nodePositon = gridPos
    # dirDict = {UP: topD, RIGHT: rightD, DOWN: bottomD, LEFT: leftD}
    # for dir in dirDict.keys():
    #     if dirDict[dir] != 0 and dirDict[dir] < minDistance:
    #         minDistance = dirDict[dir]
    #         minDir = dir
    # if minDir == UP:
    #     nodePositon = (nodePositon[0], nodePositon[1] - minDistance)
    # elif minDir == RIGHT:
    #     nodePositon = (nodePositon[0] + minDistance, nodePositon[1])
    # elif minDir == DOWN:
    #     nodePositon = (nodePositon[0], nodePositon[1] + minDistance)
    # elif minDir == LEFT:
    #     nodePositon = (nodePositon[0] - minDistance, nodePositon[1])
    # node = map.nodeDictionary[nodePositon]
    # return node

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

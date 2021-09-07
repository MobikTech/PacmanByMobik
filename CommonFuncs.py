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
    if map.colorMap[cell[0]][cell[1] - 1] == MAP_ROAD or map.colorMap[cell[0]][cell[1] - 1] == MAP_CROSSROAD:
        directions.append(UP)
    if map.colorMap[cell[0]][cell[1] + 1] == MAP_ROAD or map.colorMap[cell[0]][cell[1] + 1] == MAP_CROSSROAD:
        directions.append(DOWN)
    if map.colorMap[cell[0] + 1][cell[1]] == MAP_ROAD or map.colorMap[cell[0] + 1][cell[1]] == MAP_CROSSROAD:
        directions.append(RIGHT)
    if map.colorMap[cell[0] - 1][cell[1]] == MAP_ROAD or map.colorMap[cell[0] - 1][cell[1]] == MAP_CROSSROAD:
        directions.append(LEFT)
    return directions

def checkCollision(entity1, entity2):
    col = pygame.sprite.collide_rect(entity1.sprite, entity2.sprite)
    if col == True:
        entity1.collideGhost()
        entity2.collide()
        return True
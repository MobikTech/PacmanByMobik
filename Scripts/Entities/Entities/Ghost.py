from pygame.sprite import Group
from Scripts.Common.CoordsConverter import *
from Scripts.Common.Constants import *
from Scripts.Map.Map import Map
from Scripts.Entities.SpriteEntity import SpriteEntity

import random



class Ghost():

    GHOST_SPEED = 1

    def __init__(self, spriteGroup: Group,
                 startPosition: Tuple[int, int],
                 file: str,
                 name: str,
                 map: Map,
                 pathColor: Tuple[int, int, int, int]):
        self.sprite = SpriteEntity(spriteGroup, startPosition, file)
        self.name = name
        self.map = map
        self.pathColor = pathColor
        self.speed = Ghost.GHOST_SPEED
        self.startDirection = DIRECTIONS.UP
        self.currentDirection = self.startDirection

    # def move(self):
    #     cell = worldToGridT(self.sprite.rect.center)
    #     if self.map.colorMap[cell[0]][cell[1]] == CELL_TYPE.MAP_CROSSROAD:
    #         directions = raycast(self.rect.center, self.map)
    #         if len(directions) > 0:
    #             self.currentDirection = random.choice(directions)
    #     self.moveByDirection(self.currentDirection)
    #
    #
    # def moveByDirection(self, direction: int):
    #     if direction == UP:
    #         self.rect.y -= self.speed
    #     elif direction == DOWN:
    #         self.rect.y += self.speed
    #     elif direction == RIGHT:
    #         self.rect.x += self.speed
    #     elif direction == LEFT:
    #         self.rect.x -= self.speed
    #
    # def collidePlayer(self):
    #     print(self.name)
import pygame
from Constants import *
from typing import Tuple
from CommonFuncs import *
from Map import Map
import random
from Entity import Entity


class Ghost(Entity):
    def __init__(self, name: str, file: str, spriteGroup: pygame.sprite.Group, startPosition: Tuple[int, int], map: Map):
        Entity.__init__(self, spriteGroup, startPosition, file)
        self.name = name
        self.speed = 1
        self.map = map
        self.direction = UP


    def move(self):
        cell = worldToGridT(self.rect.center)
        if self.map.colorMap[cell[0]][cell[1]] == MAP_CROSSROAD:
            directions = raycast(self.rect.center, self.map)
            if len(directions) > 0:
                self.direction = random.choice(directions)
        self.moveByDirection(self.direction)


    def moveByDirection(self, direction: int):
        if direction == UP:
            self.rect.y -= self.speed
        elif direction == DOWN:
            self.rect.y += self.speed
        elif direction == RIGHT:
            self.rect.x += self.speed
        elif direction == LEFT:
            self.rect.x -= self.speed

    def collide(self):
        print(self.name)
        self.respawn()

    def respawn(self):
        self.rect.center = self.startPosition
        self.direction = UP


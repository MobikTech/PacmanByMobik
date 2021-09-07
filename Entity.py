import pygame
from Constants import *
from typing import Tuple
from CommonFuncs import *


class Entity(object):
    def __init__(self, spriteGroup:pygame.sprite.Group, startPosition:Tuple[int, int], file:str):
        self.sprite = pygame.sprite.Sprite(spriteGroup)

        self.sprite.image = pygame.Surface((CELL_SIZE - 1, CELL_SIZE - 1))
        self.sprite.image = pygame.image.load(file)
        self.rect = self.sprite.rect = self.sprite.image.get_rect()
        self.startPosition = startPosition
        self.rect.center = self.startPosition

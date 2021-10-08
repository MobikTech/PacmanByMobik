import pygame
from Scripts.Entity.Entity import Entity
from typing import Tuple

class Coin(Entity):
    def __init__(self, spriteGroup: pygame.sprite.Group, startPosition: Tuple[int, int]):
        Entity.__init__(self, spriteGroup, startPosition, '../../../Sprites/PacmanCoin.png')

    def removeCoin(self):
        del self
from pygame.sprite import Group
from Scripts.Entities.SpriteEntity import SpriteEntity
from typing import Tuple

class Coin():
    def __init__(self, spriteGroup: Group,
                 startPosition: Tuple[int, int]):
        self.sprite = SpriteEntity(spriteGroup, startPosition, '../../Sprites/PacmanCoin.png')

    def removeCoin(self):
        del self
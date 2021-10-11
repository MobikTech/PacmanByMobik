from pygame.sprite import Group
from Scripts.Entities.CollidableEntity import CollidableEntity
from Scripts.Entities.SpriteEntity import SpriteEntity
from Scripts.Common.Constants import *
from typing import Tuple

class Coin(CollidableEntity):
    def __init__(self, spriteGroup: Group,
                 startWorldPosition: Tuple[int, int]):
        self.spriteEntity = SpriteEntity(SPRITE_TYPES.COIN, spriteGroup, startWorldPosition, MAIN_DIRECTORY + '\Sprites\PacmanCoin.png')

    # def removeCoin(self):
    #     del self

    def collisionHandler(self, sprite: SpriteEntity):
        if sprite.spriteType == SPRITE_TYPES.PACMAN:
            self.spriteEntity.spriteGroup.remove(self.spriteEntity.sprite)
            del self
        elif sprite.spriteType == SPRITE_TYPES.GHOST:
            pass

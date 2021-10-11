from typing import Tuple
from pygame.image import load
from pygame.surface import Surface
from pygame.sprite import *
from Scripts.Common.Constants import *


class SpriteEntity(object):
    SPRITE_SIZE = CELL_SIZE

    def __init__(self, spriteType: int,
                 spriteGroup: Group,
                 startWorldPosition: Tuple[int, int],
                 file: str):
        self.spriteType = spriteType
        self.spriteGroup = spriteGroup
        self.sprite = Sprite(spriteGroup)
        self.sprite.image = Surface((SpriteEntity.SPRITE_SIZE,
                                     SpriteEntity.SPRITE_SIZE))
        self.sprite.image = load(file)
        self.startPosition = startWorldPosition
        self.rect = self.sprite.rect = self.sprite.image.get_rect()
        self.rect.center = self.startPosition

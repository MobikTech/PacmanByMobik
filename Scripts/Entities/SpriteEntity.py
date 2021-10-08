from pygame.image import load
from pygame.surface import Surface
from Scripts.Common.CommonFuncs import *
from pygame.sprite import *


class SpriteEntity(object):

    SPRITE_SIZE = CELL_SIZE - 1

    def __init__(self, spriteGroup:Group,
                 startPosition:Tuple[int, int],
                 file:str):

        self.sprite = Sprite(spriteGroup)
        self.sprite.image = Surface((SpriteEntity.SPRITE_SIZE,
                                     SpriteEntity.SPRITE_SIZE))
        self.sprite.image = load(file)
        self.startPosition = startPosition
        self.rect = self.sprite.rect = self.sprite.image.get_rect()
        self.rect.center = self.startPosition

    def respawn(self, startPosition, startDirection):
        self.rect.center = startPosition
        self.currentDirection = startDirection    # refactor: add sprite to each direction
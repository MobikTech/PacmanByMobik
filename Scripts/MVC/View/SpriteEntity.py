from pygame.image import load
from pygame.surface import Surface
from pygame.sprite import *

from Scripts.MVC.Controller.Common.Constants import CELL_SIZE
from Scripts.MVC.Controller.Common.CommonClasses import CoordsConverter
from Scripts.MVC.Model.Navigation.Coords import Coords


class SpriteEntity(object):
    SPRITE_SIZE = CELL_SIZE

    def __init__(self, spriteType: int,
                 spriteGroup: Group,
                 coords: Coords,
                 file: str):
        self.spriteType = spriteType
        self.spriteGroup = spriteGroup
        self.sprite = Sprite(spriteGroup)
        self.sprite.image = Surface((SpriteEntity.SPRITE_SIZE,
                                     SpriteEntity.SPRITE_SIZE))
        self.sprite.image = load(file)
        self.rect = self.sprite.rect = self.sprite.image.get_rect()
        self.coordsWorld = CoordsConverter.gridToWorld(coords)
        self.rect.center = self.coordsWorld.getTuple()


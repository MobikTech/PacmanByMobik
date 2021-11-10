from pygame.sprite import Group
from Scripts.Old.Common.CommonFuncs import *
from Scripts.Old.Common.CoordsConverter import *
from Scripts.MVC.Model.Common.Constants import *
from Scripts.Old.Entities.CollidableEntity import CollidableEntity
from Scripts.Model.SpriteEntity import SpriteEntity
import random


class Ghost(CollidableEntity):
    GHOST_SPEED = 1

    def __init__(self, spriteGroup: Group,
                 startWorldPosition: Tuple[int, int],
                 spriteFile: str,
                 name: str,
                 colorMap: list[list[tuple[int, int, int, int]]],
                 pathColor: Tuple[int, int, int, int]):
        self.spriteEntity = SpriteEntity(SPRITE_TYPES.GHOST, spriteGroup, startWorldPosition, spriteFile)
        self.name = name
        self.colorMap = colorMap

        self.speed = Ghost.GHOST_SPEED
        self.startDirection = DIRECTIONS.UP
        self.currentDirection = self.startDirection

        self.pathColor = pathColor

    def moveGhost(self, newDirection):
        if inCellCenter(self.spriteEntity.sprite.rect.center, 1):
            ghostGridPosition = worldToGridT(self.spriteEntity.sprite.rect.center)
            if getCellType(self.colorMap, ghostGridPosition) == CELL_TYPE.CROSSROAD:
                self.spriteEntity.sprite.rect.center = gridToWorldT(ghostGridPosition)
                if newDirection != None:
                    self.currentDirection = newDirection
        moveSpriteEntity(self.spriteEntity, self.currentDirection, self.speed)
        # newDirection = self._tryRandomChangeDirection(self.colorMap, self.spriteEntity)
        # if newDirection != None:
        #     self.currentDirection = newDirection
        # moveSpriteEntity(self.spriteEntity, self.currentDirection, self.speed)

    def _tryRandomChangeDirection(self, colorMap: list[list[tuple[int, int, int, int]]], sprite: SpriteEntity):
        possibleDirections = getPossibleDirections(sprite, colorMap)

        if inCellCenter(sprite.rect.center, 1):
            playerGridPosition = worldToGridT(sprite.rect.center)
            if getCellType(colorMap, playerGridPosition) == CELL_TYPE.CROSSROAD:
                sprite.rect.center = gridToWorldT(playerGridPosition)
                return random.choice(possibleDirections)
        return None

    def collisionHandler(self, sprite: SpriteEntity):
        if sprite.spriteType == SPRITE_TYPES.PACMAN:
            pass
        elif sprite.spriteType == SPRITE_TYPES.COIN:
            pass

    def respawn(self):
        self.spriteEntity.sprite.rect.center = self.spriteEntity.startPosition
        self.currentDirection = self.startDirection


def getGhostName(type: int):
    if type == MOVABLE_ENTITIES.GHOST_RIKKO:
        return 'Rikko'
    elif type == MOVABLE_ENTITIES.GHOST_GREENKY:
        return 'Greenky'
    elif type == MOVABLE_ENTITIES.GHOST_PINKY:
        return 'Pinky'
    elif type == MOVABLE_ENTITIES.GHOST_CLYNE:
        return 'Clyne'
    return None

def getGhostColor(type: int):
    if type == MOVABLE_ENTITIES.GHOST_RIKKO:
        return COLORS.RED
    elif type == MOVABLE_ENTITIES.GHOST_GREENKY:
        return COLORS.GREEN
    elif type == MOVABLE_ENTITIES.GHOST_PINKY:
        return COLORS.PINK
    elif type == MOVABLE_ENTITIES.GHOST_CLYNE:
        return COLORS.YELLOW
    return None

def getGhostType(name: str):
    if name == 'Rikko':
        return MOVABLE_ENTITIES.GHOST_RIKKO
    elif name == 'Greenky':
        return MOVABLE_ENTITIES.GHOST_GREENKY
    elif name == 'Pinky':
        return MOVABLE_ENTITIES.GHOST_PINKY
    elif name == 'Clyne':
        return MOVABLE_ENTITIES.GHOST_CLYNE
    return None

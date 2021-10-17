from Scripts.Old.Common.CommonFuncs import *
from pygame.sprite import Group

from Scripts.Old.Entities.CollidableEntity import CollidableEntity
from Scripts.Model.SpriteEntity import SpriteEntity


class Player(CollidableEntity):
    PLAYER_SPEED = 1
    START_HP = 3
    GHOST_DAMAGE = 1
    COIN_SCORE_COST = 10

    def __init__(self,
                 spriteGroup: Group,
                 startWorldPosition: Tuple[int, int],
                 colorMap: list[list[tuple[int, int, int, int]]]):
        self.spriteEntity = SpriteEntity(SPRITE_TYPES.PACMAN, spriteGroup, startWorldPosition, MAIN_DIRECTORY + '\Sprites\Pacman.png')
        self.colorMap = colorMap
        self.speed = Player.PLAYER_SPEED
        # refactor: add sprite to each direction
        self.startDirection = DIRECTIONS.RIGHT
        self.currentDirection = self.startDirection

        self.score = 0
        self.hp = Player.START_HP
        self.lastVisitedCrossroad = None

    def tryMovePlayer(self, newDirection):
        # newDirection = self._tryChangeDirection(self.colorMap, self.spriteEntity, self.currentDirection)

        # if inCellCenter(self.spriteEntity.sprite.rect.center, 1):
        #     playerGridPosition = worldToGridT(self.spriteEntity.sprite.rect.center)
        #     if getCellType(self.colorMap, playerGridPosition) == CELL_TYPE.MAP_CROSSROAD:
        #         if newDirection != None and self.currentDirection != newDirection:
        #             self.spriteEntity.sprite.rect.center = gridToWorldT(playerGridPosition)
        #             self.currentDirection = newDirection
        # moveSpriteEntity(self.spriteEntity, self.currentDirection, self.speed)

        if newDirection != None and self.currentDirection != newDirection:
            self.currentDirection = newDirection
        if self._canMove(self.spriteEntity, self.currentDirection, self.colorMap):
            moveSpriteEntity(self.spriteEntity, self.currentDirection, self.speed)

    def _tryChangeDirection(self, colorMap: list[list[tuple[int, int, int, int]]], sprite: SpriteEntity,
                            currentDirection: int):
        pressedKeys = pygame.key.get_pressed()
        direction = defineDirection(pressedKeys)
        if direction in (None, currentDirection):
            return None
        if direction == getOppositeDirection(currentDirection):
            return direction
        if inCellCenter(sprite.rect.center, 2):
            playerGridPosition = worldToGridT(sprite.rect.center)
            if getCellType(colorMap, playerGridPosition) == CELL_TYPE.MAP_CROSSROAD:
                # aligning in cell center
                sprite.rect.center = gridToWorldT(playerGridPosition)
                return direction
        return None

    def _canMove(self, sprite: SpriteEntity, currentDirection: int, colorMap: list[list[tuple[int, int, int, int]]]):
        nextCellPosition = worldToGridT(getOffsettedPoint(sprite.rect.center, currentDirection, CELL_HALF_SIZE + 1))
        nextCellType = getCellType(colorMap, nextCellPosition)
        if nextCellType in (CELL_TYPE.MAP_ROAD, CELL_TYPE.MAP_CROSSROAD, CELL_TYPE.MAP_PACMAN_START_POSITION):
            return True
        return False

    def collisionHandler(self, sprite: SpriteEntity):
        if sprite.spriteType == SPRITE_TYPES.GHOST:
            self.hp -= Player.GHOST_DAMAGE
        if sprite.spriteType == SPRITE_TYPES.COIN:
            self.score += Player.COIN_SCORE_COST

    def respawn(self):
        self.spriteEntity.sprite.rect.center = self.spriteEntity.startPosition
        self.currentDirection = self.startDirection
        self.lastVisitedCrossroad = None

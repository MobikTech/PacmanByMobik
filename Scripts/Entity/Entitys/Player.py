from CommonFuncs import *
from Scripts.Entity.Entity import Entity

class Player(Entity):
    def __init__(self, group:pygame.sprite.Group , startPosition:Tuple[int, int], gmController):
        Entity.__init__(self, group, startPosition, '../../../Sprites/Pacman.png')
        self.speed = 2
        self.startDirection = pygame.K_d
        self.currentDirection = self.startDirection
        self.score = 0
        self.hp = 5
        self.gmController = gmController



    def collideGhost(self):
        self.hp -= 1
        if self.hp < 1:
            print('game over')
            self.gmController.gameOver = True

    def _collectCoins(self):
        gridX, gridY = worldToGridT(self.rect.center)
        if self.gmController.coinsMap[gridX][gridY] != None:
            self.gmController.coinsMap[gridX][gridY].sprite.remove(self.gmController.sprites_group)
            self.gmController.coinsMap[gridX][gridY] = None
            self.gmController.coinAmount -= 1
            self.score += 10
            # print(self.gmController.coinAmount)
        if self.gmController.coinAmount < 1:
            self.gmController.gameOver = True
            print("end level")

    def _move(self, pressedKey: int):
        if pressedKey == pygame.K_w:
            self.rect.y -= self.speed
        elif pressedKey == pygame.K_s:
            self.rect.y += self.speed
        elif pressedKey == pygame.K_d:
            self.rect.x += self.speed
        elif pressedKey == pygame.K_a:
            self.rect.x -= self.speed
        self._collectCoins()

    def _isValidDirection(self, pressedKey:int):
        playerCenterW = self.rect.center
        playerGridCell = worldToGridT(playerCenterW)
        map = self.gmController.map

        if pressedKey == self.currentDirection:
            return False
        if pressedKey == pygame.K_w:
            if self.currentDirection == pygame.K_s:
                return True
            # Если центр спрайта игрока попадает в центр любой клетки на сетке,он проверяет возможность двигаться по направлению(если следущая клетка - дорога)
            if inSomeRect(playerCenterW, gridToWorldT(playerGridCell), CELL_RECT_SIDE) and \
                    map.colorMap[playerGridCell[0]][playerGridCell[1]] == MAP_CROSSROAD:
                self.rect.center = gridToWorldT(playerGridCell)
                return True
        elif pressedKey == pygame.K_s:
            if self.currentDirection == pygame.K_w:
                return True
            if inSomeRect(playerCenterW, gridToWorldT(playerGridCell), CELL_RECT_SIDE) and \
                    map.colorMap[playerGridCell[0]][playerGridCell[1]] == MAP_CROSSROAD:
                self.rect.center = gridToWorldT(playerGridCell)
                return True
        elif pressedKey == pygame.K_d:
            if self.currentDirection == pygame.K_a:
                return True
            if inSomeRect(playerCenterW, gridToWorldT(playerGridCell), CELL_RECT_SIDE) and \
                    map.colorMap[playerGridCell[0]][playerGridCell[1]] == MAP_CROSSROAD:
                self.rect.center = gridToWorldT(playerGridCell)
                return True
        elif pressedKey == pygame.K_a:
            if self.currentDirection == pygame.K_d:
                return True
            if inSomeRect(playerCenterW, gridToWorldT(playerGridCell), CELL_RECT_SIDE) and \
                    map.colorMap[playerGridCell[0]][playerGridCell[1]] == MAP_CROSSROAD:
                self.rect.center = gridToWorldT(playerGridCell)
                return True
        return False

    def movePlayer(self):
        pressedKeys = pygame.key.get_pressed()

        if pressedKeys[pygame.K_w] and self._isValidDirection(pygame.K_w):
            self.currentDirection = pygame.K_w
        if pressedKeys[pygame.K_s] and self._isValidDirection(pygame.K_s):
            self.currentDirection = pygame.K_s
        if pressedKeys[pygame.K_d] and self._isValidDirection(pygame.K_d):
            self.currentDirection = pygame.K_d
        if pressedKeys[pygame.K_a] and self._isValidDirection(pygame.K_a):
            self.currentDirection = pygame.K_a

        if self._canMove(self.currentDirection):
            self._move(self.currentDirection)

    def _canMove(self, currentDirection:int):
        map = self.gmController.map
        tlX, tlY = worldToGridT(self.rect.topleft)
        brX, brY = worldToGridT(self.rect.bottomright)

        if currentDirection == pygame.K_w:
            if map.colorMap[brX][brY - 1] not in (MAP_WALL, MAP_SPIRIT_DOOR):
                return True
        elif currentDirection == pygame.K_s:
            if map.colorMap[tlX][tlY + 1] not in (MAP_WALL, MAP_SPIRIT_DOOR):
                return True
        elif currentDirection == pygame.K_d:
            if map.colorMap[tlX + 1][tlY] not in (MAP_WALL, MAP_SPIRIT_DOOR):
                return True
        elif currentDirection == pygame.K_a:
            if map.colorMap[brX - 1][brY] not in (MAP_WALL, MAP_SPIRIT_DOOR):
                return True
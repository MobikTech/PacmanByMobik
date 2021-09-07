import pygame
from Constants import *
from Player import *
from Map import *
from CommonFuncs import *
from Ghost import Ghost
from Text import TextObject
from Coin import Coin
import random

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.gameOver = False
        # self.background = pygame.surface.Surface(SCREEN_SIZE).convert()
        self.clock = pygame.time.Clock()
        self.map_1 = Map(pygame.image.load('Sprites/pacman_map_1_31x31.png'), pygame.image.load('Sprites/pacman_map_1_651x651.png'))
        # self.map_1 = Map(pygame.image.load('Sprites/pacman_map_2_31x31.png'), pygame.image.load('Sprites/pacman_map_2_651x651.png'))
        # self.map_1 = Map(pygame.image.load('Sprites/pacman_map_1_31x31.png'), pygame.image.load('Sprites/pacman_map_1_651x651.png'))
        self.sprites_group = pygame.sprite.Group()

        self.enteties = list()
        self.ghostStartPosition = CENTER
        self.coinsMap = [[None for x in range(NCOLUMNS)] for y in range(NROWS)]
        self.coinAmount = 0

        self.player = Player(self.sprites_group, (CENTER[0] , CENTER[1] - 9 * CELL_SIZE), self)
        self.G_rikky = Ghost("Rikky", "Sprites/Rikky.png", self.sprites_group, self.ghostStartPosition, self.map_1)
        self.G_greenky = Ghost("Greenky", "Sprites/Greenky.png", self.sprites_group, self.ghostStartPosition, self.map_1)
        self.G_pinky = Ghost("Pinky", "Sprites/Pinky.png", self.sprites_group, self.ghostStartPosition, self.map_1)
        self.G_clyde = Ghost("Clyde", "Sprites/Clyne.png", self.sprites_group, self.ghostStartPosition, self.map_1)

        self.scoreText = TextObject('Fonts/Pinmolddemo-jEaxv.otf', 32, WHITE, (CENTER[0], CENTER[1] + CELL_SIZE * 2), "score: " + str(self.player.score))
        self.hpText = TextObject('Fonts/Pinmolddemo-jEaxv.otf', 32, WHITE, (CENTER[0] - CELL_SIZE * 11, CENTER[1] + CELL_SIZE * 2), "hp: " + str(self.player.hp))
        self.gameOverText = TextObject('Fonts/Pinmolddemo-jEaxv.otf', 56, WHITE, (CENTER[0], CENTER[1] + CELL_SIZE * 5), "game over")




    def start(self):
        self.mapScan()
        self.screen.fill(BLACK)
        self.enteties.append(self.player)
        self.enteties.append(self.G_rikky)
        self.enteties.append(self.G_greenky)
        self.enteties.append(self.G_pinky)
        self.enteties.append(self.G_clyde)

    def respawnAll(self):
        for entity in self.enteties:
            entity.respawn()
        self.render()
        # pygame.time.delay(1000)

    def mapScan(self):
        map = self.map_1.colorMap
        for x in range(NCOLUMNS):
            for y in range(NROWS):
                if map[x][y] == MAP_PACMAN_START_POSITION:
                    self.player.startPosition = gridToWorld(x, y)
                elif map[x][y] == MAP_GHOSTS_START_POSITION:
                    self.ghostStartPosition = gridToWorld(x, y)
                elif map[x][y] == MAP_ROAD or map[x][y] == MAP_CROSSROAD:
                    self.coinsMap[x][y] = Coin(self.sprites_group, gridToWorld(x, y))
                    self.coinAmount += 1


    def update(self):
        self.clock.tick(FPS)
        self.eventHandler()
        if self.gameOver == False:
            self.movePlayer()
            self.ghostMove()
            self.render()
        else:
            self.endGame()


    def endGame(self):
        self.clearScreen()
        self.gameOverText.textUpdate('game over', self.screen)
        self.scoreText.textUpdate('score: ' + str(self.player.score), self.screen)

    def clearScreen(self):
        self.screen.blit(self.map_1.background, self.map_1.background.get_rect())



    def eventHandler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

    def render(self):
        self.clearScreen()

        self.sprites_group.update()
        self.sprites_group.draw(self.screen)
        self.scoreText.textUpdate('score: ' + str(self.player.score), self.screen)
        self.hpText.textUpdate('hp: ' + str(self.player.hp), self.screen)



    def ghostMove(self):
        self.G_rikky.move()
        self.G_pinky.move()
        self.G_greenky.move()
        self.G_clyde.move()

        checkCollision(self.player, self.G_rikky)
        checkCollision(self.player, self.G_pinky)
        checkCollision(self.player, self.G_greenky)
        checkCollision(self.player, self.G_clyde)




    def isValidDirection(self, pressedKey:int):
        playerCenterW = self.player.rect.center
        playerGridCell = worldToGridT(playerCenterW)

        if pressedKey == self.player.currentDirection:
            return False
        if pressedKey == pygame.K_w:
            if self.player.currentDirection == pygame.K_s:
                return True
            # Если центр спрайта игрока попадает в центр любой клетки на сетке,он проверяет возможность двигаться по направлению(если следущая клетка - дорога)
            if inSomeRect(playerCenterW, gridToWorldT(playerGridCell), CELL_RECT_SIDE) and \
                    self.map_1.colorMap[playerGridCell[0]][playerGridCell[1]] == MAP_CROSSROAD:
                self.player.rect.center = gridToWorldT(playerGridCell)
                return True
        elif pressedKey == pygame.K_s:
            if self.player.currentDirection == pygame.K_w:
                return True
            if inSomeRect(playerCenterW, gridToWorldT(playerGridCell), CELL_RECT_SIDE) and \
                    self.map_1.colorMap[playerGridCell[0]][playerGridCell[1]] == MAP_CROSSROAD:
                self.player.rect.center = gridToWorldT(playerGridCell)
                return True

        elif pressedKey == pygame.K_d:
            if self.player.currentDirection == pygame.K_a:
                return True
            if inSomeRect(playerCenterW, gridToWorldT(playerGridCell), CELL_RECT_SIDE) and \
                    self.map_1.colorMap[playerGridCell[0]][playerGridCell[1]] == MAP_CROSSROAD:
                self.player.rect.center = gridToWorldT(playerGridCell)
                return True
        elif pressedKey == pygame.K_a:
            if self.player.currentDirection == pygame.K_d:
                return True
            if inSomeRect(playerCenterW, gridToWorldT(playerGridCell), CELL_RECT_SIDE) and \
                    self.map_1.colorMap[playerGridCell[0]][playerGridCell[1]] == MAP_CROSSROAD:
                self.player.rect.center = gridToWorldT(playerGridCell)
                return True
        return False

    def movePlayer(self):
        pressedKeys = pygame.key.get_pressed()

        if pressedKeys[pygame.K_w] and self.isValidDirection(pygame.K_w):
            self.player.currentDirection = pygame.K_w
        if pressedKeys[pygame.K_s] and self.isValidDirection(pygame.K_s):
            self.player.currentDirection = pygame.K_s
        if pressedKeys[pygame.K_d] and self.isValidDirection(pygame.K_d):
            self.player.currentDirection = pygame.K_d
        if pressedKeys[pygame.K_a] and self.isValidDirection(pygame.K_a):
            self.player.currentDirection = pygame.K_a

        # self.xPosition = self.player.sprite.rect.x
        # self.yPosition = self.player.sprite.rect.y

        if self.canMove(self.player.currentDirection):
            self.player.move(self.player.currentDirection)

    def canMove(self, currentDirection:int):
        tlX, tlY = worldToGridT(self.player.rect.topleft)
        # trX, trY = worldToGridT(self.playerRect.topright)
        # blX, blY = worldToGridT(self.playerRect.bottomleft)
        brX, brY = worldToGridT(self.player.rect.bottomright)

        if currentDirection == pygame.K_w:
            if self.map_1.colorMap[brX][brY - 1] not in (MAP_WALL, MAP_SPIRIT_DOOR):
                return True
        elif currentDirection == pygame.K_s:
            if self.map_1.colorMap[tlX][tlY + 1] not in (MAP_WALL, MAP_SPIRIT_DOOR):
                return True
        elif currentDirection == pygame.K_d:
            if self.map_1.colorMap[tlX + 1][tlY] not in (MAP_WALL, MAP_SPIRIT_DOOR):
                return True
        elif currentDirection == pygame.K_a:
            if self.map_1.colorMap[brX - 1][brY] not in (MAP_WALL, MAP_SPIRIT_DOOR):
                return True



gameController = GameController()
gameController.start()
while True:
    gameController.update()
    pygame.display.flip()

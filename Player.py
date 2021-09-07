import pygame
from Constants import *
from CommonFuncs import *
from typing import Tuple
from Entity import Entity

class Player(Entity):
    def __init__(self, group:pygame.sprite.Group , startPosition:Tuple[int, int], gmController):
        Entity.__init__(self, group, startPosition, 'Sprites/Pacman.png')
        self.speed = 2
        self.currentDirection = pygame.K_d
        self.score = 0
        self.hp = 3
        self.gmController = gmController


    def move(self, pressedKey: int):
        if pressedKey == pygame.K_w:
            self.rect.y -= self.speed
        elif pressedKey == pygame.K_s:
            self.rect.y += self.speed
        elif pressedKey == pygame.K_d:
            self.rect.x += self.speed
        elif pressedKey == pygame.K_a:
            self.rect.x -= self.speed
        self.collectCoins()

    def collideGhost(self):
        self.hp -= 1
        self.respawn()
        self.gmController.respawnAll()

        if self.hp < 1:
            print('game over')
            self.gmController.gameOver = True

    def respawn(self):
        self.rect.center = self.startPosition
        self.currentDirection = pygame.K_d

    def collectCoins(self):
        gridX, gridY = worldToGridT(self.rect.center)
        if self.gmController.coinsMap[gridX][gridY] != None:
            self.gmController.coinsMap[gridX][gridY].sprite.remove(self.gmController.sprites_group)
            self.gmController.coinsMap[gridX][gridY] = None
            self.gmController.coinAmount -= 1
            self.score += 10
            print(self.gmController.coinAmount)
        if self.gmController.coinAmount < 1:
            self.gmController.gameOver = True
            print("end level")



    # def update(self):
    #     self.sprite.update()

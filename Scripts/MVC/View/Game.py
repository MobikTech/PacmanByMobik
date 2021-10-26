import pygame
from Scripts.MVC.Controller.Common.Constants import *
from Scripts.MVC.Controller.GameLoop import GameLoop
from Scripts.MVC.Model.Navigation.Coords import Coords
from Scripts.MVC.View.PathDrawer import PathDrawer
from Scripts.MVC.View.SpritesContatiner import SpritesContainer
from Scripts.MVC.View.UIContatiner import UIContainer


class GameController(object):


    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN.SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.gameLooper = GameLoop()
        self.layer1 = self.gameLooper.info.background

        self.spritesContainer = SpritesContainer(self.gameLooper)
        self.uiContainer = UIContainer()


    def start(self):
        self.gameLooper.start()
        self.gameLooper.events.playerPathCalculated = self.__drawPath
        self.gameLooper.events.ghostsPathCalculated = self.__drawPath
        # self.gameLooper.events.coinCollected = self.__deleteSpriteCoin

    def update(self):
        if self.gameLooper.info.hp < 1:
            self.__endGame()
        else:
            self.clock.tick(FPS)
            self.__eventHandler()
            self.__render()

    def __render(self):
        self.__clearScreen()
        self.uiContainer.update(self.gameLooper.info.hp, self.gameLooper.info.score, self.layer1)
        self.gameLooper.update()
        self.spritesContainer.updateSpritesPositions()
        self.spritesContainer.spritesGroup.draw(self.layer1)
        self.screen.blit(self.layer1, SCREEN.SCREEN_START_POINT)

    def __eventHandler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

    def __endGame(self):
        self.__clearScreen()
        self.uiContainer.endGameUpdate(self.gameLooper.info.score, self.layer1)
        self.screen.blit(self.layer1, SCREEN.SCREEN_START_POINT)

    def __clearScreen(self):
        self.layer1 = self.gameLooper.info.background.copy()


    def __drawPath(self, path, startPoint, targetPoint, color):
        PathDrawer.drawPath(path,
                            startPoint,
                            targetPoint,
                            self.gameLooper.info.map.grid,
                            color,
                            self.layer1)

    def __deleteSpriteCoin(self, coords: Coords):
        self.spritesContainer.spritesGroup.remove(self.spritesContainer.coinsSprites[coords.getTuple()].sprite)
        self.spritesContainer.coinsSprites.pop(coords.getTuple())

gameController = GameController()
gameController.start()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.QUIT:
            running = False
    gameController.update()
    pygame.display.flip()

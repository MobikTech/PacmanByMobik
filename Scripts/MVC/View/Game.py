import pygame
from Scripts.MVC.Controller.Common.Constants import *
from Scripts.MVC.Controller.GameLoop import GameLoop
from Scripts.MVC.View.PathDrawer import PathDrawer
from Scripts.MVC.View.SpriteEntity import SpriteEntity
from Scripts.MVC.View.SpritesContatiner import SpritesContainer


class GameController(object):


    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN.SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.gameOver = False
        self.gameLooper = GameLoop()
        self.layer1 = self.gameLooper.info.background

        self.spritesContainer = SpritesContainer(self.gameLooper)

    def start(self):
        self.gameLooper.start()
        self.gameLooper.events.playerPathCalculated = self.__drawPath
        self.gameLooper.events.ghostsPathCalculated = self.__drawPath

    def update(self):
        if self.gameOver == True:
            self.__endGame()
        else:
            self.clock.tick(FPS)
            self.__eventHandler()
            self.__render()

    def __render(self):
        self.__clearScreen()
        self.spritesContainer.updateSpritesPositions()
        self.spritesContainer.spritesGroup.draw(self.layer1)
        self.gameLooper.update()
        self.screen.blit(self.layer1, SCREEN.SCREEN_START_POINT)

    def __eventHandler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

    def __endGame(self):
        self.__clearScreen()
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

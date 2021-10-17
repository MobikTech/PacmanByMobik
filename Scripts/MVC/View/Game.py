import pygame
from Scripts.MVC.View.Constants import *


class GameController(object):


    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.gameOver = False



    def start(self):
        pass

    def update(self):
        if self.gameOver == True:
            self._endGame()
        else:
            self.clock.tick(FPS)
            self._eventHandler()
            self.render()

    def render(self):
        # self._clearScreen()
        self.screen.blit(self.layer1, SCREEN_START_POINT)

    def _eventHandler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
    #
    # def _clearScreen(self):
    #     self.layer1 = self.currentMap.background.copy()

    def _endGame(self):
        self._clearScreen()
        self.screen.blit(self.layer1, SCREEN_START_POINT)


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

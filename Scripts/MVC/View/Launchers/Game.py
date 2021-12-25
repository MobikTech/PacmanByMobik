import pygame

from Scripts.MVC.Controller.Common.Constants import *
from Scripts.MVC.Controller.GameLoop import GameLoop, GameInfo
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
        self.start()

    def play_step(self, actions):
        if sum(actions) != 1:
            raise NotImplementedError
        direction = None
        if actions[0] == 1:
            direction = DIRECTIONS.UP
        elif actions[1] == 1:
            direction = DIRECTIONS.RIGHT
        elif actions[2] == 1:
            direction = DIRECTIONS.DOWN
        elif actions[3] == 1:
            direction = DIRECTIONS.LEFT

        score_old = self.gameLooper.info.score
        hp_old = self.gameLooper.info.hp
        self.update(direction)

        reward = 0
        if self.gameLooper.info.score > score_old:
            reward += 1
        if self.gameLooper.info.hp < hp_old:
            reward -= 1

        game_over = False
        if self.gameLooper.info.hp < 1:
            game_over = True

        return reward, game_over, self.gameLooper.info.score


    def reset(self):
        self.__init__()

    def get_screen_image(self):
        return pygame.surfarray.array3d(pygame.display.get_surface())


    def start(self):
        self.gameLooper.start()
        self.gameLooper.events.playerPathCalculated = self.__drawPath
        # self.gameLooper.events.ghostsPathCalculated = self.__drawPath
        self.gameLooper.events.newGhostAdded = self.__initNewGhost
        # to hide coins
        self.gameLooper.events.coinCollected = self.__deleteSpriteCoin

    def update(self, playerDirection=None):
        if self.gameLooper.info.hp < 1:
            self.__endGame()
        else:
            self.clock.tick(FPS)
            self.__eventHandler()
            self.__render(playerDirection)
            ##
            # print(self.get_screen_image().shape)
            # print(self.get_screen_image()[0][0])

    def __render(self, playerDirection):
        self.__clearScreen()
        self.uiContainer.update(self.gameLooper.info.hp, self.gameLooper.info.score, self.layer1)
        self.gameLooper.update(playerDirection)
        self.spritesContainer.updateSpritesPositions()
        self.spritesContainer.spritesGroup.draw(self.layer1)
        self.screen.blit(self.layer1, SCREEN.SCREEN_START_POINT)
        pygame.display.flip()

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

    def __initNewGhost(self, ghost):
        self.spritesContainer.initGhost(ghost)



#region GameLauncher

# gameController = GameController()
# print('game')
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_ESCAPE:
#                 running = False
#         elif event.type == pygame.QUIT:
#             running = False
#     gameController.update()
#     pygame.display.flip()

#endregion



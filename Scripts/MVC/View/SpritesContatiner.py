from pygame.sprite import Group
from Scripts.MVC.Controller.GameLoop import GameLoop
from Scripts.MVC.View.SpriteEntity import SpriteEntity

from Scripts.MVC.Controller.Common.Constants import *


class SpritesContainer():
    def __init__(self, gameLooper: GameLoop):
        self.gameLooper = gameLooper
        self.spritesGroup = Group()
        self.playerSprite = SpriteEntity(SPRITE_TYPES.PACMAN,
                                         self.spritesGroup,
                                         gameLooper.info.player.startCoords,
                                         MAIN_DIRECTORY + '\Sprites\Pacman.png')
        self.ghostsSprites = dict()
        self.__initGhosts()
        self.coinsSprites = dict()
        # self.__initCoins()

    def __initGhosts(self):
        for ghost in self.gameLooper.info.ghosts:
            self.ghostsSprites[ghost] = SpriteEntity(SPRITE_TYPES.GHOST,
                                                     self.spritesGroup,
                                                     ghost.coords,
                                                     SpritesContainer.getGhostSpritiePath(ghost.ghostType))

    def __initCoins(self):
        for coin in self.gameLooper.info.coinsContainer.coinsDict.values():
            self.coinsSprites[coin.coords.getTuple()] = SpriteEntity(SPRITE_TYPES.COIN,
                                                                     self.spritesGroup,
                                                                     coin.coords,
                                                                     MAIN_DIRECTORY + '\Sprites\PacmanCoin.png')

    def updateSpritesPositions(self):
        self.playerSprite.rect.center = self.gameLooper.info.player.coordsWorld.getTuple()
        for ghost in self.ghostsSprites.keys():
            self.ghostsSprites[ghost].rect.center = ghost.coordsWorld.getTuple()

    @staticmethod
    def getGhostSpritiePath(type: int):
        if type == GHOST_TYPE.RIKKO:
            return MAIN_DIRECTORY + '\Sprites\Rikko.png'
        elif type == GHOST_TYPE.PINKY:
            return MAIN_DIRECTORY + '\Sprites\Pinky.png'
        elif type == GHOST_TYPE.GREENKY:
            return MAIN_DIRECTORY + '\Sprites\Greenky.png'
        elif type == GHOST_TYPE.CLYNE:
            return MAIN_DIRECTORY + '\Sprites\Clyne.png'

import pygame
from Constants import *

# Map-making inctructions:
# yellow (255, 255, 0, 255) - pacman start point
# pink (255, 0, 255, 255) - ghosts spawn point
# black (0, 0, 0, 255) - roads
# green (0, 255, 0, 255) - crossroads
# blue (0, 0, 255, 255) - walls
# white (255, 255, 255, 255) - non-active space(for example, for UI)
# red (255, 0, 0, 255) - door for spirit house

class Map(object):
    def __init__(self, image:pygame.Surface, background:pygame.Surface):
        self.mapImage = image
        self.background = background
        self.colorMap = self.getColorMap(image)
        # self.coinMap = self.spawnCoins()
        self.background.get_rect().center = CENTER


    def getColorMap(self, image:pygame.Surface):
        map1 = pygame.pixelarray.PixelArray(image)
        x, y = map1.shape
        colorMap = [[0 for x in range(x)] for y in range(y)]
        for i in range(x):
            for k in range(y):
                colorMap[i][k] = image.unmap_rgb(map1[i][k])
        return colorMap

    # def spawnCoins(self, image: pygame.Surface):
    #     map1 = pygame.pixelarray.PixelArray(image)
    #     x, y = map1.shape
    #     spawnCoins = [[None for x in range(x)] for y in range(y)]
    #     for i in range(x):
    #         for k in range(y):
    #             colorMap[i][k] = image.unmap_rgb(map1[i][k])

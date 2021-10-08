import pygame
from typing import Tuple

class TextObject(object):
    def __init__(self, fontFile: str, fontSize: int, fontColor: tuple, position: Tuple[int, int], text: str):
        self.fontColor = fontColor
        self.position = position
        self.font = pygame.font.Font(fontFile, fontSize)
        self.textSurface = self.font.render(text, True, self.fontColor)
        self.rect = self.textSurface.get_rect()
        self.rect.center = self.position

    def textUpdate(self, newText: str, surface):
        self.textSurface = self.font.render(newText, True, self.fontColor)
        self.rect = self.textSurface.get_rect()
        self.rect.center = self.position

        surface.blit(self.textSurface, self.rect)



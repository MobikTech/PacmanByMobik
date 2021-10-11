from typing import Tuple
from pygame.font import Font

from Scripts.Common.Constants import *


class TextObject(object):
    FONT_PATH = 'D:\Projects\PYTHON\PacmanByMobik\Fonts\Pinmolddemo-jEaxv.otf'
    FONT_COLOR = COLORS.WHITE
    def __init__(self, fontSize: int, worldPosition: Tuple[int, int], text: str):
        self.fontColor = TextObject.FONT_COLOR
        self.position = worldPosition
        self.font = Font(TextObject.FONT_PATH, fontSize)
        self.textSurface = self.font.render(text, True, self.fontColor)
        self.rect = self.textSurface.get_rect()
        self.rect.center = self.position

    def textUpdate(self, newText: str, surface):
        self.textSurface = self.font.render(newText, True, self.fontColor)
        self.rect = self.textSurface.get_rect()
        self.rect.center = self.position

        surface.blit(self.textSurface, self.rect)

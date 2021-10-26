from pygame.font import Font
from Scripts.MVC.Controller.Common.Constants import COLORS, MAIN_DIRECTORY
from Scripts.MVC.Model.Navigation.Coords import Coords


class TextObject(object):
    FONT_PATH = '/Fonts/Pinmolddemo-jEaxv.otf'
    FONT_COLOR = COLORS.WHITE
    def __init__(self, fontSize: int, coordsWorld: Coords, text: str):
        self.fontColor = TextObject.FONT_COLOR
        self.coords = coordsWorld
        self.font = Font(MAIN_DIRECTORY + TextObject.FONT_PATH, fontSize)
        self.textSurface = self.font.render(text, True, self.fontColor)
        self.rect = self.textSurface.get_rect()
        self.rect.center = coordsWorld.getTuple()

    def textUpdate(self, newText: str, surface):
        self.textSurface = self.font.render(newText, True, self.fontColor)
        self.rect = self.textSurface.get_rect()
        self.rect.center = self.coords.getTuple()

        surface.blit(self.textSurface, self.rect)
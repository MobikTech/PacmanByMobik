from Scripts.MVC.Controller.Common.Constants import *
from Scripts.MVC.Model.Navigation.Coords import Coords
from Scripts.MVC.View.TextObject import TextObject


class UIContainer():

    HP_MARKER_POSITION = Coords((SCREEN.SCREEN_CENTER[0] - CELL_SIZE * 11, SCREEN.SCREEN_CENTER[1] + CELL_SIZE * 4))
    SCORE_MARKER_POSITION = Coords((SCREEN.SCREEN_CENTER[0], SCREEN.SCREEN_CENTER[1] + CELL_SIZE * 4))
    GAME_OVER_MARKER_POSITION = Coords((SCREEN.SCREEN_CENTER[0], SCREEN.SCREEN_CENTER[1] + CELL_SIZE * 7))

    def __init__(self):
        self.hp = TextObject(32, UIContainer.HP_MARKER_POSITION, "hp: " + str(0))
        self.score = TextObject(32, UIContainer.SCORE_MARKER_POSITION, "score: " + str(0))
        self.gameOver = TextObject(56, UIContainer.GAME_OVER_MARKER_POSITION, 'Game Over')


    def update(self, hp: int, score: int, surface):
        self.hp.textUpdate('hp: ' + str(hp), surface)
        self.score.textUpdate('score: ' + str(score), surface)

    def endGameUpdate(self, score: int, surface):
        self.gameOver.textUpdate('game over', surface)
        self.score.textUpdate('score: ' + str(score), surface)
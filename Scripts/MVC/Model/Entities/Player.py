from Scripts.MVC.Model.Navigation.Coords import Coords
from Scripts.MVC.Controller.Common.CommonClasses import CoordsConverter


class Player(object):
    SPEED = 1

    def __init__(self,
                 startCoords: Coords,
                 startDirection: str):
        self.startCoords = startCoords
        self.startDirection = startDirection

        self.coords = startCoords.__copy__()
        self.coordsWorld = CoordsConverter.gridToWorld(self.coords)

        self.direction = startDirection

    def move(self):
        self.coordsWorld.offsetTo(self.direction, Player.SPEED)
        self.coords = CoordsConverter.worldToGrid(self.coordsWorld)

    def respawn(self):
        self.coords = self.startCoords.__copy__()
        self.coordsWorld = CoordsConverter.gridToWorld(self.coords)
        self.direction = self.startDirection

    # todo auto game handler
    def moveGrid(self):
        self.coords.offsetTo(self.direction, 1)

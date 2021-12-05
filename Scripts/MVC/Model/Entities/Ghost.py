from Scripts.MVC.Controller.Common.CommonClasses import CoordsConverter
from Scripts.MVC.Model.Navigation.Coords import Coords


class Ghost(object):
    SPEED = 25

    def __init__(self,
                 startCoords: Coords,
                 startDirection: str,
                 type: int):
        self.startCoords = startCoords
        self.startDirection = startDirection

        self.coords = startCoords.__copy__()
        self.coordsWorld = CoordsConverter.gridToWorld(self.coords)

        self.direction = startDirection
        self.ghostType = type

    def move(self):
        self.coordsWorld.offsetTo(self.direction, Ghost.SPEED)
        self.coords = CoordsConverter.worldToGrid(self.coordsWorld)

    def respawn(self):
        self.coords = self.startCoords.__copy__()
        self.coordsWorld = CoordsConverter.gridToWorld(self.coords)
        self.direction = self.startDirection
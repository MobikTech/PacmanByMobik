from Scripts.MVC.Controller.Common.CommonClasses import CoordsConverter
from Scripts.MVC.Model.Navigation.Coords import Coords


class Ghost(object):
    SPEED = 1

    def __init__(self,
                 startPosition: Coords,
                 startDirection: str,
                 type: int):
        self.startCoords = startPosition
        self.startDirection = startDirection

        self.coords = startPosition.__copy__()
        self.coordsWorld = CoordsConverter.gridToWorld(self.coords)
        self.direction = startDirection
        self.ghostType = type

    def move(self):
        self.coordsWorld.offsetTo(self.direction, Ghost.SPEED)
        self.coords = CoordsConverter.worldToGrid(self.coordsWorld)
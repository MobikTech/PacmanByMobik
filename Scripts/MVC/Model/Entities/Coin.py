from Scripts.MVC.Model.Navigation.Coords import Coords
from Scripts.MVC.Controller.Common.CommonClasses import CoordsConverter



class Coin(object):
    def __init__(self, startPos: tuple[int, int]):
        self.coords = Coords(startPos)
        self.coordsWorld = CoordsConverter.gridToWorld(self.coords)


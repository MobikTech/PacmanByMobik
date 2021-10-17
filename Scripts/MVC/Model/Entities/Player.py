from Scripts.MVC.Model.Navigation.Coords import Coords


class Player(object):
    SPEED = 1

    def __init__(self,
                 startPosition: Coords,
                 startDirection: str):
        self.__startCoords = startPosition
        self.__startDirection = startDirection

        self.coords = Coords()
        self.direction = startDirection

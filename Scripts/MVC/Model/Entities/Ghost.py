from Scripts.MVC.Model.Navigation.Coords import Coords


class Ghost(object):

    def __init__(self,
                 startPosition: Coords,
                 startDirection: str):
        self.__startCoords = startPosition
        self.__startDirection = startDirection

        self.coords = Coords()
        self.direction = startDirection

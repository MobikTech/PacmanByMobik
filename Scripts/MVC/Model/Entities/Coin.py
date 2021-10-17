from Scripts.MVC.Model.Navigation.Coords import Coords


class Coin(object):
    def __init__(self, startPos: tuple[int, int]):
        self.coords = Coords(startPos)

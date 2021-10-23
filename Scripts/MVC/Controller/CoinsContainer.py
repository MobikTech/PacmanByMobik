from Scripts.MVC.Model.Entities.Coin import Coin
from Scripts.MVC.Model.Navigation.Coords import Coords
from Scripts.MVC.Model.Navigation.Map import Map


class CoinsContainer():
    def __init__(self, map: Map):
        self.coinsDict: dict[tuple[int, int]] = dict()
        self.__spawnCoins(map)

    def __spawnCoins(self, map):
        coinsPositionsList = map.roadsPositionsList + list(map.nodesDictionary.keys())
        for position in coinsPositionsList:
            self.coinsDict[position] = Coin(position)

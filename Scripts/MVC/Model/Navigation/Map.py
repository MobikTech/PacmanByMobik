from Scripts.MVC.Model.Navigation.Coords import Coords
from Scripts.MVC.Model.Navigation.Nodes import Node


class Map():
    def __init__(self,
                 grid: dict[tuple[int, int]],
                 playerStartPos: tuple[int, int],
                 ghostsStartPos: tuple[int, int],
                 playerStartDir: str,
                 ghostsStartDir: str,
                 nodeDict: dict[Node]
                 ):
        self.grid = grid

        self.playerStartPosition = Coords(playerStartPos)
        self.ghostsStartPosition = Coords(ghostsStartPos)

        self.playerStartDirection = playerStartDir
        self.ghostsStartDirection = ghostsStartDir

        self.nodesDictionary = nodeDict
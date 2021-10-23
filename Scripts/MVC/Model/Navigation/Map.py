from Scripts.MVC.Controller.MazeInfo.MazeGenerator import MazeGenerator
from Scripts.MVC.Model.Navigation.Coords import Coords


class Map():
    def __init__(self, mazeGenerator: MazeGenerator):
        self.grid = mazeGenerator.grid

        self.playerStartPosition = Coords(coords=mazeGenerator.playerStartPosition)
        self.ghostsStartPosition = Coords(coords=mazeGenerator.ghostsStartPosition)

        self.playerStartDirection = mazeGenerator.playerStartDirection
        self.ghostsStartDirection = mazeGenerator.ghostsStartDirection

        self.nodesDictionary = mazeGenerator.nodeDictionary
        self.roadsPositionsList = mazeGenerator.roadsPositions
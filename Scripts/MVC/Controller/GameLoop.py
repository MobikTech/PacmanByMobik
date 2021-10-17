from Scripts.MVC.Controller.MazeInfo.MazeGenerator import MazeGenerator
from Scripts.MVC.Model.Entities.Ghost import Ghost
from Scripts.MVC.Model.Entities.Player import Player
from Scripts.MVC.Model.Navigation.Map import Map


class GameLoop():
    def __init__(self):
        self.__mazeGenerator = MazeGenerator()
        self.map = Map(self.__mazeGenerator.grid,
                       self.__mazeGenerator.playerStartPosition,
                       self.__mazeGenerator.ghostsStartPosition,
                       self.__mazeGenerator.playerStartDirection,
                       self.__mazeGenerator.ghostsStartDirection,
                       self.__mazeGenerator.nodeDictionary)
        self.player = Player(self.map.playerStartPosition,
                             self.map.playerStartDirection)
        self.ghost = Ghost(self.map.ghostsStartPosition,
                           self.map.ghostsStartDirection)




    def start(self):

        pass

    def update(self):
        pass



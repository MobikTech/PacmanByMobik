import random

from Scripts.MVC.Controller.CoinsContainer import CoinsContainer
from Scripts.MVC.Controller.Common.Algorithmes import Algorithmes
from Scripts.MVC.Controller.Common.CommonClasses import CoordsBehaviour
from Scripts.MVC.Controller.Common.Constants import *
from Scripts.MVC.Controller.MazeInfo.MazeGenerator import MazeGenerator
from Scripts.MVC.Controller.MazeInfo.RandomMazeGenerator import RandomMazeGenerator
from Scripts.MVC.Model.Entities.Ghost import Ghost
from Scripts.MVC.Model.Entities.Player import Player
from Scripts.MVC.Model.Navigation.Coords import Coords
from Scripts.MVC.Model.Navigation.Map import Map
from Scripts.MVC.View.PathDrawer import PathDrawer


class Events():
    def __init__(self):
        self.playerPathCalculated = None
        self.ghostsPathCalculated = None
        self.coinCollected = None


class GameInfo():
    PLAYER_MOVEMENT_ALGORITHM = SEARCH_ALGORITHMES.ASTAR
    GHOSTS_MOVEMENT_ALGORITHM = SEARCH_ALGORITHMES.BFS
    MAX_HP_AMOUNT = 3
    SCORE_STEP_COUNTER = 10

    def __init__(self):
        self.__mazeGenerator = MazeGenerator()
        self.map = Map(self.__mazeGenerator)
        self.player = Player(self.map.playerStartPosition,
                             self.map.playerStartDirection)
        self.ghosts = list()

        self.__initGhosts()
        self.coinsContainer = CoinsContainer(self.map)
        self.background = self.__mazeGenerator.backgroundImage

        self.score = 0
        self.hp = GameInfo.MAX_HP_AMOUNT

    def __initGhosts(self):
        ghostTypes = [GHOST_TYPE.RIKKO]
        # ghostTypes = [GHOST_TYPE.RIKKO,
        #               GHOST_TYPE.PINKY,
        #               GHOST_TYPE.GREENKY,
        #               GHOST_TYPE.CLYNE]
        for type in ghostTypes:
            self.ghosts.append(Ghost(self.map.ghostsStartPosition,
                                     self.map.ghostsStartDirection,
                                     type))


class GameLoop():
    def __init__(self):
        self.info = GameInfo()
        self.events = Events()

    def start(self):
        pass

    def update(self):
        MotionManager.tryMoveEntities(self.info, self.events)
        CoinsManager.tryDeleteCoin(self.info, self.events.coinCollected)
        self.__collisionHandler()

    def __collisionHandler(self):
        if self.__tryCollideWithGhosts():
            self.info.hp -= 1
            self.__respawnAll()

    def __tryCollideWithGhosts(self):
        for ghost in self.info.ghosts:
            if ghost.coords == self.info.player.coords:
                return True
        return False

    def __respawnAll(self):
        self.info.player.respawn()
        for ghost in self.info.ghosts:
            ghost.respawn()
        MotionManager.resetPlayerPathProps()


class CoinsManager():

    @staticmethod
    def tryDeleteCoin(gameInfo: GameInfo, event):
        if gameInfo.coinsContainer.tryDeleteCoin(gameInfo.player.coords) == True:
            gameInfo.score += GameInfo.SCORE_STEP_COUNTER
            if event != None:
                event(gameInfo.player.coords)



# class EntityMotionInfo():
#     def __init__(self, entity):
#         self.entity = entity
#
#         self.currentPlayerStartPoint = None
#         self.currentPlayerTarget = None
#         self.currentPlayerPath = None
#         self.currentPlayerDirection = None
#         self.currentPlayerDirectionIndex = None


class MotionManager():
    currentPlayerStartPoint = None
    currentPlayerTarget = None
    currentPlayerPath = None
    currentPlayerDirection = None
    currentPlayerDirectionIndex = None

    @staticmethod
    def resetPlayerPathProps():
        MotionManager.currentPlayerStartPoint = None
        MotionManager.currentPlayerTarget = None
        MotionManager.currentPlayerPath = None
        MotionManager.currentPlayerDirection = None
        MotionManager.currentPlayerDirectionIndex = None

    @staticmethod
    def tryMoveEntities(gameInfo: GameInfo, events: Events):

        MotionManager.__tryMovePlayer(gameInfo, events.playerPathCalculated)
        MotionManager.__tryMoveGhosts(gameInfo, events.ghostsPathCalculated)


    # region PlayerMovement
    @staticmethod
    def __tryMovePlayer(gameInfo: GameInfo, event):

        if MotionManager.currentPlayerPath == None:
            MotionManager.__recalculatePlayerPath(gameInfo)

        elif gameInfo.player.coords == MotionManager.currentPlayerTarget:
            MotionManager.__recalculatePlayerPath(gameInfo)

        if CoordsBehaviour.inCellCenter(gameInfo.player.coordsWorld):
            MotionManager.__tryChangeDirection(gameInfo)

        gameInfo.player.move()

        if event != None:
            event(MotionManager.currentPlayerPath,
                  MotionManager.currentPlayerStartPoint,
                  MotionManager.currentPlayerTarget,
                  COLORS.WHITE)

    @staticmethod
    def __tryChangeDirection(gameInfo: GameInfo):
        currentCellType = gameInfo.map.grid[gameInfo.player.coords.getTuple()]
        if currentCellType == CELL_TYPE.CROSSROAD:
            MotionManager.currentPlayerDirectionIndex += 1
            MotionManager.currentPlayerDirection = \
                gameInfo.player.direction = \
                MotionManager.currentPlayerPath[MotionManager.currentPlayerDirectionIndex]

    @staticmethod
    def __recalculatePlayerPath(gameInfo: GameInfo):
        MotionManager.currentPlayerDirectionIndex = 0
        MotionManager.currentPlayerStartPoint = gameInfo.player.coords
        # MotionManager.currentPlayerTarget = Coords((22, 14))
        MotionManager.currentPlayerTarget = Coords(random.choice(gameInfo.map.roadsPositionsList))
        MotionManager.currentPlayerPath = Algorithmes.getPathToTarget(GameInfo.PLAYER_MOVEMENT_ALGORITHM,
                                                                      MotionManager.currentPlayerStartPoint,
                                                                      MotionManager.currentPlayerTarget,
                                                                      gameInfo.map)
        MotionManager.currentPlayerDirection = gameInfo.player.direction = MotionManager.currentPlayerPath[0]

    # endregion

    # region GhostsMovement
    @staticmethod
    def __tryMoveGhosts(gameInfo: GameInfo, event):
        for ghost in gameInfo.ghosts:
            MotionManager.__tryMoveGhost(ghost, gameInfo, event)

    @staticmethod
    def __tryMoveGhost(ghost, gameInfo: GameInfo, event):
        #region collision handler
        if ghost.coords == gameInfo.player.coords:
            return
        #endregion

        if not RandomMazeGenerator.inMapRect(ghost.coords):
            ghost.move()
            return

        ghostPath = Algorithmes.getPathToTarget(GameInfo.GHOSTS_MOVEMENT_ALGORITHM,
                                                ghost.coords,
                                                gameInfo.player.coords,
                                                gameInfo.map)

        if CoordsBehaviour.inCellCenter(ghost.coordsWorld):
            ghost.direction = ghostPath[0]
            # MotionManager.__tryChangeDirection(gameInfo)

        if event != None:
            event(ghostPath,
                  ghost.coords,
                  gameInfo.player.coords,
                  PathDrawer.getGhostColor(ghost.ghostType))

        ghost.move()

    # endregion

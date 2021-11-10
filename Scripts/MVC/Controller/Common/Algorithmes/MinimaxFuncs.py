# from Scripts.MVC.Controller.Common.Algorithmes.Algorithmes import MapNavigationFuncs
from Scripts.MVC.Controller.Common.Algorithmes.Algorithmes import NodesNavigationFuncs
from Scripts.MVC.Controller.Common.CommonClasses import DirectionManager
from Scripts.MVC.Model.Entities.Player import Player
from Scripts.MVC.Model.Navigation.Coords import Coords, CELL_TYPE
from Scripts.MVC.Model.Navigation.Map import Map
from Scripts.MVC.Model.Navigation.Nodes import Node


class ExtraInfo():
    def __init__(self, coinsDict, ghosts):
        self.coinsDict = coinsDict
        self.ghosts = ghosts


class GameState():
    def __init__(self, playerNode: Node, map: Map, coinsDict: dict, evaluation: int, ghostsCoords:list=None, ghostsInfos:list=None):
        self.__map = map
        self.__coinsDict = coinsDict
        self.playerNode = playerNode
        self.evaluation = evaluation
        if ghostsCoords:
            self.ghostsInfos = self.__getGhostsInfos(playerNode, ghostsCoords)
        elif ghostsInfos:
            self.ghostsInfos = ghostsInfos

    def __defineGhostsNearestNode(self, ghostsCoords):
        unfoundedGhostsNearestNodes = dict()
        for ghostCoords in ghostsCoords:
            unfoundedGhostsNearestNodes[ghostCoords.getTuple()] = NodesNavigationFuncs.findNearestNodeTo(ghostCoords,
                                                                                                         self.__map)
        return unfoundedGhostsNearestNodes

    def __getGhostsInfos(self, playerNode, ghostsCoords):
        ghostsInfos = list()
        unfoundedGhostsNearestNodes = self.__defineGhostsNearestNode(ghostsCoords)

        queue = [(playerNode, [playerNode])]
        visited = list()
        while queue:
            node, path = queue.pop(0)
            visited.append(node)

            if len(unfoundedGhostsNearestNodes.keys()) < 1:
                return ghostsInfos

            for ghostPosition in list(unfoundedGhostsNearestNodes.keys()):
                ghostCoords = Coords(ghostPosition)
                if node == unfoundedGhostsNearestNodes[ghostPosition]:
                    direction, offset = NodesNavigationFuncs.getOffsetFromNearestNode(path[-1], ghostCoords)
                    ghostsInfos.append(GhostInfo(ghostCoords, path, offset, direction))
                    unfoundedGhostsNearestNodes.pop(ghostPosition)

            for nodeInfo in node.neighborsNodeInfo.values():
                if nodeInfo == None:
                    continue
                if visited.__contains__(nodeInfo.node) == False:
                    newPath = path.copy()
                    newPath.append(nodeInfo.node)
                    queue.append((nodeInfo.node, newPath))

    def __getGhostsInfosCopy(self):
        newGhostsInfos = list()
        for ghostInfo in self.ghostsInfos:
            newGhostsInfos.append(ghostInfo.__copy__())
        return newGhostsInfos

    def __makeGhostsTurn(self, distance):
        for ghostInfo in self.ghostsInfos:
            self.__moveGhostByPath(ghostInfo, distance)

    def __moveGhostByPath(self, ghostInfo, distance):
        ghostCoords = ghostInfo.ghostCoords
        distanceLeft = distance

        while distanceLeft > 0:

            if ghostInfo.extraLength > 0:
                directionToPlayer = DirectionManager.getOppositeToDirection(ghostInfo.extraDirection)
                distanceToLastNode = int(min(distanceLeft, ghostInfo.extraLength))
                ghostCoords.offsetTo(directionToPlayer, distanceToLastNode)
                distanceLeft -= distanceToLastNode
                ghostInfo.extraLength -= distanceToLastNode
                if ghostInfo.extraLength == 0:
                    ghostInfo.extraDirection = None

            elif len(ghostInfo.nodeList) < 2:
                break

            else:
                directionToPlayer, distanceBetweenNeighbors = NodesNavigationFuncs.getDirectionAndLengthBetweenNodes(
                    ghostInfo.nodeList[-1],
                    ghostInfo.nodeList[-2])
                distanceToPlayer = int(min(distanceLeft, distanceBetweenNeighbors))
                ghostCoords.offsetTo(directionToPlayer, distanceToPlayer)
                ghostInfo.nodeList.pop()
                distanceLeft -= distanceToPlayer
                ghostInfo.extraLength = distanceBetweenNeighbors - distanceToPlayer
                if ghostInfo.extraLength > 0:
                    ghostInfo.extraDirection = DirectionManager.getOppositeToDirection(directionToPlayer)
                else:
                    ghostInfo.extraDirection = None

            if self.__map.grid[ghostCoords.getTuple()] == CELL_TYPE.WALL:
                raise Exception('Incorrect coords {0}, it is a wall'.format(ghostCoords.__str__()))

    @staticmethod
    def getNewGameState(oldGameState, newPlayerNode):
        traveledDistance = NodesNavigationFuncs.getLengthBetweenNeighbors(oldGameState.playerNode.coords,
                                                                          newPlayerNode.coords)
        newGameState = GameState(newPlayerNode, oldGameState.__map,
                                 oldGameState.__coinsDict, 0, ghostsInfos=oldGameState.__getGhostsInfosCopy())
        newGameState.__makeGhostsTurn(traveledDistance)
        newGameState.evaluation = MinimaxFuncs.evaluateNeighbor(oldGameState.playerNode,
                                                                newPlayerNode,
                                                                oldGameState.__coinsDict,
                                                                newGameState.ghostsInfos)
        return newGameState


class MinimaxFuncs():
    COIN_COST = 0
    GHOST_COST = -30

    @staticmethod
    def evaluateNeighbor(startNode, nextNode, coinsDict: dict, ghostsInfos):
        from Scripts.MVC.Controller.Common.Algorithmes.Algorithmes import MapNavigationFuncs
        direction = MapNavigationFuncs.getDirectionToNeighbour(startNode.coords, nextNode.coords)
        evaluateValue = 0
        currentCoords = startNode.coords.__copy__()
        #todo remove
        roadLength = 0
        while currentCoords != nextNode.coords:
            if coinsDict.keys().__contains__(currentCoords.getTuple()):
                evaluateValue += MinimaxFuncs.COIN_COST
            for ghostInfo in ghostsInfos:
                if currentCoords == ghostInfo.ghostCoords:
                    evaluateValue += MinimaxFuncs.GHOST_COST
            currentCoords.offsetTo(direction, 1)
            roadLength += 1
        if coinsDict.keys().__contains__(currentCoords.getTuple()):
            evaluateValue += MinimaxFuncs.COIN_COST
        return evaluateValue

    @staticmethod
    def minimax(startNode, depth, isMaximizingPlayer, alpha, beta, prestartNode):
        # should return best direction
        # returned (direction, value)
        INFINITY = 10000

        if depth == 0:
            return None, 0

        if isMaximizingPlayer:
            bestValue = -INFINITY
            bestDirection = None

            for nodeDirection in NodesNavigationFuncs.getNodeDirections(startNode):
                neighborInfo = startNode.neighborsNodeInfo[nodeDirection]

                newGameState = GameState(neighborInfo.node, gameState.ghostsPaths)

                if neighborInfo.node == prestartNode:
                    continue

                currentValue = MinimaxFuncs.evaluateNeighbor(startNode, neighborInfo.node, extraInfo.coinsDict,
                                                             extraInfo.ghosts)
                direction, value = MinimaxFuncs.minimax(neighborInfo.node, depth - 1, False, alpha, beta, extraInfo,
                                                        startNode)
                currentValue += value

                if currentValue >= bestValue:
                    bestValue = currentValue
                    bestDirection = nodeDirection

                alpha = max(alpha, bestValue)
                if beta <= alpha:
                    break
            return bestDirection, bestValue
        else:
            bestValue = +INFINITY
            bestDirection = None
            for nodeDirection in NodesNavigationFuncs.getNodeDirections(startNode):
                neighborInfo = startNode.neighborsNodeInfo[nodeDirection]
                if neighborInfo.node == prestartNode:
                    continue

                currentValue = MinimaxFuncs.estimateNeighbor(startNode, neighborInfo.node, extraInfo.coinsDict,
                                                             extraInfo.ghosts)
                direction, value = MinimaxFuncs.minimax(neighborInfo.node, depth - 1, True, alpha, beta, extraInfo,
                                                        startNode)
                currentValue += value

                if currentValue <= bestValue:
                    bestValue = currentValue
                    bestDirection = nodeDirection

                beta = min(beta, bestValue)
                if beta <= alpha:
                    break
            return bestDirection, bestValue

    @staticmethod
    def evaluateDirection(depth, restBranchValue, betweenNeighborsValue):
        fullValue = restBranchValue + betweenNeighborsValue * depth
        return fullValue

    # @staticmethod
    # def minimax(depth, prestartNode, gameState: GameState):
    #     # should return best direction
    #     # returned (bestDirection, totalValue)
    #     INFINITY = 10000
    #
    #     if depth == 0:
    #         return None, 0
    #
    #     bestDirection = None
    #     totalNodeValue = 0
    #     bestValue = -INFINITY
    #
    #     # # todo test
    #     testInfo = TestInfo()
    #
    #     for nodeDirection in NodesNavigationFuncs.getNodeDirections(gameState.playerNode):
    #         neighborInfo = gameState.playerNode.neighborsNodeInfo[nodeDirection]
    #
    #         newPlayerNode = neighborInfo.node
    #         if newPlayerNode == prestartNode:
    #             continue
    #         newGameState = GameState.getNewGameState(gameState, newPlayerNode)
    #
    #         neighborEvaluation = newGameState.evaluation
    #         # neighborsEvaluation += neighborEvaluation
    #
    #         (direction, restBranchValue) = MinimaxFuncs.minimax(depth - 1, gameState.playerNode, newGameState)
    #         # fullValue = (restBranchValue + neighborEvaluation * 4 ) * depth
    #         fullValue = MinimaxFuncs.evaluateDirection(depth, restBranchValue, neighborEvaluation)
    #         totalNodeValue += fullValue
    #
    #         # todo test
    #         testInfo.possibleValues.append((fullValue, nodeDirection))
    #
    #
    #         if fullValue > bestValue:
    #             bestValue = fullValue
    #             bestDirection = nodeDirection
    #
    #     # todo test
    #     testInfo.chosenValue = bestValue
    #     testInfo.chosenDirection = bestDirection
    #     print('-----------')
    #     for possibleValue in testInfo.possibleValues:
    #         print('{0} - {1}'.format(possibleValue[0], possibleValue[1]))
    #     print('chosen value - {0}'.format(testInfo.chosenValue))
    #     print('chosen direction - {0}'.format(testInfo.chosenDirection))
    #
    #     return bestDirection, totalNodeValue


class TestInfo():
    def __init__(self):
        self.possibleValues = list()
        self.chosenDirection = None
        self.chosenValue = None


class GhostInfo():
    def __init__(self, ghostCoords, nodeList, extraLength, extraDirection):
        self.ghostCoords = ghostCoords.__copy__()
        self.nodeList = nodeList.copy()
        self.extraLength = extraLength
        self.extraDirection = extraDirection

    def __copy__(self):
        return GhostInfo(self.ghostCoords, self.nodeList, self.extraLength, self.extraDirection)

    def getGhostsCoords(self):
        pass

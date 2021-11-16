# from Scripts.MVC.Controller.Common.Algorithmes.Algorithmes import MapNavigationFuncs
import random

from Scripts.MVC.Controller.Common.Algorithmes.Algorithmes import NodesNavigationFuncs
from Scripts.MVC.Controller.Common.CommonClasses import DirectionManager
from Scripts.MVC.Controller.Common.Constants import AI_ALGORITHMES
from Scripts.MVC.Model.Entities.Player import Player
from Scripts.MVC.Model.Navigation.Coords import Coords, CELL_TYPE
from Scripts.MVC.Model.Navigation.Map import Map
from Scripts.MVC.Model.Navigation.Nodes import Node


class ExtraInfo():
    def __init__(self, coinsDict, ghosts):
        self.coinsDict = coinsDict
        self.ghosts = ghosts


class GameState():
    def __init__(self, playerNode: Node, map: Map, coinsDict: dict, evaluation: int, ghostsCoords:list):
        self.__map = map
        self.__coinsDict = coinsDict
        self.playerNode = playerNode
        self.evaluation = evaluation
        self.ghostsInfos = self.__getGhostsInfos(playerNode, ghostsCoords)

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

    def __makeGhostsTurn(self, distance, algorithm):
        for ghostInfo in self.ghostsInfos:
            if algorithm == AI_ALGORITHMES.MINIMAX:
                self.__moveGhostByPath(ghostInfo, distance)
            elif algorithm == AI_ALGORITHMES.EXPECTIMAX:
                self.__moveGhostRandomly(ghostInfo, distance, self.__map.grid)

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

    def __moveGhostRandomly(self, ghostInfo, distance, grid):
        ghostCoords = ghostInfo.ghostCoords
        distanceLeft = distance

        possibleDirections = DirectionManager.getPossibleDirections(ghostCoords, grid)
        direction = random.choice(possibleDirections)
        while distanceLeft > 0:
            ghostCoords.offsetTo(direction, 1)
            distanceLeft -= 1
            if grid[ghostCoords.getTuple()] == CELL_TYPE.CROSSROAD:
                possibleDirections = DirectionManager.getPossibleDirections(ghostCoords, grid)
                direction = random.choice(possibleDirections)

            if self.__map.grid[ghostCoords.getTuple()] == CELL_TYPE.WALL:
                raise Exception('Incorrect coords {0}, it is a wall'.format(ghostCoords.__str__()))

    def __getGhostsCoordsCopy(self):
        ghostsCoords = []
        for info in self.ghostsInfos:
            ghostsCoords.append(info.ghostCoords.__copy__())
        return ghostsCoords

    @staticmethod
    def getNewGameState(oldGameState, newPlayerNode, algorithm):
        traveledDistance = NodesNavigationFuncs.getLengthBetweenNeighbors(oldGameState.playerNode.coords,
                                                                          newPlayerNode.coords)
        newGameState = GameState(newPlayerNode, oldGameState.__map,
                                 oldGameState.__coinsDict, 0, oldGameState.__getGhostsCoordsCopy())
        newGameState.__makeGhostsTurn(traveledDistance, algorithm)
        newGameState.evaluation = MinimaxFuncs.evaluateNeighbor(oldGameState.playerNode,
                                                                newPlayerNode,
                                                                oldGameState.__coinsDict,
                                                                oldGameState.ghostsInfos)
        return newGameState


class MinimaxFuncs():
    COIN_COST = 1
    EXTRA_COINS_COST = 1
    GHOST_COST = -10
    INFINITY = 1000000

    @staticmethod
    def evaluateNeighbor(startNode, nextNode, coinsDict: dict, ghostsInfos):
        from Scripts.MVC.Controller.Common.Algorithmes.Algorithmes import MapNavigationFuncs
        direction = MapNavigationFuncs.getDirectionToNeighbour(startNode.coords, nextNode.coords)
        # print(direction)
        evaluateValue = 0
        currentCoords = startNode.coords.__copy__()
        #todo remove
        roadLength = 0
        coinsCost = MinimaxFuncs.COIN_COST
        if len(coinsDict) < 20:
            coinsCost += MinimaxFuncs.EXTRA_COINS_COST
        elif len(coinsDict) < 10:
            coinsCost += MinimaxFuncs.EXTRA_COINS_COST * 2
        while currentCoords != nextNode.coords:
            # print()
            # print('coords - ' + str(currentCoords))
            if coinsDict.keys().__contains__(currentCoords.getTuple()):
                evaluateValue += coinsCost
            for ghostInfo in ghostsInfos:
                # print('ghost - ' + str(ghostInfo.ghostCoords))
                if currentCoords == ghostInfo.ghostCoords:
                    # print(roadLength)
                    evaluateValue += MinimaxFuncs.GHOST_COST
            currentCoords.offsetTo(direction, 1)
            roadLength += 1
        if coinsDict.keys().__contains__(currentCoords.getTuple()):
            evaluateValue += MinimaxFuncs.COIN_COST
        return evaluateValue

    # @staticmethod
    # def minimax(depth, isMaximizingPlayer, alpha, beta, gameState):
    #     # should return best direction
    #     # returned (direction, value)
    #     INFINITY = 10000
    #
    #     if depth == 0:
    #         return None, 0
    #
    #     if isMaximizingPlayer:
    #         bestValue = -INFINITY
    #         bestDirection = None
    #
    #         for nodeDirection in NodesNavigationFuncs.getNodeDirections(startNode):
    #             neighborInfo = startNode.neighborsNodeInfo[nodeDirection]
    #
    #             newGameState = GameState(neighborInfo.node, gameState.ghostsPaths)
    #
    #             if neighborInfo.node == prestartNode:
    #                 continue
    #
    #             currentValue = MinimaxFuncs.estimateNeighbor(startNode, neighborInfo.node, extraInfo.coinsDict,
    #                                                          extraInfo.ghosts)
    #             direction, value = MinimaxFuncs.minimax(neighborInfo.node, depth - 1, False, alpha, beta, extraInfo,
    #                                                     startNode)
    #             currentValue += value
    #
    #             if currentValue >= bestValue:
    #                 bestValue = currentValue
    #                 bestDirection = nodeDirection
    #
    #             alpha = max(alpha, bestValue)
    #             if beta <= alpha:
    #                 break
    #         return bestDirection, bestValue
    #     else:
    #         bestValue = +INFINITY
    #         bestDirection = None
    #         for nodeDirection in NodesNavigationFuncs.getNodeDirections(startNode):
    #             neighborInfo = startNode.neighborsNodeInfo[nodeDirection]
    #             if neighborInfo.node == prestartNode:
    #                 continue
    #
    #             currentValue = MinimaxFuncs.estimateNeighbor(startNode, neighborInfo.node, extraInfo.coinsDict,
    #                                                          extraInfo.ghosts)
    #             direction, value = MinimaxFuncs.minimax(neighborInfo.node, depth - 1, True, alpha, beta, extraInfo,
    #                                                     startNode)
    #             currentValue += value
    #
    #             if currentValue <= bestValue:
    #                 bestValue = currentValue
    #                 bestDirection = nodeDirection
    #
    #             beta = min(beta, bestValue)
    #             if beta <= alpha:
    #                 break
    #         return bestDirection, bestValue

    @staticmethod
    def evaluateDirection(depth, restBranchValue, betweenNeighborsValue):
        fullValue = restBranchValue + betweenNeighborsValue * depth
        return fullValue

    @staticmethod
    def minimax(depth, prestartNode, gameState: GameState, path: list):
        if depth == 0:
            return None, 0

        bestDirection = None
        totalNodeValue = 0
        bestValue = -MinimaxFuncs.INFINITY
        path.append(gameState.playerNode)

        neighborDirections = NodesNavigationFuncs.getNodeDirections(gameState.playerNode)
        neighborCount = len(neighborDirections)
        for nodeDirection in neighborDirections:
            neighborInfo = gameState.playerNode.neighborsNodeInfo[nodeDirection]
            newPlayerNode = neighborInfo.node

            if path.__contains__(newPlayerNode):
                continue

            if newPlayerNode == prestartNode:
                continue
            newGameState = GameState.getNewGameState(gameState, newPlayerNode, AI_ALGORITHMES.MINIMAX)

            neighborEvaluation = newGameState.evaluation
            # neighborsEvaluation += neighborEvaluation

            (direction, restBranchValue) = MinimaxFuncs.minimax(depth - 1, gameState.playerNode, newGameState, path.copy())

            fullValue = MinimaxFuncs.evaluateDirection(depth, restBranchValue, neighborEvaluation)
            totalNodeValue += fullValue


            if fullValue > bestValue:
                bestValue = fullValue
                bestDirection = nodeDirection

        totalNodeValue = int(totalNodeValue / neighborCount)
        return bestDirection, totalNodeValue

    @staticmethod
    def expectimax(depth, prestartNode, gameState: GameState, path: list):
        if depth == 0:
            return None, 0

        bestDirection = None
        totalNodeValue = 0
        bestValue = -MinimaxFuncs.INFINITY
        path.append(gameState.playerNode)

        neighborDirections = NodesNavigationFuncs.getNodeDirections(gameState.playerNode)
        neighborCount = len(neighborDirections)
        for nodeDirection in neighborDirections:
            neighborInfo = gameState.playerNode.neighborsNodeInfo[nodeDirection]
            newPlayerNode = neighborInfo.node

            if path.__contains__(newPlayerNode):
                continue

            if newPlayerNode == prestartNode:
                continue
            newGameState = GameState.getNewGameState(gameState, newPlayerNode, AI_ALGORITHMES.EXPECTIMAX)
            neighborEvaluation = newGameState.evaluation
            (direction, restBranchValue) = MinimaxFuncs.expectimax(depth - 1, gameState.playerNode, newGameState,
                                                                path.copy())
            fullValue = MinimaxFuncs.evaluateDirection(depth, restBranchValue, neighborEvaluation)
            totalNodeValue += fullValue

            if fullValue > bestValue:
                bestValue = fullValue
                bestDirection = nodeDirection

        totalNodeValue = totalNodeValue / neighborCount
        return bestDirection, totalNodeValue


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

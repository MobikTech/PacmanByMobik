# from Scripts.MVC.Controller.Common.Algorithmes.Algorithmes import MapNavigationFuncs
from Scripts.MVC.Controller.Common.Algorithmes.Algorithmes import NodesNavigationFuncs
from Scripts.MVC.Controller.Common.CommonClasses import DirectionManager
from Scripts.MVC.Model.Entities.Player import Player
from Scripts.MVC.Model.Navigation.Coords import Coords
from Scripts.MVC.Model.Navigation.Map import Map
from Scripts.MVC.Model.Navigation.Nodes import Node


class ExtraInfo():
    def __init__(self, coinsDict, ghosts):
        self.coinsDict = coinsDict
        self.ghosts = ghosts

class GameState():
    def __init__(self, playerNode: Node, ghostsCoords: list, map: Map, coinsDict: dict, evaluation: int):
        self.__map = map
        self.__coinsDict = coinsDict
        self.playerNode = playerNode
        self.ghostsPaths: dict[Coords, PathToGhost] = self.__initGhostPaths(playerNode, self.__getGhostsCoordsCopy(ghostsCoords))
        self.evaluation = evaluation

    def __getGhostsCoordsCopy(self, ghostsCoords: list):
        newGhostsCoords = list()
        for coords in ghostsCoords:
            newGhostsCoords.append(coords.__copy__())
            return newGhostsCoords

    def __initGhostPaths(self, startNode: Node, ghostsCoords: list):
        unfoundedGhostsNearestNodes = self.__defineGhostsNearestNode(ghostsCoords)
        ghostsPathDict = self.__bfsForGhosts(startNode, unfoundedGhostsNearestNodes)
        return ghostsPathDict

    def __defineGhostsNearestNode(self, ghostsCoords):
        unfoundedGhostsNearestNodes = dict()
        for ghostCoords in ghostsCoords:
            unfoundedGhostsNearestNodes[ghostCoords] = NodesNavigationFuncs.findNearestNodeTo(ghostCoords, self.__map)
            return unfoundedGhostsNearestNodes

    def __bfsForGhosts(self, startNode, unfoundedGhostsNearestNodes):
        ghostsPathDict = dict()

        queue = [(startNode, [startNode])]
        visited = list()
        while queue:
            node, path = queue.pop(0)
            visited.append(node)

            if len(unfoundedGhostsNearestNodes.keys()) < 1:
                return ghostsPathDict

            for ghostCoords in unfoundedGhostsNearestNodes.keys():
                # ghostCoords = ghostCoords.__copy__()
                if node == unfoundedGhostsNearestNodes[ghostCoords]:
                    direction, offset = NodesNavigationFuncs.getOffsetFromNearestNode(path[-1], ghostCoords)
                    ghostsPathDict[ghostCoords] = PathToGhost(path, offset, direction)
                    unfoundedGhostsNearestNodes.pop(ghostCoords)

            for nodeInfo in node.neighborsNodeInfo.values():
                if nodeInfo == None:
                    continue
                if visited.__contains__(nodeInfo.node) == False:
                    newPath = path.copy()
                    newPath.append(nodeInfo.node)
                    queue.append((nodeInfo.node, newPath))

    def __moveGhostsByPath(self, distance):
        for ghostCoords in self.ghostsPaths.keys():
            distanceLeft = distance
            pathToGhost = self.ghostsPaths[ghostCoords]

            while distanceLeft > 0:

                if len(pathToGhost.nodeList) < 2:
                    # todo substitute by func
                    directionToPlayer = DirectionManager.getOppositeToDirection(pathToGhost.extraDirection)
                    distanceToPlayer = min(distanceLeft, pathToGhost.extraLength)
                    ghostCoords.offsetTo(directionToPlayer, distanceToPlayer)
                    distanceLeft = 0
                    pathToGhost.extraLength -= distanceLeft
                    return


                if pathToGhost.extraLength > 0:
                    # todo substitute by func
                    directionToPlayer = DirectionManager.getOppositeToDirection(pathToGhost.extraDirection)
                    distanceToLastNode = min(distanceLeft, pathToGhost.extraLength)
                    ghostCoords.offsetTo(directionToPlayer, distanceToLastNode)
                    distanceLeft -= distanceToLastNode
                    pathToGhost.extraLength -= distanceToLastNode

                else:
                    directionBetweenNeighbors, distanceBetweenNeighbors = NodesNavigationFuncs.getDirectionAndLengthBetweenNodes(
                        pathToGhost.nodeList[-1],
                        pathToGhost.nodeList[-2])
                    distanceToPlayer = min(distanceLeft, distanceBetweenNeighbors)
                    ghostCoords.offsetTo(directionBetweenNeighbors, distanceToPlayer)
                    distanceLeft -= distanceToPlayer
                    pathToGhost.extraLength = distanceBetweenNeighbors - distanceToPlayer

    def __evaluatePath(self):

        pass

    def getOffsettedGameState(self, newPlayerNode: Node):
        gameState = GameState(newPlayerNode, list(self.ghostsPaths.keys()), self.__map, self.__coinsDict, 0)
        traveledDistance = NodesNavigationFuncs.getLengthBetweenNeighbors(self.playerNode.coords, newPlayerNode.coords)
        gameState.__moveGhostsByPath(traveledDistance)
        gameState.evaluation = MinimaxFuncs.evaluateNeighbor(self.playerNode,
                                                             newPlayerNode,
                                                             gameState.__coinsDict,
                                                             gameState.ghostsPaths.keys())



class MinimaxFuncs():
    COIN_COST = 1
    GHOST_COST = -10

    def __init__(self, ghosts):
        self.ghosts = ghosts

    #todo remove
    def __getGameState(self, gameInfo):
        return GameState(gameInfo.player, gameInfo.ghosts, gameInfo.map, gameInfo.coinsContainer.coinsDict)

    @staticmethod
    def evaluateNeighbor(startNode, nextNode,
                         coinsDict: dict,
                         ghostsCoords):
        from Scripts.MVC.Controller.Common.Algorithmes.Algorithmes import MapNavigationFuncs
        direction = MapNavigationFuncs.getDirectionToNeighbour(startNode.coords, nextNode.coords)
        evaluateValue = 0
        currentCoords = startNode.coords.__copy__()
        while currentCoords != nextNode.coords:
            if coinsDict.keys().__contains__(currentCoords.getTuple()):
                evaluateValue += MinimaxFuncs.COIN_COST
            for ghostCoords in ghostsCoords:
                if currentCoords == ghostCoords:
                    evaluateValue += MinimaxFuncs.GHOST_COST
            currentCoords.offsetTo(direction, 1)
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
    def minimax(depth, alpha, beta, prestartNode, gameState: GameState):
        # should return best direction
        # returned (direction, value)
        INFINITY = 10000

        if depth == 0:
            return None, 0

        bestValue = -INFINITY
        bestDirection = None
        totalValue = 0
        direction = None

        leavesEvaluation = 0

        for nodeDirection in NodesNavigationFuncs.getNodeDirections(gameState.playerNode):
            neighborInfo = gameState.playerNode.neighborsNodeInfo[nodeDirection]

            newPlayerNode = neighborInfo.node
            newGameState = gameState.getOffsettedGameState(newPlayerNode)

            if newPlayerNode == prestartNode:
                continue

            leavesEvaluation

            currentValue = MinimaxFuncs.evaluateNeighbor(startNode, neighborInfo.node, extraInfo.coinsDict,
                                                         extraInfo.ghosts)
            (direction, value) = MinimaxFuncs.minimax(neighborInfo.node, depth - 1, False, alpha, beta, extraInfo,
                                                    startNode)
            currentValue += value

            if currentValue >= bestValue:
                bestValue = currentValue
                bestDirection = nodeDirection

            alpha = max(alpha, bestValue)
            if beta <= alpha:
                break

        return bestDirection, bestValue





class PathToGhost():
    def __init__(self, nodeList, extraLength, extraDirection):
        self.nodeList = nodeList
        self.extraLength = extraLength
        self.extraDirection = extraDirection


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
    def __init__(self, playerNode: Node, ghostsCoords: list, map: Map, coinsDict: dict, evaluation: int):
        self.__map = map
        self.__coinsDict = coinsDict
        self.__ghostsCoords = ghostsCoords
        self.playerNode = playerNode
        self.ghostsPaths: list[PathToGhost] = self.__initGhostPaths(playerNode, self.__getGhostsCoordsCopy(ghostsCoords))
        self.evaluation = evaluation

    def __copy__(self):
        return GameState(self.playerNode, self.__getGhostsCoordsCopy(self.__ghostsCoords), self.__map, self.__coinsDict, self.evaluation)

    def __getGhostsCoordsCopy(self, ghostsCoords: list):
        newGhostsCoords = list()
        for coords in ghostsCoords:
            newGhostsCoords.append(coords.__copy__())
        return newGhostsCoords

    def __initGhostPaths(self, startNode: Node, ghostsCoords: list):
        unfoundedGhostsNearestNodes = self.__defineGhostsNearestNode(ghostsCoords)
        ghostsPaths = self.__bfsForGhosts(startNode, unfoundedGhostsNearestNodes)
        return ghostsPaths

    def __defineGhostsNearestNode(self, ghostsCoords):
        unfoundedGhostsNearestNodes = dict()
        for ghostCoords in ghostsCoords:
            unfoundedGhostsNearestNodes[ghostCoords.getTuple()] = NodesNavigationFuncs.findNearestNodeTo(ghostCoords, self.__map)
        return unfoundedGhostsNearestNodes

    def __bfsForGhosts(self, startNode, unfoundedGhostsNearestNodes):
        ghostsPaths = list()

        queue = [(startNode, [startNode])]
        visited = list()
        while queue:
            node, path = queue.pop(0)
            visited.append(node)

            if len(unfoundedGhostsNearestNodes.keys()) < 1:
                return ghostsPaths

            for ghostPosition in list(unfoundedGhostsNearestNodes.keys()):
                ghostCoords = Coords(ghostPosition)
                if node == unfoundedGhostsNearestNodes[ghostPosition]:
                    direction, offset = NodesNavigationFuncs.getOffsetFromNearestNode(path[-1], ghostCoords)
                    ghostsPaths.append(PathToGhost(ghostCoords, path, offset, direction))
                    unfoundedGhostsNearestNodes.pop(ghostPosition)

            # for ghostCoords in list(unfoundedGhostsNearestNodes.keys()):
            #     # ghostCoords = ghostCoords.__copy__()
            #     if node == unfoundedGhostsNearestNodes[ghostCoords]:
            #         direction, offset = NodesNavigationFuncs.getOffsetFromNearestNode(path[-1], ghostCoords)
            #         ghostsPathDict[ghostCoords] = PathToGhost(path, offset, direction)
            #         unfoundedGhostsNearestNodes.pop(ghostCoords)

            for nodeInfo in node.neighborsNodeInfo.values():
                if nodeInfo == None:
                    continue
                if visited.__contains__(nodeInfo.node) == False:
                    newPath = path.copy()
                    newPath.append(nodeInfo.node)
                    queue.append((nodeInfo.node, newPath))

    def __moveGhostsByPath(self, distance):
        for ghostPath in self.ghostsPaths:
            ghostCoords = ghostPath.ghostCoords
            ghostCoordsCopy = ghostCoords.__copy__()
            ghostPathCopy = ghostPath.__copy__()
            distanceLeft = distance
            # pathToGhost = self.ghostsPaths[ghostCoords]

            while distanceLeft > 0:

                if ghostPath.extraLength > 0:
                    # todo substitute by func
                    directionToPlayer = DirectionManager.getOppositeToDirection(ghostPath.extraDirection)
                    distanceToLastNode = int(min(distanceLeft, ghostPath.extraLength))
                    ghostCoords.offsetTo(directionToPlayer, distanceToLastNode)
                    distanceLeft -= distanceToLastNode
                    ghostPath.extraLength -= distanceToLastNode
                    if ghostPath.extraLength == 0:
                        ghostPath.extraDirection = None

                elif len(ghostPath.nodeList) < 2:
                    break

                else:
                    directionToPlayer, distanceBetweenNeighbors = NodesNavigationFuncs.getDirectionAndLengthBetweenNodes(
                        ghostPath.nodeList[-1],
                        ghostPath.nodeList[-2])
                    distanceToPlayer = int(min(distanceLeft, distanceBetweenNeighbors))
                    ghostCoords.offsetTo(directionToPlayer, distanceToPlayer)
                    # ghostPath.nodeList.pop(-1)
                    ghostPath.nodeList.pop()
                    distanceLeft -= distanceToPlayer
                    ghostPath.extraLength = distanceBetweenNeighbors - distanceToPlayer
                    if ghostPath.extraLength > 0:
                        ghostPath.extraDirection = DirectionManager.getOppositeToDirection(directionToPlayer)
                    else:
                        ghostPath.extraDirection = None

                if self.__map.grid[ghostCoords.getTuple()] == CELL_TYPE.WALL:
                    return
                    raise Exception('Incorrect coords {0}, it is a wall'.format(ghostCoords.__str__()))


        # for ghostCoords in self.ghostsPaths.keys():
        #     ghostCoordsCopy = ghostCoords.__copy__()
        #     ghostPathCopy = self.ghostsPaths[ghostCoordsCopy].__copy__()
        #     distanceLeft = distance
        #     pathToGhost = self.ghostsPaths[ghostCoords]
        #
        #     while distanceLeft > 0:
        #
        #         if pathToGhost.extraLength > 0:
        #             # todo substitute by func
        #             directionToPlayer = DirectionManager.getOppositeToDirection(pathToGhost.extraDirection)
        #             distanceToLastNode = int(min(distanceLeft, pathToGhost.extraLength))
        #             ghostCoords.offsetTo(directionToPlayer, distanceToLastNode)
        #             distanceLeft -= distanceToLastNode
        #             pathToGhost.extraLength -= distanceToLastNode
        #             if pathToGhost.extraLength == 0:
        #                 pathToGhost.extraDirection = None
        #
        #         elif len(pathToGhost.nodeList) < 2:
        #             break
        #
        #         else:
        #             directionToPlayer, distanceBetweenNeighbors = NodesNavigationFuncs.getDirectionAndLengthBetweenNodes(
        #                 pathToGhost.nodeList[-1],
        #                 pathToGhost.nodeList[-2])
        #             distanceToPlayer = int(min(distanceLeft, distanceBetweenNeighbors))
        #             ghostCoords.offsetTo(directionToPlayer, distanceToPlayer)
        #             pathToGhost.nodeList.pop(-1)
        #             distanceLeft -= distanceToPlayer
        #             pathToGhost.extraLength = distanceBetweenNeighbors - distanceToPlayer
        #             if pathToGhost.extraLength > 0:
        #                 pathToGhost.extraDirection = DirectionManager.getOppositeToDirection(directionToPlayer)
        #             else:
        #                 pathToGhost.extraDirection = None
        #
        #         if self.__map.grid[ghostCoords.getTuple()] == CELL_TYPE.WALL:
        #             raise Exception('Incorrect coords {0}, it is a wall'.format(ghostCoords.__str__()))

    def __getGhostsPaths(self, gameState):
        ghostsCoords = list()
        for ghostPath in gameState.ghostsPaths:
            ghostsCoords.append(ghostPath.ghostCoords)
        return ghostsCoords

    def getOffsettedGameState(self, newPlayerNode: Node):
        gameState = GameState(newPlayerNode, self.__getGhostsCoordsCopy(self.__ghostsCoords), self.__map, self.__coinsDict, 0)
        gameStateCopy = gameState.__copy__()
        traveledDistance = NodesNavigationFuncs.getLengthBetweenNeighbors(self.playerNode.coords, newPlayerNode.coords)
        gameState.__moveGhostsByPath(traveledDistance)

        gameStateCopy.__moveGhostsByPath(traveledDistance)

        gameState.evaluation = MinimaxFuncs.evaluateNeighbor(self.playerNode,
                                                             newPlayerNode,
                                                             gameState.__coinsDict,
                                                             self.__getGhostsCoordsCopy(self.__ghostsCoords))
        return gameState



class MinimaxFuncs():
    COIN_COST = 1
    GHOST_COST = -10


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
    def minimax(depth, prestartNode, gameState: GameState):
        # should return best direction
        # returned (bestDirection, totalValue)
        INFINITY = 10000

        if depth == 0:
            return None, 0

        bestDirection = None
        totalNodeValue = 0
        bestValue = -INFINITY

        # todo test
        testInfo = TestInfo()

        for nodeDirection in NodesNavigationFuncs.getNodeDirections(gameState.playerNode):
            neighborInfo = gameState.playerNode.neighborsNodeInfo[nodeDirection]

            newPlayerNode = neighborInfo.node
            if newPlayerNode == prestartNode:
                continue
            newGameState = gameState.getOffsettedGameState(newPlayerNode)


            neighborEvaluation = newGameState.evaluation
            # neighborsEvaluation += neighborEvaluation

            (direction, totalValue) = MinimaxFuncs.minimax(depth - 1, gameState.playerNode, newGameState)
            fullValue = totalValue + neighborEvaluation * depth * 2
            totalNodeValue += fullValue

            # todo test
            testInfo.possibleValues.append((fullValue, nodeDirection))


            if fullValue > bestValue:
                bestValue = fullValue
                bestDirection = nodeDirection

        # todo test
        testInfo.chosenValue = bestValue
        testInfo.chosenDirection = bestDirection
        # print('-----------')
        # for possibleValue in testInfo.possibleValues:
        #     print('{0} - {1}'.format(possibleValue[0], possibleValue[1]))
        # print('chosen value - {0}'.format(testInfo.chosenValue))
        # print('chosen direction - {0}'.format(testInfo.chosenDirection))

        return bestDirection, totalNodeValue


class TestInfo():
    def __init__(self):
        self.possibleValues = list()
        self.chosenDirection = None
        self.chosenValue = None


class PathToGhost():
    def __init__(self, ghostCoords, nodeList, extraLength, extraDirection):
        self.ghostCoords = ghostCoords
        self.nodeList = nodeList
        self.extraLength = extraLength
        self.extraDirection = extraDirection

    def __copy__(self):
        return PathToGhost(self.ghostCoords.__copy__(), self.nodeList.copy(), self.extraLength, self.extraDirection)


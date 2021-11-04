# from Scripts.MVC.Controller.Common.Algorithmes.Algorithmes import MapNavigationFuncs
from Scripts.MVC.Controller.Common.Algorithmes.Algorithmes import NodesNavigationFuncs
from Scripts.MVC.Model.Entities.Player import Player
from Scripts.MVC.Model.Navigation.Map import Map
from Scripts.MVC.Model.Navigation.Nodes import Node


class ExtraInfo():
    def __init__(self, coinsDict, ghosts):
        self.coinsDict = coinsDict
        self.ghosts = ghosts


class MinimaxFuncs():
    COIN_COST = 1
    GHOST_COST = -100

    def __init__(self, ghosts):
        self.ghosts = ghosts

    def __getGameState(self, gameInfo):
        return GameState(gameInfo.player, gameInfo.ghosts, gameInfo.map, gameInfo.coinsContainer.coinsDict)

    @staticmethod
    def estimateNeighbor(startNode, nextNode,
                         coinsDict: dict,
                         ghosts):
        from Scripts.MVC.Controller.Common.Algorithmes.Algorithmes import MapNavigationFuncs
        direction = MapNavigationFuncs.getDirectionToNeighbour(startNode.coords, nextNode.coords)
        estimateValue = 0
        currentCoords = startNode.coords.__copy__()
        while currentCoords != nextNode.coords:
            if coinsDict.keys().__contains__(currentCoords.getTuple()):
                estimateValue += MinimaxFuncs.COIN_COST
            for ghost in ghosts:
                if currentCoords == ghost.coords:
                    estimateValue += MinimaxFuncs.GHOST_COST
            currentCoords.offsetTo(direction, 1)
        if coinsDict.keys().__contains__(currentCoords.getTuple()):
            estimateValue += MinimaxFuncs.COIN_COST
        return estimateValue

    @staticmethod
    def minimax(startNode, depth, isMaximizingPlayer, alpha, beta, extraInfo, prestartNode):
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
                if neighborInfo.node == prestartNode:
                    continue

                currentValue = MinimaxFuncs.estimateNeighbor(startNode, neighborInfo.node, extraInfo.coinsDict,
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




class GameState():
    def __init__(self, player: Player, ghosts: list, map: Map, coinsDict: dict):
        self.player = player
        self.map = map
        self.ghostsPaths = self.__initGhostPaths(map.nodesDictionary[player.coords.getTuple()], ghosts)
        self.coinsDict = coinsDict

    def __initGhostPaths(self, startNode: Node, ghosts: list):
        unfoundedGhostsNearestNodes = self.__defineGhostsNearestNode(ghosts)
        ghostsPathDict = self.__bfsForGhosts(startNode, unfoundedGhostsNearestNodes)
        return ghostsPathDict

    def __defineGhostsNearestNode(self, ghosts):
        unfoundedGhostsNearestNodes = dict()
        for ghost in ghosts:
            unfoundedGhostsNearestNodes[ghost] = NodesNavigationFuncs.findNearestNodeTo(ghost.coords, self.map)
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

            for ghost in unfoundedGhostsNearestNodes.keys():
                if node == unfoundedGhostsNearestNodes[ghost]:
                    direction, offset = NodesNavigationFuncs.getOffsetFromNearestNode(path[-1], ghost.coords)
                    ghostsPathDict[ghost] = PathToGhost(path, offset, direction)
                    unfoundedGhostsNearestNodes.pop(ghost)

            for nodeInfo in node.neighborsNodeInfo.values():
                if nodeInfo == None:
                    continue
                if visited.__contains__(nodeInfo.node) == False:
                    newPath = path.copy()
                    newPath.append(nodeInfo.node)
                    queue.append((nodeInfo.node, newPath))


class PathToGhost():
    def __init__(self, nodeList, extraLength, extraDirection):
        self.nodeList = nodeList
        self.extraLength = extraLength
        self.extraDirection = extraDirection


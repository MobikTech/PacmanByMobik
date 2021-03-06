from math import sqrt, pow, fabs

from Scripts.MVC.Model.Navigation.Coords import Coords
from Scripts.MVC.Model.Navigation.Map import Map
from Scripts.MVC.Model.Navigation.Nodes import Node
from Scripts.MVC.Controller.Common.Constants import *


class Algorithmes():

    @staticmethod
    def __bfs(startNode: Node,
              targetNode: Node):
        queue = [(startNode, [startNode])]
        visited = list()
        while queue:
            node, path = queue.pop(0)
            visited.append(node)
            if node == targetNode:
                return path

            for nodeInfo in node.neighborsNodeInfo.values():
                if nodeInfo == None:
                    continue
                if visited.__contains__(nodeInfo.node) == False:
                    newPath = path.copy()
                    newPath.append(nodeInfo.node)
                    queue.append((nodeInfo.node, newPath))

    @staticmethod
    def __aStar(startNode: Node,
                targetNode: Node):
        from Scripts.MVC.Controller.Common.Algorithmes.AStarFuncs import AStarFuncs
        return AStarFuncs.aStar(startNode, targetNode)

    @staticmethod
    def minimax(gameInfo):
        DEPTH = 5
        from Scripts.MVC.Controller.Common.Algorithmes.MinimaxFuncs import MinimaxFuncs, GameState

        startNode = gameInfo.map.nodesDictionary[gameInfo.player.coords.getTuple()]
        ghostsCoords = list()
        for ghost in gameInfo.ghosts:
            ghostsCoords.append(ghost.coords.__copy__())

        result = MinimaxFuncs.minimax(DEPTH,
                                      None,
                                      GameState(startNode,
                                                gameInfo.map,
                                                gameInfo.coinsContainer.coinsDict,
                                                0,
                                                ghostsCoords=ghostsCoords),
                                      [])
        return result

    @staticmethod
    def expectimax(gameInfo):
        DEPTH = 5
        from Scripts.MVC.Controller.Common.Algorithmes.MinimaxFuncs import MinimaxFuncs, GameState

        startNode = gameInfo.map.nodesDictionary[gameInfo.player.coords.getTuple()]
        ghostsCoords = list()
        for ghost in gameInfo.ghosts:
            ghostsCoords.append(ghost.coords.__copy__())

        result = MinimaxFuncs.expectimax(DEPTH,
                                         None,
                                         GameState(startNode,
                                                   gameInfo.map,
                                                   gameInfo.coinsContainer.coinsDict,
                                                   0,
                                                   ghostsCoords=ghostsCoords),
                                         [])
        return result

    @staticmethod
    def getPathToTarget(algorithmType: int,
                        startPoint: Coords,
                        target: Coords,
                        map):
        directionsPath = list()

        startNearestNeighbour = NodesNavigationFuncs.findNearestNodeTo(startPoint, map)
        targetNearestNeighbour = NodesNavigationFuncs.findNearestNodeTo(target, map)

        nodesPath = None
        if algorithmType == SEARCH_ALGORITHMES.BFS:
            nodesPath = Algorithmes.__bfs(startNearestNeighbour, targetNearestNeighbour)
        elif algorithmType == SEARCH_ALGORITHMES.ASTAR:
            nodesPath = Algorithmes.__aStar(startNearestNeighbour, targetNearestNeighbour)

        if startNearestNeighbour == targetNearestNeighbour:
            firstNode = secondNode = lastNode = preLastNode = nodesPath[0]
        else:
            firstNode = nodesPath[0]
            secondNode = nodesPath[1]
            lastNode = nodesPath[-1]
            preLastNode = nodesPath[-2]

        if not NodesNavigationFuncs.isBetweenNeighborNodes(firstNode, secondNode, startPoint):
            directionsPath.append(MapNavigationFuncs.getDirectionToNeighbour(startPoint,
                                                                             firstNode.coords))
        for index in range(len(nodesPath) - 1):
            direction = MapNavigationFuncs.getDirectionToNeighbour(nodesPath[index].coords,
                                                                   nodesPath[index + 1].coords)
            directionsPath.append(direction)

        if not NodesNavigationFuncs.isBetweenNeighborNodes(lastNode, preLastNode, target):
            directionsPath.append(MapNavigationFuncs.getDirectionToNeighbour(lastNode.coords,
                                                                             target))
        return directionsPath


class NodesNavigationFuncs():

    @staticmethod
    def getNodeDirections(node: Node):
        directions = list()
        for direction in node.neighborsNodeInfo.keys():
            if node.neighborsNodeInfo[direction] != None:
                directions.append(direction)
        return directions

    @staticmethod
    def findNearestNodeTo(coords: Coords, map: Map):
        if map.grid[coords.getTuple()] == CELL_TYPE.WALL:
            raise Exception('Incorrect coords {0}, it is a wall'.format(coords.__str__()))

        nodes = map.nodesDictionary
        # if inMapRect(CENTER_GRID_SPACE, gridPosition) == False:
        #     raise Exception('position over the grid of playable map')
        if map.grid[coords.getTuple()] == CELL_TYPE.CROSSROAD:
            return nodes[coords.getTuple()]

        directionsList = list()
        for direction in [DIRECTIONS.UP, DIRECTIONS.DOWN, DIRECTIONS.RIGHT, DIRECTIONS.LEFT]:
            newCoords = coords.getOffsetted(direction, 1)
            if map.grid[newCoords.getTuple()] != CELL_TYPE.WALL:
                directionsList.append(direction)

        rayLength = 1
        while True:
            for direction in directionsList:
                newCoords = coords.getOffsetted(direction, rayLength)
                if map.grid[newCoords.getTuple()] == CELL_TYPE.CROSSROAD:
                    return nodes[newCoords.getTuple()]
            rayLength += 1

    @staticmethod
    def getOffsetFromNearestNode(node: Node, coords: Coords):
        direction = MapNavigationFuncs.getDirectionToNeighbour(node.coords, coords)
        offset = NodesNavigationFuncs.getLengthBetweenNeighbors(node.coords, coords)
        return direction, offset

    @staticmethod
    def getDirectionAndLengthBetweenNodes(fromNode: Node, toNode: Node):
        direction = MapNavigationFuncs.getDirectionToNeighbour(fromNode.coords, toNode.coords)
        offset = NodesNavigationFuncs.getLengthBetweenNeighbors(fromNode.coords, toNode.coords)
        return direction, offset

    @staticmethod
    def isBetweenNeighborNodes(firstNode: Node, secondNode: Node, point: Coords):
        if firstNode.coords.x == secondNode.coords.x:
            if point.x != firstNode.coords.x:
                return False
            if (point.y >= firstNode.coords.y and point.y <= secondNode.coords.y) or \
                    (point.y >= secondNode.coords.y and point.y <= firstNode.coords.y):
                return True
            return False
        elif firstNode.coords.y == secondNode.coords.y:
            if point.y != firstNode.coords.y:
                return False
            if (point.x >= firstNode.coords.x and point.x <= secondNode.coords.x) or \
                    (point.x >= secondNode.coords.x and point.x <= firstNode.coords.x):
                return True
            return False
        raise NotImplementedError

    @staticmethod
    def getLengthBetweenNeighbors(firstCoords: Coords, secondCoords: Coords):
        x_offset = fabs(firstCoords.x - secondCoords.x)
        y_offset = fabs(firstCoords.y - secondCoords.y)
        return int(max(x_offset, y_offset))


class MapNavigationFuncs():
    @staticmethod
    def getDistanceToTarget(point: Coords, target: Coords):
        # c = sqrt(a^2 + b^2)
        a = point.x - target.x
        b = point.y - target.y
        c = sqrt(pow(a, 2) + pow(b, 2))
        # c = pow(a, 2) + pow(b, 2)
        return c

    @staticmethod
    def getDirectionToNeighbour(startPoint: Coords, endPoint: Coords):
        if endPoint.y < startPoint.y and endPoint.x == startPoint.x:
            return DIRECTIONS.UP
        if endPoint.y > startPoint.y and endPoint.x == startPoint.x:
            return DIRECTIONS.DOWN
        if endPoint.x > startPoint.x and endPoint.y == startPoint.y:
            return DIRECTIONS.RIGHT
        if endPoint.x < startPoint.x and endPoint.y == startPoint.y:
            return DIRECTIONS.LEFT

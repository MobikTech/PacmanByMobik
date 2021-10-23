from math import sqrt, pow

from Scripts.MVC.Model.Navigation.Coords import Coords
from Scripts.MVC.Model.Navigation.Map import Map
from Scripts.MVC.Model.Navigation.Nodes import Node
from Scripts.MVC.Controller.Common.Constants import *



class Algorithmes():

    @staticmethod
    def __bfs(startNode: Node, targetNode: Node):
        queue = [(startNode, [startNode])]
        visited = list()
        while queue:
            node, path = queue.pop(0)
            visited.append(node)
            if node == targetNode:
                return path

            for nodeAndDistance in node.neighbourNodesAndDistances.values():
                if nodeAndDistance == None:
                    continue
                if visited.__contains__(nodeAndDistance[0]) == False:
                    newPath = path.copy()
                    newPath.append(nodeAndDistance[0])
                    queue.append((nodeAndDistance[0], newPath))

    @staticmethod
    def __aStar(startNode: Node, targetNode: Node):
        path = list()
        path.append(startNode)
        while path[-1] != targetNode:
            currentNode = path[-1]
            bestDirection = None

            for direction in currentNode.neighborsNodeInfo.keys():
                neighbourInfo = currentNode.neighborsNodeInfo[direction]
                if neighbourInfo == None:
                    continue
                if path.__contains__(neighbourInfo.node):
                    continue
                if neighbourInfo.node == targetNode:
                    path.append(targetNode)
                    return path
                if bestDirection == None:
                    bestDirection = direction
                    continue
                if Algorithmes.__heuristicFunction(path[-1], direction, targetNode) < \
                        Algorithmes.__heuristicFunction(path[-1], bestDirection, targetNode):
                    bestDirection = direction
            path.append(currentNode.neighborsNodeInfo[bestDirection].node)

    @staticmethod
    def __heuristicFunction(currentNode: Node, direction: int, target: Node):
        if currentNode.neighborsNodeInfo[direction] == None:
            return None
        totalDistance = 0
        totalDistance += currentNode.neighborsNodeInfo[direction].distanceToIt
        totalDistance += MapNavigationFuncs.getDistanceToTarget(currentNode.neighborsNodeInfo[direction].node.coords,
                                                                target.coords)
        return totalDistance

    @staticmethod
    def getPathToTarget(algorithmType: int, startPoint: Coords, target: Coords, map):
        directionsPath = list()

        startNearestNeighbour = NodesNavigationFuncs.findNearestNodeTo(startPoint, map)
        targetNearestNeighbour = NodesNavigationFuncs.findNearestNodeTo(target, map)

        nodesPath = None
        if algorithmType == SEARCH_ALGORITHMES.BFS:
            nodesPath = Algorithmes.__bfs(startNearestNeighbour, targetNearestNeighbour)
        elif algorithmType == SEARCH_ALGORITHMES.ASTAR:
            nodesPath = Algorithmes.__aStar(startNearestNeighbour, targetNearestNeighbour)

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
    def findNearestNodeTo(coords: Coords, map: Map):
        nodes = map.nodesDictionary
        # if inMapRect(CENTER_GRID_SPACE, gridPosition) == False:
        #     raise Exception('position over the grid of playable map')
        if map.grid[coords.getTuple()] == CELL_TYPE.CROSSROAD:
            return nodes[coords.getTuple()]

        rayLength = 1
        directionsList = list()
        for direction in [DIRECTIONS.UP, DIRECTIONS.DOWN, DIRECTIONS.RIGHT, DIRECTIONS.LEFT]:
            newCoords = coords.getOffsetted(direction, rayLength)
            if map.grid[newCoords.getTuple()] != CELL_TYPE.WALL:
                directionsList.append(direction)


        while True:
            for direction in directionsList:
                newCoords = coords.getOffsetted(direction, rayLength)
                if map.grid[newCoords.getTuple()] == CELL_TYPE.CROSSROAD:
                    return nodes[newCoords.getTuple()]
            rayLength += 1

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



class MapNavigationFuncs():
    @staticmethod
    def getDistanceToTarget(point: Coords, target: Coords):
        # c = sqrt(a^2 + b^2)
        a = point.x - target.x
        b = point.y - target.y
        c = sqrt(pow(a, 2) + pow(b, 2))
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

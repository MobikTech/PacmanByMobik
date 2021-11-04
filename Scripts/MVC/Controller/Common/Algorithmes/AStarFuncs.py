from Scripts.MVC.Controller.Common.Algorithmes.Algorithmes import MapNavigationFuncs, NodesNavigationFuncs
from Scripts.MVC.Model.Navigation.Nodes import Node


class AStarFuncs():

    @staticmethod
    def aStar(startNode: Node, targetNode: Node):
        openList = []
        closedList = []

        nodesInfo = dict()

        openList.append(startNode)
        nodesInfo[startNode] = AlgNodeInfo(0, 0, None)

        while len(openList) > 0:

            # Get the current node
            currentNode = AStarFuncs.__findMinF(openList, nodesInfo)

            closedList.append(currentNode)
            openList.remove(currentNode)

            # Found the goal
            if currentNode == targetNode:
                path = AStarFuncs.__makePath(targetNode, startNode, nodesInfo)
                path.reverse()
                return path

            directions = NodesNavigationFuncs.getNodeDirections(currentNode)
            for direction in directions:
                neighbour = currentNode.neighborsNodeInfo[direction].node

                if closedList.__contains__(neighbour):
                    continue
                if not openList.__contains__(neighbour):
                    openList.append(neighbour)
                    g = AStarFuncs.__getG(neighbour, currentNode, startNode, nodesInfo)
                    h = AStarFuncs.__getH(neighbour, targetNode)
                    nodesInfo[neighbour] = AlgNodeInfo(g=g,
                                                       h=h,
                                                       parent=currentNode)
                else:
                    newG = AStarFuncs.__getG(neighbour, currentNode, startNode, nodesInfo)
                    if newG < nodesInfo[neighbour].g:
                        nodesInfo[neighbour].g = newG
                        nodesInfo[neighbour].parent = currentNode


    @staticmethod
    def __getG(node: Node,
               parent: Node,
               startNode: Node,
               nodesInfo: dict[Node]):
        path = []
        path.append(node)
        currentNode = parent
        while currentNode != startNode:
            path.append(currentNode)
            currentNode = nodesInfo[currentNode].parent
        path.append(startNode)
        g = AStarFuncs.__getPathLength(path)
        return g

    @staticmethod
    def __getH(node: Node, target: Node):
        h = MapNavigationFuncs.getDistanceToTarget(node.coords,
                                                   target.coords)
        return h

    @staticmethod
    def __findMinF(openList: list[Node], nodesInfo: dict[Node]):
        minFNode = openList[0]
        for node in openList:
            if nodesInfo[node].getF() < nodesInfo[minFNode].getF():
                minFNode = node
        return minFNode

    @staticmethod
    def __makePath(node: Node, startNode: Node, nodesInfo: dict[Node]):
        path = []
        currentNode = node
        while currentNode != startNode:
            path.append(currentNode)
            currentNode = nodesInfo[currentNode].parent
        path.append(startNode)
        return path


    @staticmethod
    def __getPathLength(path: list[Node]):
        if len(path) == 1:
            return 0
        totalLength = 0
        currentIndex = 0
        while currentIndex != len(path) - 1:
            direction = MapNavigationFuncs.getDirectionToNeighbour(path[currentIndex].coords,
                                                                   path[currentIndex + 1].coords)
            totalLength += path[currentIndex].neighborsNodeInfo[direction].distanceToIt
            currentIndex += 1
        return totalLength


class AlgNodeInfo():
    def __init__(self, g, h, parent):
        self.g = g
        self.h = h
        self.parent = parent

    def getF(self):
        return self.g + self.h

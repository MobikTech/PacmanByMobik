from Scripts.Common.CommonFuncs import *
from Scripts.Map.Node import Node


def bfs(startNode: Node, targetNode: Node, color, surface):
    queue = [(startNode, [startNode])]
    visited = list()
    while queue:
        node, path = queue.pop(0)
        visited.append(node)
        if node == targetNode:
            DrawPath(path, color, surface)
            return path

        for nodeAndDistance in node.neighbourNodesAndDistances.values():
            if nodeAndDistance == None:
                continue
            if visited.__contains__(nodeAndDistance[0]) == False:
                newPath = path.copy()
                newPath.append(nodeAndDistance[0])
                queue.append((nodeAndDistance[0], newPath))


# refactor
def dfs(startNode: Node, targetNode: Node, color, screen, map):
    stack = [(startNode, [startNode])]
    while stack:
        (node, path) = stack.pop()
        node.isVisited = True
        if node == targetNode:
            DrawPath(path, color, screen)
            map.resetVisited()
            return path

        if node.topN != None and node.topN.isVisited == False:
            newPath = path.copy()
            newPath.append(node.topN)
            stack.append((node.topN, newPath))
        if node.rightN != None and node.rightN.isVisited == False:
            newPath = path.copy()
            newPath.append(node.rightN)
            stack.append((node.rightN, newPath))
        if node.bottomN != None and node.bottomN.isVisited == False:
            newPath = path.copy()
            newPath.append(node.bottomN)
            stack.append((node.bottomN, newPath))
        if node.leftN != None and node.leftN.isVisited == False:
            newPath = path.copy()
            newPath.append(node.leftN)
            stack.append((node.leftN, newPath))
    map.resetVisited()


def ucs(startNode: Node, targetNode: Node, color, screen, map):
    queue = [(startNode, [startNode], 0)]
    while queue:
        (node, path, cost) = queue.pop(0)
        node.distanceToThis = cost
        node.isVisited = True
        if node == targetNode:
            DrawPath(path, color, screen)
            map.resetDistances()
            return path

        if node.topN != None:
            if node.topN.distanceToThis == None or cost + node.toTopDistance < node.topN.distanceToThis:
                newPath = path.copy()
                newPath.append(node.topN)
                queue.append((node.topN, newPath, cost + node.toTopDistance))

        if node.rightN != None:
            if node.rightN.distanceToThis == None or cost + node.toRightDistance < node.rightN.distanceToThis:
                newPath = path.copy()
                newPath.append(node.rightN)
                queue.append((node.rightN, newPath, cost + node.toRightDistance))

        if node.bottomN != None:
            if node.bottomN.distanceToThis == None or cost + node.toBottomDistance < node.bottomN.distanceToThis:
                newPath = path.copy()
                newPath.append(node.bottomN)
                queue.append((node.bottomN, newPath, cost + node.toBottomDistance))

        if node.leftN != None:
            if node.leftN.distanceToThis == None or cost + node.toLeftDistance < node.leftN.distanceToThis:
                newPath = path.copy()
                newPath.append(node.leftN)
                queue.append((node.leftN, newPath, cost + node.toLeftDistance))
    map.resetDistances()


# def chooseAlgorithm(algorithm, startNode: Node, targetNode: Node, color, screen, map):
#     if algorithm == ALGORITHMES.BFS:
#         bfs(startNode, targetNode, color, screen, map)
#     elif algorithm == ALGORITHMES.DFS:
#         dfs(startNode, targetNode, color, screen, map)
#     elif algorithm == ALGORITHMES.UCS:
#         ucs(startNode, targetNode, color, screen, map)
#
#
# def changeAlgorithm(currAlgorithm):
#     maxAlg = ALGORITHMES.UCS
#     currAlgorithm += 1
#     if currAlgorithm == maxAlg + 1:
#         currAlgorithm = 0
#     return currAlgorithm
#
#
# def strOfAlg(currAlgorithm):
#     if currAlgorithm == ALGORITHMES.BFS:
#         return ALGORITHMES.BFS_STR
#     elif currAlgorithm == ALGORITHMES.DFS:
#         return ALGORITHMES.DFS_STR
#     elif currAlgorithm == ALGORITHMES.UCS:
#         return ALGORITHMES.UCS_STR

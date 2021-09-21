import pygame
from Constants import *
from CommonFuncs import *
from typing import Tuple
from Timer import Timer
from Node import Node

def bfs(startNode: Node, targetNode: Node, color, screen, map):
    queue = [(startNode, [startNode])]
    while queue:
        (node, path) = queue.pop(0)
        node.isVisited = True
        if node == targetNode:
            DrawPath(path, color, screen)
            map.resetVisited()
            return path

        if node.topN != None and node.topN.isVisited == False:
            newPath = path.copy()
            newPath.append(node.topN)
            queue.append((node.topN, newPath))
        if node.rightN != None and node.rightN.isVisited == False:
            newPath = path.copy()
            newPath.append(node.rightN)
            queue.append((node.rightN, newPath))
        if node.bottomN != None and node.bottomN.isVisited == False:
            newPath = path.copy()
            newPath.append(node.bottomN)
            queue.append((node.bottomN, newPath))
        if node.leftN != None and node.leftN.isVisited == False:
            newPath = path.copy()
            newPath.append(node.leftN)
            queue.append((node.leftN, newPath))
    map.resetVisited()

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
    queue = [(startNode, [startNode])]
    while queue:
        (node, path) = queue.pop(0)
        node.isVisited = True
        if node == targetNode:
            DrawPath(path, color, screen)
            map.resetVisited()
            return path

        priorityList = []
        if node.topN != None and node.topN.isVisited == False:
            newPath = path.copy()
            newPath.append(node.topN)
            priorityList.append((node.topN, node.toTopDistance, newPath))
            # queue.append((node.topN, newPath))
        if node.rightN != None and node.rightN.isVisited == False:
            newPath = path.copy()
            newPath.append(node.rightN)
            priorityList.append((node.rightN, node.toRightDistance, newPath))
            # queue.append((node.rightN, newPath))
        if node.bottomN != None and node.bottomN.isVisited == False:
            newPath = path.copy()
            newPath.append(node.bottomN)
            priorityList.append((node.bottomN, node.toBottomDistance, newPath))
            # queue.append((node.bottomN, newPath))
        if node.leftN != None and node.leftN.isVisited == False:
            newPath = path.copy()
            newPath.append(node.leftN)
            priorityList.append((node.leftN, node.toLeftDistance, newPath))
            # queue.append((node.leftN, newPath))
        priorityList.sort(key=lambda x: x[1])
        for nodeInfo in priorityList:
            queue.append((nodeInfo[0], nodeInfo[2]))
    map.resetVisited()

def chooseAlgorithm(algorithm, startNode: Node, targetNode: Node, color, screen, map):
    if algorithm == BFS:
        bfs(startNode, targetNode, color, screen, map)
    elif algorithm == DFS:
        dfs(startNode, targetNode, color, screen, map)
    elif algorithm == UCS:
        ucs(startNode, targetNode, color, screen, map)

def changeAlgorithm(currAlgorithm):
    maxAlg = UCS
    currAlgorithm += 1
    if currAlgorithm == maxAlg + 1:
        currAlgorithm = 0
    return currAlgorithm

def strOfAlg(currAlgorithm):
    if currAlgorithm == BFS:
        return BFS_STR
    elif currAlgorithm == DFS:
        return DFS_STR
    elif currAlgorithm == UCS:
        return UCS_STR
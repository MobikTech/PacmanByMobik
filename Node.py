import pygame
from CommonFuncs import *
# from Map import Map
# from Player import Player

class Node(object):
    def __init__(self, gridPos: Tuple[int, int]):
        self.gridPosition = gridPos
        self.topN = None
        self.rightN = None
        self.bottomN = None
        self.leftN = None
        self.isVisited = False

        self.toTopDistance = None
        self.toRightDistance = None
        self.toBottomDistance = None
        self.toLeftDistance = None



    # def addToPath(self, node):
    #     self.path.append(node)
    #     return self
    #
    # def clearPath(self):
    #     self.path = []

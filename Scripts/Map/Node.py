from Scripts.Common.CommonFuncs import *
# from Map import Map
# from Player import Player

class Node(object):
    def __init__(self, gridPosition: Tuple[int, int]):
        self.gridPosition = gridPosition
        self.neighbourNodes = dict([(DIRECTIONS.UP, None),
                                   (DIRECTIONS.DOWN, None),
                                   (DIRECTIONS.RIGHT, None),
                                   (DIRECTIONS.LEFT, None)])

        # self.topN = None
        # self.rightN = None
        # self.bottomN = None
        # self.leftN = None

        # self.isVisited = False

        # self.toTopDistance = None
        # self.toRightDistance = None
        # self.toBottomDistance = None
        # self.toLeftDistance = None

        # self.distanceToThis = None


        # self.neighbourNodesDistances = dict([(DIRECTIONS.UP, None),
        #                             (DIRECTIONS.DOWN, None),
        #                             (DIRECTIONS.RIGHT, None),
        #                             (DIRECTIONS.LEFT, None)])


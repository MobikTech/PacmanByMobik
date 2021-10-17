# from Map import Map
# from Player import Player

class Node(object):
    def __init__(self, gridPosition: Tuple[int, int]):
        self.gridPosition = gridPosition
        self.neighbourNodesAndDistances = dict([(DIRECTIONS.UP, None),
                                                (DIRECTIONS.DOWN, None),
                                                (DIRECTIONS.RIGHT, None),
                                                (DIRECTIONS.LEFT, None)])
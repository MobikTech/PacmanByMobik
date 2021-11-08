from Scripts.MVC.Controller.Common.Constants import DIRECTIONS
from Scripts.MVC.Model.Navigation.Coords import Coords


class Node(object):
    def __init__(self, position: tuple[int, int]):
        self.coords = Coords(position)
        self.neighborsNodeInfo = dict([(DIRECTIONS.UP, None),
                                       (DIRECTIONS.DOWN, None),
                                       (DIRECTIONS.RIGHT, None),
                                       (DIRECTIONS.LEFT, None)])

    def __str__(self):
        return '{0} => [{1}  {2}  {3}  {4}]'.format(self.coords.__str__(),
                                                    self.neighborsNodeInfo[DIRECTIONS.UP],
                                                    self.neighborsNodeInfo[DIRECTIONS.RIGHT],
                                                    self.neighborsNodeInfo[DIRECTIONS.DOWN],
                                                    self.neighborsNodeInfo[DIRECTIONS.LEFT])

    def __copy__(self):
        return Node(self.coords.__copy__())


class NodeInfo():
    def __init__(self, node: Node, distance: int):
        self.node = node
        self.distanceToIt = distance

    def __str__(self):
        return '{0}:{1}'.format(self.node.coords.__str__(), self.distanceToIt)

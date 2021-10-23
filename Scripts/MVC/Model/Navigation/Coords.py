from Scripts.MVC.Controller.Common.Constants import *


class Coords():
    def __init__(self, position=None, coords = None):
        if position:
            self.x = position[0]
            self.y = position[1]
        elif coords:
            self.x = coords.x
            self.y = coords.y

    def offsetTo(self, direction, distance):
        vector = Coords.directionToNormalizedVector(direction)
        offset = (vector[0] * distance, vector[1] * distance)
        self.x += offset[0]
        self.y += offset[1]

    def toCenter(self):
        from Scripts.MVC.Controller.Common.CommonClasses import CoordsConverter
        center = CoordsConverter.gridToWorld(CoordsConverter.worldToGrid(self))
        self.x = center.x
        self.y = center.y

    def getTuple(self):
        return (self.x, self.y)

    def getOffsetted(self, direction, distance):
        vector = Coords.directionToNormalizedVector(direction)
        offsetted = (self.x + vector[0] * distance, self.y + vector[1] * distance)
        return Coords(offsetted)

    def __str__(self):
        return '({0}, {1})'.format(self.x, self.y)

    def __copy__(self):
        return Coords((self.x, self.y))

    @staticmethod
    def directionToNormalizedVector(direction: str):
        if direction == DIRECTIONS.UP:
            return VECTORS.VECTOR_UP
        elif direction == DIRECTIONS.DOWN:
            return VECTORS.VECTOR_DOWN
        elif direction == DIRECTIONS.RIGHT:
            return VECTORS.VECTOR_RIGHT
        elif direction == DIRECTIONS.LEFT:
            return VECTORS.VECTOR_LEFT
        raise Exception("Was received incorrect direction")

    # @staticmethod
    # def inMap(coords: Coords):
    #     pass
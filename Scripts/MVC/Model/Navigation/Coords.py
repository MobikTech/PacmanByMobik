from Scripts.MVC.Model.Common.DirectionFuncs import directionToNormalizedVector


class Coords():
    def __init__(self, coords=(0, 0)):
        self.x = coords[0]
        self.y = coords[1]

    def offsetTo(self, direction, distance):
        vector = directionToNormalizedVector(direction)
        offset = (vector[0] * distance, vector[1] * distance)
        self.x += offset[0]
        self.y += offset[1]

    def getTuple(self):
        return (self.x, self.y)

    def getOffsetted(self, direction, distance):
        vector = directionToNormalizedVector(direction)
        offsetted = (vector[0] * distance, vector[1] * distance)
        return offsetted

    def __str__(self):
        return '({0}, {1})'.format(self.x, self.y)
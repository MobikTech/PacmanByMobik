import pygame
from Scripts.MVC.Controller.Common.CommonClasses import CoordsConverter
from Scripts.MVC.Controller.Common.Constants import CELL_TYPE
from Scripts.MVC.Model.Navigation.Coords import Coords


class PathDrawer():

    @staticmethod
    def DrawPath(path: list[str],
                 startPoint: Coords,
                 targetPoint: Coords,
                 grid: dict[tuple[int, int]],
                 color,
                 surface):
        POINT_SIZE = 6
        currentCoords = startPoint
        currentDirectionIndex = 0
        currentDirection = path[currentDirectionIndex]

        while currentCoords.getTuple() != targetPoint.getTuple():

            pygame.draw.circle(surface, color, CoordsConverter.gridToWorld(currentCoords).getTuple(), POINT_SIZE)
            if grid[currentCoords.getTuple()] == CELL_TYPE.CROSSROAD:
                currentDirectionIndex += 1
                currentDirection = path[currentDirectionIndex]
            # and \
            #                     currentCoords.getTuple() != targetPoint.getTuple()
            currentCoords = currentCoords.getOffsetted(currentDirection, 1)
        pygame.draw.circle(surface, color, CoordsConverter.gridToWorld(currentCoords).getTuple(), POINT_SIZE)


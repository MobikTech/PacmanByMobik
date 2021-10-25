import pygame
from Scripts.MVC.Controller.Common.CommonClasses import CoordsConverter
from Scripts.MVC.Controller.Common.Constants import *
from Scripts.MVC.Model.Navigation.Coords import Coords


class PathDrawer():

    @staticmethod
    def drawPath(path: list[str],
                 startPoint: Coords,
                 targetPoint: Coords,
                 grid: dict[tuple[int, int]],
                 color,
                 surface):
        if path == None:
            return
        POINT_SIZE = 6
        currentCoords = startPoint
        currentDirectionIndex = 0
        currentDirection = path[currentDirectionIndex]

        while currentCoords.getTuple() != targetPoint.getTuple():

            pygame.draw.circle(surface, color, CoordsConverter.gridToWorld(currentCoords).getTuple(), POINT_SIZE)
            if grid[currentCoords.getTuple()] == CELL_TYPE.CROSSROAD and \
                    currentCoords != startPoint:
                currentDirectionIndex += 1
                currentDirection = path[currentDirectionIndex]
            # and \
            #                     currentCoords.getTuple() != targetPoint.getTuple()
            currentCoords = currentCoords.getOffsetted(currentDirection, 1)
        pygame.draw.circle(surface, color, CoordsConverter.gridToWorld(currentCoords).getTuple(), POINT_SIZE)

    @staticmethod
    def getGhostColor(ghostType):
        if ghostType == GHOST_TYPE.RIKKO:
            return COLORS.RED
        elif ghostType == GHOST_TYPE.PINKY:
            return COLORS.PINK
        elif ghostType == GHOST_TYPE.GREENKY:
            return COLORS.GREEN
        elif ghostType == GHOST_TYPE.CLYNE:
            return COLORS.YELLOW
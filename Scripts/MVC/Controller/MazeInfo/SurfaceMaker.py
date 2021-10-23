from pygame import Surface
from pygame.sprite import Group
from Scripts.MVC.Controller.Common.Constants import *
from Scripts.MVC.Model.Navigation.Coords import Coords
from Scripts.MVC.View.SpriteEntity import SpriteEntity




class SurfaceMaker():

    @staticmethod
    def getSurface(grid: dict[tuple[int, int]]):
        surface = Surface(SCREEN.SCREEN_SIZE)
        cellSpriteEntities = dict()
        cellSpritesGroup = Group()
        for position in grid.keys():
            cellSpriteType = SurfaceMaker.getCellSpriteType(grid[position])
            cellSpriteEntities[position] = SpriteEntity(cellSpriteType,
                                                        cellSpritesGroup,
                                                        Coords(position),
                                                        str(SurfaceMaker.getSpriteFilePath(cellSpriteType)))
            cellSpritesGroup.draw(surface)
        return surface

    @staticmethod
    def getSpriteFilePath(cellSpriteType: int):
        path = MAIN_DIRECTORY + '\Sprites\CellSprites'
        if cellSpriteType == SPRITE_TYPES.CELL_ROAD:
            return path + '\CellRoad.png'
        if cellSpriteType == SPRITE_TYPES.CELL_CROSSROAD:
            return path + '\CellCrossroad.png'
        # if cellSpriteType in [SPRITE_TYPES.CELL_ROAD, SPRITE_TYPES.CELL_CROSSROAD]:
        #     return path + '\CellRoad.png'
        if cellSpriteType == SPRITE_TYPES.CELL_WALL:
            return path + '\CellWall.png'
        if cellSpriteType == SPRITE_TYPES.CELL_DOOR:
            return path + '\CellGhostDoor.png'
        raise NotImplementedError

    @staticmethod
    def getCellSpriteType(type: str):
        if type in [CELL_TYPE.WALL]:
            return SPRITE_TYPES.CELL_WALL
        if type in [CELL_TYPE.ROAD, CELL_TYPE.PACMAN_START_POSITION, CELL_TYPE.REST_SPACE]:
            return SPRITE_TYPES.CELL_ROAD
        if type in [CELL_TYPE.GHOSTS_START_POSITION]:
            return SPRITE_TYPES.CELL_DOOR
        if type in [CELL_TYPE.CROSSROAD]:
            return SPRITE_TYPES.CELL_CROSSROAD
        raise NotImplementedError

    @staticmethod
    def getCellType(color: tuple[int, int, int, int]):
        if color == (0, 0, 255, 255):
            return CELL_TYPE.WALL
        elif color == (0, 0, 0, 255):
            return CELL_TYPE.ROAD
        elif color == (0, 255, 0, 255):
            return CELL_TYPE.CROSSROAD
        elif color == (255, 255, 0, 255):
            return CELL_TYPE.PACMAN_START_POSITION
        elif color == (255, 0, 255, 255):
            return CELL_TYPE.GHOSTS_START_POSITION
        elif color == (255, 255, 255, 255):
            return CELL_TYPE.REST_SPACE

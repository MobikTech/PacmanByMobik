from pygame import Surface
from pygame.sprite import Sprite, Group

from Scripts.Common.CommonFuncs import *
from Scripts.Map.Node import Node
from Scripts.Common.CoordsConverter import *


# region Map-making inctructions:
# yellow (255, 255, 0, 255) - pacman start point
# pink (255, 0, 255, 255) - ghosts spawn point
# black (0, 0, 0, 255) - roads
# green (0, 255, 0, 255) - crossroads
# blue (0, 0, 255, 255) - walls
# white (255, 255, 255, 255) - non-active space(for example, for UI)
# red (255, 0, 0, 255) - door for spirit house
# endregion

class Map(object):
    def __init__(self, colorMap: list[list[tuple[int, int, int, int]]]):
        self.colorMap = colorMap

        # refactor: add random generation of background image
        self.background = getSurface(colorMap, SCREEN_SIZE)
        self.background.get_rect().center = SCREEN_CENTER

        self.playerStartWorldPosition = None
        self.ghostsStartWorldPosition = None
        self.nodeDictionary = dict()
        self.roadCoordsList = list()
        self.crossroadCoordsList = self.nodeDictionary.keys()

        self._scanColorMap()
        # self._defineNodesNeighbours()

    def _scanColorMap(self):
        for x in range(GRID_COLUMNS_COUNT):
            for y in range(GRID_ROWS_COUNT):
                currentCellColor = self.colorMap[x][y]
                if currentCellColor == CELL_TYPE.MAP_PACMAN_START_POSITION:
                    self.playerStartWorldPosition = gridToWorld(x, y)
                elif currentCellColor == CELL_TYPE.MAP_GHOSTS_START_POSITION:
                    self.ghostsStartWorldPosition = gridToWorld(x, y)
                elif currentCellColor == CELL_TYPE.MAP_ROAD:
                    self.roadCoordsList.append((x, y))
                elif currentCellColor == CELL_TYPE.MAP_CROSSROAD:
                    self.nodeDictionary[(x, y)] = Node((x, y))

    def _defineNodesNeighbours(self):
        for node in self.nodeDictionary.values():
            for direction in node.neighbourNodesAndDistances.keys():
                x, y = nextPoint = getOffsettedPoint(node.gridPosition, direction, 1)
                if self.colorMap[x][y] in (CELL_TYPE.MAP_ROAD,
                                           CELL_TYPE.MAP_CROSSROAD,
                                           CELL_TYPE.MAP_PACMAN_START_POSITION):
                    currentDistance = 1
                    while self.colorMap[x][y] != CELL_TYPE.MAP_CROSSROAD:
                        x, y = nextPoint = getOffsettedPoint(nextPoint, direction, 1)
                        currentDistance += 1
                    node.neighbourNodesAndDistances[direction] = (
                        self.nodeDictionary[nextPoint], currentDistance)
                    # node.neighbourNodesDistances[direction] = currentDistance


def getSurface(colorMap: list[list[tuple[int, int, int, int]]],
               screenSize: Tuple[int, int]):
    surface = Surface(screenSize)
    cellSpriteEntities = dict()
    cellSpritesGroup = Group()
    for x in range(len(colorMap[0])):
        for y in range(len(colorMap)):
            cellSpriteType = getCellSpriteType(colorMap[x][y])
            cellSpriteEntities[(x, y)] = SpriteEntity(cellSpriteType,
                                                      cellSpritesGroup,
                                                      gridToWorld(x, y),
                                                      str(getCellSpritePath(cellSpriteType)))

    cellSpritesGroup.draw(surface)
    return surface


def getCellSpriteType(color: Tuple[int, int, int, int]):
    if color in [CELL_TYPE.MAP_WALL]:
        return SPRITE_TYPES.CELL_WALL
    if color in [CELL_TYPE.MAP_ROAD, CELL_TYPE.MAP_PACMAN_START_POSITION, CELL_TYPE.MAP_REST_SPACE]:
        return SPRITE_TYPES.CELL_ROAD
    if color in [CELL_TYPE.MAP_GHOSTS_START_POSITION]:
        return SPRITE_TYPES.CELL_DOOR
    if color in [CELL_TYPE.MAP_CROSSROAD]:
        return SPRITE_TYPES.CELL_CROSSROAD
    raise NotImplementedError


def getCellSpritePath(cellSpriteType: int):
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

from pygame.constants import KEYDOWN, K_ESCAPE, QUIT
from pygame.image import load

from Scripts.Old.Common.SearchAlgorithmes import *
from Scripts.MVC.Model.Entities.Coin import *
from Scripts.MVC.Model.Entities.Ghost import *
from Scripts.MVC.Model.Entities.Player import Player
from Scripts.Old.Map.Map import Map
from Scripts.Old.Other.TextObject import TextObject


class GameController(object):
    HP_MARKER_POSITION = (CENTER_WORLD_SPACE[0] - CELL_SIZE * 11, CENTER_WORLD_SPACE[1] + CELL_SIZE * 3)
    SCORE_MARKER_POSITION = (CENTER_WORLD_SPACE[0], CENTER_WORLD_SPACE[1] + CELL_SIZE * 3)
    GAME_OVER_MARKER_POSITION = (CENTER_WORLD_SPACE[0], CENTER_WORLD_SPACE[1] + CELL_SIZE * 6)

    GAME_OVER_HP_VALUE = 0
    GAME_OVER_COIN_COUNT = -1

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.gameOver = False

        # self.mazeGenerator = MazeGenerator(COLUMNS_COUNT, ROWS_COUNT)
        self.map1 = Map(getColorMap(load(MAIN_DIRECTORY + '\Sprites\pacman_map_1_31x31.png')))
        # self.map2 = Map(getColorMap(load(MAIN_DIRECTORY + '\Sprites\pacman_map_2_31x31.png')),
        #                 load(MAIN_DIRECTORY + '\Sprites\pacman_map_2_651x651.png'))

        # self.currentMap = Map(self.mazeGenerator.colorMap)
        self.currentMap = self.map1

        self.entitiesSpriteGroup = Group()
        self.player = Player(self.entitiesSpriteGroup,
                             self.currentMap.playerStartWorldPosition,
                             self.currentMap.colorMap)
        self.ghostsDict = None
        self.coinsMap = dict()
        self.layer1 = self.currentMap.background
        self.ghostsCanMove = True
        self.ui = dict()

        self.playerTargetPosition = getRandomCoinPosition(self.coinsMap)
        self.currentPath = None

        self.currentDrawingPath = None
        self.startPlayerPosition = None
        self.currentDirectionIndex = 0
        self.lastCrossroad = None

    def start(self):
        self._spawnCoins()
        self.ghostsDict = {MOVABLE_ENTITIES.GHOST_RIKKO: self._createGhost(MOVABLE_ENTITIES.GHOST_RIKKO),
                           MOVABLE_ENTITIES.GHOST_GREENKY: self._createGhost(MOVABLE_ENTITIES.GHOST_GREENKY),
                           MOVABLE_ENTITIES.GHOST_PINKY: self._createGhost(MOVABLE_ENTITIES.GHOST_PINKY),
                           MOVABLE_ENTITIES.GHOST_CLYNE: self._createGhost(MOVABLE_ENTITIES.GHOST_CLYNE)}
        self.ui = {
            UI_TEXT_OBJECTS.HP_MARKER: TextObject(32, GameController.HP_MARKER_POSITION, "hp: " + str(self.player.hp)),
            UI_TEXT_OBJECTS.SCORE_MARKER: TextObject(32, GameController.SCORE_MARKER_POSITION,
                                                     "score: " + str(self.player.score)),
            UI_TEXT_OBJECTS.GAME_OVER_MARKER: TextObject(32, GameController.GAME_OVER_MARKER_POSITION, 'Game Over')}

    def update(self):
        if self.gameOver == True:
            self._endGame()
        else:
            self.clock.tick(FPS)
            self._eventHandler()
            self.stopGhosts()

            self._tryCheckPlayerGhostsCollisions()
            self._tryCheckPlayerCoinsCollisions()
            self.render()
            self._tryStopGame()

    def render(self):
        self._clearScreen()
        self.entitiesSpriteGroup.draw(self.layer1)
        # self.algorithmHandler()
        self._tryMoveGhosts()
        self._tryMovePlayer()
        self._updateUI()
        self.screen.blit(self.layer1, SCREEN_START_POINT)

    def _eventHandler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

    def _clearScreen(self):
        self.layer1 = self.currentMap.background.copy()

    def _createGhost(self, ghostType: int):
        return Ghost(self.entitiesSpriteGroup,
                     self.currentMap.ghostsStartWorldPosition,
                     MAIN_DIRECTORY + '\Sprites\\' + getGhostName(ghostType) + '.png',
                     getGhostName(ghostType),
                     self.currentMap.colorMap,
                     getGhostColor(ghostType))

    def _tryMoveGhosts(self):
        if self.ghostsCanMove == False:
            return
        for ghost in self.ghostsDict.values():
            path = bfs(findNearestNodeTo(worldToGridT(ghost.spriteEntity.rect.center), self.currentMap),
                       findNearestNodeTo(worldToGridT(self.player.spriteEntity.rect.center), self.currentMap),
                       ghost.pathColor,
                       self.layer1)
            ghostPosition = worldToGridT(ghost.spriteEntity.rect.center)
            nodePosition = path[0].gridPosition
            if ghostPosition == nodePosition:
                direction = getDirectionToNeighbour(ghostPosition, path[1].gridPosition)
            else:
                direction = getDirectionToNeighbour(worldToGridT(ghost.spriteEntity.rect.center),
                                                    path[0].gridPosition)
            ghost.moveGhost(direction)

    def _tryMovePlayer(self):
        currentPlayerPosition = worldToGridT(self.player.spriteEntity.rect.center)
        targetPosition = self.playerTargetPosition
        directionsPath = self.currentPath
        startPlayerPosition = self.startPlayerPosition
        DirectionsPathDraw = self.currentPath
        if currentPlayerPosition == targetPosition or directionsPath == None:
            targetPosition = self.playerTargetPosition = getRandomCoinPosition(self.coinsMap)
            DirectionsPathDraw = directionsPath = self.currentDrawingPath = self.currentPath = getPathToTarget(currentPlayerPosition, targetPosition, self.currentMap)
            self.currentDirectionIndex = 0
            self.player.lastVisitedCrossroad = None
            startPlayerPosition = self.startPlayerPosition = currentPlayerPosition
        pygame.draw.circle(self.layer1, COLORS.BLUE, gridToWorldT(currentPlayerPosition), 6)
        pygame.draw.circle(self.layer1, COLORS.BLUE, gridToWorldT(targetPosition), 6)

        DrawDirectionsPath(directionsPath,
                           startPlayerPosition,
                           targetPosition,
                           self.currentMap.colorMap,
                           COLORS.BLUE,
                           self.layer1)

        colorMap = getColorMapDict(self.currentMap.colorMap)
        if inCellCenter(self.player.spriteEntity.rect.center, 2) and \
                colorMap[currentPlayerPosition] == CELL_TYPE.CROSSROAD and \
                self.player.lastVisitedCrossroad != currentPlayerPosition:
            self.player.spriteEntity.rect.center = gridToWorldT(currentPlayerPosition)
            self.player.lastVisitedCrossroad = currentPlayerPosition
            self.currentDirectionIndex += 1
            self.currentDrawingPath.pop(0)
        self.player.tryMovePlayer(directionsPath[self.currentDirectionIndex])


    def _tryCheckPlayerGhostsCollisions(self):
        for ghost in self.ghostsDict.values():
            if checkToCollision(self.player.spriteEntity, ghost.spriteEntity):
                self.player.collisionHandler(ghost.spriteEntity)
                ghost.collisionHandler(self.player.spriteEntity)
                self._respawnAll()

    def _tryCheckPlayerCoinsCollisions(self):
        currentPlayerCoords = worldToGridT(self.player.spriteEntity.rect.center)
        if self.coinsMap.__contains__(currentPlayerCoords):
            self.player.collisionHandler(self.coinsMap[currentPlayerCoords].spriteEntity)
            self.coinsMap[currentPlayerCoords].collisionHandler(self.player.spriteEntity)
            self.coinsMap.pop(currentPlayerCoords)

    def _tryStopGame(self):
        if self.player.hp <= GameController.GAME_OVER_HP_VALUE or \
                len(self.coinsMap) <= GameController.GAME_OVER_COIN_COUNT:
            self.gameOver = True

    def _spawnCoins(self):
        map = self.currentMap
        coinsSlots = map.roadCoordsList + list(map.crossroadCoordsList)
        coinsSlots.append(worldToGridT(map.playerStartWorldPosition))
        for coinSlotGridCoords in coinsSlots:
            self.coinsMap[coinSlotGridCoords] = Coin(self.entitiesSpriteGroup, gridToWorldT(coinSlotGridCoords))

    def _respawnAll(self):
        for ghost in self.ghostsDict.values():
            ghost.respawn()
        self.player.respawn()

        # pygame.time.delay(1000)

    def stopGhosts(self):
        if pygame.key.get_pressed()[pygame.K_x]:
            self.ghostsCanMove = not self.ghostsCanMove

    def _updateUI(self):
        self.ui[UI_TEXT_OBJECTS.HP_MARKER].textUpdate('hp: ' + str(self.player.hp), self.layer1)
        self.ui[UI_TEXT_OBJECTS.SCORE_MARKER].textUpdate('score: ' + str(self.player.score), self.layer1)

    def _endGame(self):
        self._clearScreen()
        self.ui[UI_TEXT_OBJECTS.GAME_OVER_MARKER].textUpdate('game over', self.layer1)
        self.ui[UI_TEXT_OBJECTS.SCORE_MARKER].textUpdate('score: ' + str(self.player.score), self.layer1)
        self.screen.blit(self.layer1, SCREEN_START_POINT)


gameController = GameController()
gameController.start()
running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
    gameController.update()
    pygame.display.flip()

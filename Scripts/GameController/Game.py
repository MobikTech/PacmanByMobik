from pygame.image import load
from Scripts.Entities.Entities.Coin import *
from Scripts.Entities.Entities.Ghost import *
from Scripts.Entities.Entities.Player import Player
from Scripts.Map.Map import Map
from Scripts.Other.TextObject import TextObject


class GameController(object):
    HP_MARKER_POSITION = (CENTER[0] - CELL_SIZE * 11, CENTER[1] + CELL_SIZE * 2)
    SCORE_MARKER_POSITION = (CENTER[0], CENTER[1] + CELL_SIZE * 2)
    GAME_OVER_MARKER_POSITION = (CENTER[0], CENTER[1] + CELL_SIZE * 5)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.gameOver = False

        self.map1 = Map(getColorMap(load(MAIN_DIRECTORY + '\Sprites\pacman_map_1_31x31.png')),
                        load(MAIN_DIRECTORY + '\Sprites\pacman_map_1_651x651.png'))
        # self.map2 = Map(getColorMap(load(MAIN_DIRECTORY + '\Sprites\pacman_map_2_31x31.png')),
        #                 load(MAIN_DIRECTORY + '\Sprites\pacman_map_2_651x651.png'))
        self.currentMap = self.map1

        self.entitiesSpriteGroup = Group()
        self.player = Player(self.entitiesSpriteGroup,
                             self.currentMap.playerStartWorldPosition,
                             self.currentMap.colorMap)
        self.ghostsDict = None
        self.coinsMap = dict()

        self.layer1 = self.currentMap.background
        self.layer2 = Surface(SCREEN_SIZE)

        self.ghostsCanMove = True
        self.ui = dict()

        # region OldFields

        # self.timer = Timer()
        # self.currentAlgorithm = BFS
        # self.timeBFS = 0
        # self.timeDFS = 0
        # self.timeUCS = 0
        #
        # self.scoreText = TextObject('Fonts/Pinmolddemo-jEaxv.otf', 32, WHITE, (CENTER[0], CENTER[1] + CELL_SIZE * 2),
        #                             "score: " + str(self.player.score))
        # self.hpText = TextObject('Fonts/Pinmolddemo-jEaxv.otf', 32, WHITE,
        #                          (CENTER[0] - CELL_SIZE * 11, CENTER[1] + CELL_SIZE * 2), "hp: " + str(self.player.hp))
        # self.gameOverText = TextObject('Fonts/Pinmolddemo-jEaxv.otf', 56, WHITE, (CENTER[0], CENTER[1] + CELL_SIZE * 5),
        #                                "game over")
        # self.currentAlgorithmText = TextObject('Fonts/Pinmolddemo-jEaxv.otf', 32, WHITE,
        #                                        (CENTER[0], CENTER[1] + CELL_SIZE * 8),
        #                                        "Algorithm: " + strOfAlg(self.currentAlgorithm))
        # self.timeBFSText = TextObject('Fonts/Pinmolddemo-jEaxv.otf', 20, WHITE, (CENTER[0], CENTER[1] + CELL_SIZE * 10),
        #                               "BFS Time: " + str(self.timeBFS))
        # self.timeDFSText = TextObject('Fonts/Pinmolddemo-jEaxv.otf', 20, WHITE, (CENTER[0], CENTER[1] + CELL_SIZE * 11),
        #                               "DFS Time: " + str(self.timeDFS))
        # self.timeUCSText = TextObject('Fonts/Pinmolddemo-jEaxv.otf', 20, WHITE, (CENTER[0], CENTER[1] + CELL_SIZE * 12),
        #                               "UCS Time: " + str(self.timeUCS))
        #
        # self.algChangeTimer = Timer()
        # self.ghostMoving = True
        # endregion

    def start(self):
        image = load('D:\\Projects\\PYTHON\\PacmanByMobik\\Sprites\\CellSprites\\CellWall.png')
        self._spawnCoins()
        self.ghostsDict = {MOVABLE_ENTITIES.GHOST_RIKKO: self._createGhost(MOVABLE_ENTITIES.GHOST_RIKKO),
                           MOVABLE_ENTITIES.GHOST_GREENKY: self._createGhost(MOVABLE_ENTITIES.GHOST_GREENKY),
                           MOVABLE_ENTITIES.GHOST_PINKY: self._createGhost(MOVABLE_ENTITIES.GHOST_PINKY),
                           MOVABLE_ENTITIES.GHOST_CLYNE: self._createGhost(MOVABLE_ENTITIES.GHOST_CLYNE)}
        self.ui = {
            UI_TEXT_OBJECTS.HP_MARKER: TextObject(32, GameController.HP_MARKER_POSITION, "hp: " + str(self.player.hp)),
            UI_TEXT_OBJECTS.SCORE_MARKER: TextObject(32, GameController.SCORE_MARKER_POSITION, "score: " + str(self.player.score)),
            UI_TEXT_OBJECTS.GAME_OVER_MARKER: TextObject(32, GameController.GAME_OVER_MARKER_POSITION, 'Game Over')}

        # self.algChangeTimer.start()

    def update(self):
        if self.gameOver == True:
            self._endGame()
        else:
            self.clock.tick(FPS)
            self._eventHandler()
            self.player.tryMovePlayer()
            self._tryGhostsMove()

            self._tryCheckPlayerGhostsCollisions()
            self._tryCheckPlayerCoinsCollisions()
            self.render()
            self._tryStopGame()

        # self.algorithmHandler()
        # self.calculateAlgsTime()
        # self.stopGhosts()
        # pygame.time.delay(100)
        # else:
        #     self.endGame()

    def render(self):
        self._clearScreen()
        self.entitiesSpriteGroup.draw(self.layer1)
        self._updateUI()
        # self.entitiesSpriteGroup.update()

        self.screen.blit(self.layer1, SCREEN_START_POINT)

    def _eventHandler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

    def _clearScreen(self):
        self.layer1 = self.map1.background.copy()

    def _createGhost(self, ghostType: int):
        return Ghost(self.entitiesSpriteGroup,
                     self.currentMap.ghostsStartWorldPosition,
                     MAIN_DIRECTORY + '\Sprites\\' + getGhostName(ghostType) + '.png',
                     getGhostName(ghostType),
                     self.currentMap.colorMap,
                     getGhostColor(ghostType))

    def _tryGhostsMove(self):
        if self.ghostsCanMove == False:
            return
        for ghost in self.ghostsDict.values():
            ghost.moveGhost()

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
        if self.player.hp < 1 or len(self.coinsMap) < 1:
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

    def _updateUI(self):
        self.ui[UI_TEXT_OBJECTS.HP_MARKER].textUpdate('hp: ' + str(self.player.hp), self.layer1)
        self.ui[UI_TEXT_OBJECTS.SCORE_MARKER].textUpdate('score: ' + str(self.player.score), self.layer1)
        # self.currentAlgorithmText.textUpdate("Algorithm: " + strOfAlg(self.currentAlgorithm), self.screen)
        # self.timeBFSText.textUpdate("BFS Time: " + str(self.timeBFS), self.screen)
        # self.timeDFSText.textUpdate("DFS Time: " + str(self.timeDFS), self.screen)
        # self.timeUCSText.textUpdate("UCS Time: " + str(self.timeUCS), self.screen)

    def _endGame(self):
        self._clearScreen()
        self.ui[UI_TEXT_OBJECTS.GAME_OVER_MARKER].textUpdate('game over', self.layer1)
        self.ui[UI_TEXT_OBJECTS.SCORE_MARKER].textUpdate('score: ' + str(self.player.score), self.layer1)
        self.screen.blit(self.layer1, SCREEN_START_POINT)

    # region OldCode
    # def start(self):
    #
    #
    #     self.screen.fill(BLACK)
    #     self.enteties.append(self.player)
    #     self.ghosts.append(self.G_rikky)
    #     self.ghosts.append(self.G_greenky)
    #     self.ghosts.append(self.G_pinky)
    #     self.ghosts.append(self.G_clyne)
    #
    #     self.enteties = self.enteties + self.ghosts
    #     # self.enteties.append(self.G_rikky2)
    #     # self.enteties.append(self.G_rikky3)
    #     self.algChangeTimer.start()
    #
    # def update(self):
    #     self.clock.tick(FPS)
    #     self.eventHandler()
    #     if self.gameOver == False:
    #         self.player.tryMovePlayer()
    #         if self.ghostMoving:
    #             self.ghostMove()
    #         self.checkCollisions()
    #         self.render()
    #         self.algorithmHandler()
    #         self.calculateAlgsTime()
    #         self.stopGhosts()
    #
    #         # pygame.time.delay(100)
    #     else:
    #         self.endGame()
    #
    # def render(self):
    #     self.clearScreen()
    #     self.sprites_group.update()
    #     self.sprites_group.draw(self.screen)
    #     self.scoreText.textUpdate('score: ' + str(self.player.score), self.screen)
    #     self.hpText.textUpdate('hp: ' + str(self.player.hp), self.screen)
    #     self.currentAlgorithmText.textUpdate("Algorithm: " + strOfAlg(self.currentAlgorithm), self.screen)
    #     self.timeBFSText.textUpdate("BFS Time: " + str(self.timeBFS), self.screen)
    #     self.timeDFSText.textUpdate("DFS Time: " + str(self.timeDFS), self.screen)
    #     self.timeUCSText.textUpdate("UCS Time: " + str(self.timeUCS), self.screen)
    #
    # def respawnAll(self):
    #     for entity in self.enteties:
    #         entity.respawn(entity.startPosition, entity.startDirection)
    #     self.render()
    #     # pygame.time.delay(1000)
    #
    # def algorithmHandler(self):
    #     for ghost in self.ghosts:
    #         chooseAlgorithm(self.currentAlgorithm,
    #                         findNearestNodeTo(ghost.rect.center, self.map),
    #                         findNearestNodeTo(self.player.rect.center, self.map),
    #                         ghost.pathColor, self.screen, self.map)
    #     if self.algChangeTimer.stop() > 1 and pygame.key.get_pressed()[pygame.K_z]:
    #         self.currentAlgorithm = changeAlgorithm(self.currentAlgorithm)
    #         self.algChangeTimer.start()
    #
    # def calculateAlgsTime(self):
    #     if pygame.key.get_pressed()[pygame.K_c]:
    #         ghost = self.ghosts[0]
    #         self.timer.start()
    #         chooseAlgorithm(BFS,
    #                         findNearestNodeTo(ghost.rect.center, self.map),
    #                         findNearestNodeTo(self.player.rect.center, self.map),
    #                         ghost.pathColor, self.screen, self.map)
    #         self.timeBFS = self.timer.stop().__round__(5)
    #
    #         self.timer.start()
    #         chooseAlgorithm(DFS,
    #                         findNearestNodeTo(ghost.rect.center, self.map),
    #                         findNearestNodeTo(self.player.rect.center, self.map),
    #                         ghost.pathColor, self.screen, self.map)
    #         self.timeDFS = self.timer.stop().__round__(5)
    #
    #         self.timer.start()
    #         chooseAlgorithm(UCS,
    #                         findNearestNodeTo(ghost.rect.center, self.map),
    #                         findNearestNodeTo(self.player.rect.center, self.map),
    #                         ghost.pathColor, self.screen, self.map)
    #         self.timeUCS = self.timer.stop().__round__(5)
    #
    # def stopGhosts(self):
    #     if pygame.key.get_pressed()[pygame.K_x]:
    #         self.ghostMoving = not self.ghostMoving
    #
    # def endGame(self):
    #     self.clearScreen()
    #     self.gameOverText.textUpdate('game over', self.screen)
    #     self.scoreText.textUpdate('score: ' + str(self.player.score), self.screen)
    #
    # def clearScreen(self):
    #     self.screen.blit(self.map.background, self.map.background.get_rect())
    #
    # def eventHandler(self):
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             exit()
    #
    # def ghostMove(self):
    #     for ghost in self.ghosts:
    #         ghost.move()
    #
    # def checkCollisions(self):
    #     # if checkCollision(self.player, self.G_rikky) or \
    #     #         checkCollision(self.player, self.G_pinky) or \
    #     #         checkCollision(self.player, self.G_greenky) or \
    #     #         checkCollision(self.player, self.G_clyne):
    #     #     self.respawnAll()
    #     for ghost in self.ghosts:
    #         if checkCollision(self.player, ghost):
    #             self.respawnAll()
    #             break
    # endregion


gameController = GameController()
gameController.start()
while True:
    gameController.update()
    pygame.display.flip()

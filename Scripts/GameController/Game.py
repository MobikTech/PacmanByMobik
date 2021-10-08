from Scripts.Entities.Sprites.PlayerSprite import *
from Scripts.Map.Map import Map
from Scripts.Entities.Sprites.GhostSprite import GhostSprite
from Text import TextObject
from SearchAlgorithmes import *


class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.gameOver = False
        # self.background = pygame.surface.Surface(SCREEN_SIZE).convert()
        self.clock = pygame.time.Clock()
        self.sprites_group = pygame.sprite.Group()

        self.enteties = list()
        self.ghosts = list()
        self.coinsMap = [[None for x in range(NCOLUMNS)] for y in range(NROWS)]
        self.coinAmount = 0
        self.map_1 = Map(pygame.image.load('../Sprites/pacman_map_1_31x31.png'), pygame.image.load(
            '../Sprites/pacman_map_1_651x651.png'))
        self.map_2 = Map(pygame.image.load('../Sprites/pacman_map_2_31x31.png'), pygame.image.load(
            '../Sprites/pacman_map_2_651x651.png'))
        self.map = self.map_1
        self.map.mapScan(self)

        self.player = PlayerSprite(self.sprites_group, self.map.playerStartPosition, self)
        self.G_rikky = GhostSprite("Rikky", "../../Sprites/Rikky.png", self.sprites_group, self.map.ghostsStartPosition, self.map, RED)
        # self.G_rikky2 = Ghost("Rikky2", "Sprites/Rikky.png", self.sprites_group, self.map.ghostsStartPosition, self.map)
        # self.G_rikky3 = Ghost("Rikky3", "Sprites/Rikky.png", self.sprites_group, self.map.ghostsStartPosition, self.map)

        self.G_greenky = GhostSprite("Greenky", "../../Sprites/Greenky.png", self.sprites_group, self.map.ghostsStartPosition, self.map, GREEN)
        self.G_pinky = GhostSprite("Pinky", "../../Sprites/Pinky.png", self.sprites_group, self.map.ghostsStartPosition, self.map, PINK)
        self.G_clyne = GhostSprite("Clyde", "../../Sprites/Clyne.png", self.sprites_group, self.map.ghostsStartPosition, self.map, YELLOW)

        self.timer = Timer()
        self.currentAlgorithm = BFS
        self.timeBFS = 0
        self.timeDFS = 0
        self.timeUCS = 0


        self.scoreText = TextObject('Fonts/Pinmolddemo-jEaxv.otf', 32, WHITE, (CENTER[0], CENTER[1] + CELL_SIZE * 2), "score: " + str(self.player.score))
        self.hpText = TextObject('Fonts/Pinmolddemo-jEaxv.otf', 32, WHITE, (CENTER[0] - CELL_SIZE * 11, CENTER[1] + CELL_SIZE * 2), "hp: " + str(self.player.hp))
        self.gameOverText = TextObject('Fonts/Pinmolddemo-jEaxv.otf', 56, WHITE, (CENTER[0], CENTER[1] + CELL_SIZE * 5), "game over")
        self.currentAlgorithmText = TextObject('Fonts/Pinmolddemo-jEaxv.otf', 32, WHITE, (CENTER[0], CENTER[1] + CELL_SIZE * 8), "Algorithm: " + strOfAlg(self.currentAlgorithm))
        self.timeBFSText = TextObject('Fonts/Pinmolddemo-jEaxv.otf', 20, WHITE, (CENTER[0], CENTER[1] + CELL_SIZE * 10), "BFS Time: " + str(self.timeBFS))
        self.timeDFSText = TextObject('Fonts/Pinmolddemo-jEaxv.otf', 20, WHITE, (CENTER[0], CENTER[1] + CELL_SIZE * 11), "DFS Time: " + str(self.timeDFS))
        self.timeUCSText = TextObject('Fonts/Pinmolddemo-jEaxv.otf', 20, WHITE, (CENTER[0], CENTER[1] + CELL_SIZE * 12), "UCS Time: " + str(self.timeUCS))

        self.algChangeTimer = Timer()
        self.ghostMoving = True



    def start(self):
        self.screen.fill(BLACK)
        self.enteties.append(self.player)
        self.ghosts.append(self.G_rikky)
        self.ghosts.append(self.G_greenky)
        self.ghosts.append(self.G_pinky)
        self.ghosts.append(self.G_clyne)

        self.enteties = self.enteties + self.ghosts
        # self.enteties.append(self.G_rikky2)
        # self.enteties.append(self.G_rikky3)
        self.algChangeTimer.start()

    def respawnAll(self):
        for entity in self.enteties:
            entity.respawn(entity.startPosition, entity.startDirection)
        self.render()
        # pygame.time.delay(1000)

    def algorithmHandler(self):
        for ghost in self.ghosts:
            chooseAlgorithm(self.currentAlgorithm,
                        findNearestNodeTo(ghost.rect.center, self.map),
                        findNearestNodeTo(self.player.rect.center, self.map),
                        ghost.pathColor, self.screen,self.map)
        if self.algChangeTimer.stop() > 1 and pygame.key.get_pressed()[pygame.K_z]:
            self.currentAlgorithm = changeAlgorithm(self.currentAlgorithm)
            self.algChangeTimer.start()

    def calculateAlgsTime(self):
        if pygame.key.get_pressed()[pygame.K_c]:
            ghost = self.ghosts[0]
            self.timer.start()
            chooseAlgorithm(BFS,
                findNearestNodeTo(ghost.rect.center, self.map),
                findNearestNodeTo(self.player.rect.center, self.map),
                ghost.pathColor, self.screen,self.map)
            self.timeBFS = self.timer.stop().__round__(5)

            self.timer.start()
            chooseAlgorithm(DFS,
                            findNearestNodeTo(ghost.rect.center, self.map),
                            findNearestNodeTo(self.player.rect.center, self.map),
                            ghost.pathColor, self.screen, self.map)
            self.timeDFS = self.timer.stop().__round__(5)

            self.timer.start()
            chooseAlgorithm(UCS,
                            findNearestNodeTo(ghost.rect.center, self.map),
                            findNearestNodeTo(self.player.rect.center, self.map),
                            ghost.pathColor, self.screen, self.map)
            self.timeUCS = self.timer.stop().__round__(5)

    def stopGhosts(self):
        if pygame.key.get_pressed()[pygame.K_x]:
            self.ghostMoving = not self.ghostMoving


    def update(self):
        self.clock.tick(FPS)
        self.eventHandler()
        if self.gameOver == False:
            self.player.movePlayer()
            if self.ghostMoving:
                self.ghostMove()
            self.checkCollisions()
            self.render()
            self.algorithmHandler()
            self.calculateAlgsTime()
            self.stopGhosts()

                # pygame.time.delay(100)
        else:
            self.endGame()


    def endGame(self):
        self.clearScreen()
        self.gameOverText.textUpdate('game over', self.screen)
        self.scoreText.textUpdate('score: ' + str(self.player.score), self.screen)

    def clearScreen(self):
        self.screen.blit(self.map.background, self.map.background.get_rect())

    def eventHandler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

    def render(self):
        self.clearScreen()
        self.sprites_group.update()
        self.sprites_group.draw(self.screen)
        self.scoreText.textUpdate('score: ' + str(self.player.score), self.screen)
        self.hpText.textUpdate('hp: ' + str(self.player.hp), self.screen)
        self.currentAlgorithmText.textUpdate("Algorithm: " + strOfAlg(self.currentAlgorithm), self.screen)
        self.timeBFSText.textUpdate("BFS Time: " + str(self.timeBFS), self.screen)
        self.timeDFSText.textUpdate("DFS Time: " + str(self.timeDFS), self.screen)
        self.timeUCSText.textUpdate("UCS Time: " + str(self.timeUCS), self.screen)



    def ghostMove(self):
        for ghost in self.ghosts:
            ghost.move()

    def checkCollisions(self):
        # if checkCollision(self.player, self.G_rikky) or \
        #         checkCollision(self.player, self.G_pinky) or \
        #         checkCollision(self.player, self.G_greenky) or \
        #         checkCollision(self.player, self.G_clyne):
        #     self.respawnAll()
        for ghost in self.ghosts:
            if checkCollision(self.player, ghost):
                self.respawnAll()
                break







gameController = GameController()
gameController.start()
while True:
    gameController.update()
    pygame.display.flip()

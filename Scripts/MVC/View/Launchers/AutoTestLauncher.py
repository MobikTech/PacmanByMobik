from Scripts.MVC.Controller.Common.Algorithmes.Algorithmes import Algorithmes
from Scripts.MVC.Controller.GameLoop import MotionManager, GameLoop
from Scripts.MVC.View.Timer import Timer


LAUNCHES_COUNT = 20

class TestController():
    WIN_MARKER = 'win'
    LOSE_MARKER = 'lose'

    def __init__(self):
        self.gameLooper = GameLoop()
        self.isRunning = True
        self.result = None

        self.timer = Timer()

    def start(self):
        self.gameLooper.start()
        self.timer.start()
        print('Start Coins num: {0}'.format(self.gameLooper.info.coinsContainer.getCoinsCount()))

    def update(self):
        self.gameLooper.update()
        if self.gameLooper.info.coinsContainer.getCoinsCount() < 1:
            self.__endGame(TestController.WIN_MARKER)
        elif self.gameLooper.info.hp < 1:
            self.__endGame(TestController.LOSE_MARKER)

    def __endGame(self, endType: str):
        timeStr = str(self.timer.start())
        scoreStr = str(self.gameLooper.info.score)
        algStr = TestController.getAlgStr(MotionManager.PLAYER_ALGORITHM)
        coinsLeft = self.gameLooper.info.coinsContainer.getCoinsCount().__str__()
        self.result = Result(endType, timeStr, scoreStr, algStr, coinsLeft)
        self.isRunning = False

    @staticmethod
    def getAlgStr(algMethod):
        if algMethod == Algorithmes.minimax:
            return 'Minimax'
        elif algMethod == Algorithmes.expectimax:
            return 'Expectimax'
        raise NotImplementedError


class Result():
    def __init__(self, status, time, score, algorithm, coinsLeft):
        self.status = status
        self.time = time
        self.score = score
        self.algorithm = algorithm

        self.coinsLeft = coinsLeft

    def __str__(self):
        print('---------------')
        print('Game result: {0}'.format(self.status))
        print('Time: {0}'.format(self.time))
        print('Score: {0}'.format(self.score))
        print('Algorithm: {0}'.format(self.algorithm))
        print('CoinsLeft: {0}'.format(self.coinsLeft))
        print('---------------')
        # print()

class ResultContainer():
    def __init__(self):
        self.results = list()

    def add(self, result: Result):
        self.results.append(result)

    def showStatisticInfo(self):
        winCount = 0
        loseCount = 0
        for result in self.results:
            if result.status == 'win':
                winCount += 1
            if result.status == 'lose':
                loseCount += 1

        print('WinRate: {0}%'.format(int((winCount / (winCount + loseCount)) * 100)))

#region TestLauncher

resultContainer = ResultContainer()
for counter in range(LAUNCHES_COUNT):
    testController = TestController()
    testController.start()
    while testController.isRunning:
        testController.update()
    print(testController.result.__str__())
    resultContainer.add(testController.result)
resultContainer.showStatisticInfo()

#endregion
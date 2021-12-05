import torch
import random
import numpy as np
import skimage

from Scripts.MVC.Controller.Common.Constants import GRID, CELL_SIZE
from Scripts.MVC.View.Launchers.Game import GameController
from collections import deque
from Scripts.MVC.View.RL.ModelRL import Linaer_Q_Network, QTrainer
from Scripts.MVC.View.RL.Helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001
ACTIONS_COUNT = 4
INPUT_SIZE = GRID.COLUMNS_COUNT * GRID.ROWS_COUNT
# INPUT_SIZE = GRID.COLUMNS_COUNT * GRID.ROWS_COUNT * CELL_SIZE * CELL_SIZE

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate (< 1)
        self.memory = deque(maxlen=MAX_MEMORY) #popleft()
        self.model = Linaer_Q_Network(INPUT_SIZE, 256, ACTIONS_COUNT)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game: GameController):
        # screen_image = torch.from_numpy(game.get_screen_image())
        # screen_image = torch.flatten(screen_image, 1)
        # return screen_image
        image = game.get_screen_image()
        image = skimage.color.rgb2gray(image)
        image = skimage.transform.resize(image, (GRID.COLUMNS_COUNT, GRID.ROWS_COUNT))

        return np.array(image).flatten()

    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, game_overs = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)

    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)

    def get_actions(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = np.zeros(ACTIONS_COUNT)
        if random.randint(0, 200) < self.epsilon:
            move_index = random.randint(0, ACTIONS_COUNT - 1)
            final_move[move_index] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move_index = torch.argmax(prediction).item()
            final_move[move_index] = 1
        return final_move

def train():
    print('train')
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = GameController()
    iter = 0
    while True:
        state_old = agent.get_state(game)

        actions = agent.get_actions(state_old)

        #todo
        reward, game_over, score = game.play_step(actions)
        state_new = agent.get_state(game)

        agent.train_short_memory(state_old, actions, reward,
                                 state_new, game_over)

        agent.remember(state_old, actions, reward, state_new, game_over)

        if game_over:
            #todo
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

        iter += 1


# if __name__ == '__main__':
#     train()
train()




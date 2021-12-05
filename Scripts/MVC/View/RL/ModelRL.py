import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

class Linaer_Q_Network(nn.Module):

    def __init__(self, input_size, hidden_size, output_size):
        super(Linaer_Q_Network, self).__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)


    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, file_name='model.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)
        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)



class QTrainer:
    def __init__(self, model, lr, gamma):
        self.model = model
        self.lr = lr
        self.gamma = gamma
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, states, actions, rewards, next_states, game_overs):
        states = torch.tensor(states, dtype=torch.float)
        next_states = torch.tensor(next_states, dtype=torch.float)
        actions = torch.tensor(actions, dtype=torch.long)
        rewards = torch.tensor(rewards, dtype=torch.float)

        # (n, x)

        if len(states.shape) == 1:
            # (1, x)
            states = torch.unsqueeze(states, 0)
            next_states = torch.unsqueeze(next_states, 0)
            actions = torch.unsqueeze(actions, 0)
            rewards = torch.unsqueeze(rewards, 0)
            game_overs = (game_overs,)

        # 1: predicted Q values with current state
        pred = self.model(states)

        target = pred.clone()
        for idx in range(len(game_overs)):
            Q_new = rewards[idx]
            if not game_overs[idx]:
                Q_new = rewards[idx] + self.gamma * torch.max(self.model(next_states[idx]))

            target[idx][torch.argmax(actions[idx]).item()] = Q_new

        # 2: Q_new = r + y * max(next_predicted Q value) -> only do this if not done
        # pred.clone()
        # preds[argmax(action)] = Q_new
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()



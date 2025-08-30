import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

import os

class LinearQNet(nn.Module):
    def __init__(self, inputSize, hiddenSize, secondHiddenSize, outputSize):
        super().__init__()

        self.linear1 = nn.Linear(in_features=inputSize, out_features=hiddenSize)
        self.linear2 = nn.Linear(in_features=hiddenSize, out_features=secondHiddenSize)
        self.linear3 = nn.Linear(in_features=secondHiddenSize, out_features=outputSize)


    def forward(self, X):
        out = self.linear1(X)
        out = F.relu(out)
        out = self.linear2(out)
        out = F.relu(out)
        out = self.linear3(out)

        return out

    def save(self, epochs):
        import time

        path = f"models/model_incremental_{epochs}_{time.time()}.pth"
        torch.save(self.state_dict(), path)


class QTrainner:
    def __init__(self, model, lr, gama):
        self.model = model
        self.lr = lr
        self.gama = gama
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()


    # def trainStepOld(self, state, action, reward, nextState, gameOver):
    #     state = torch.tensor(state, dtype=torch.float)
    #     action = torch.tensor(state, dtype=torch.long)
    #     reward = torch.tensor(state, dtype=torch.float)
    #     nextState = torch.tensor(nextState, dtype=torch.float)
    #
    #     if len (state.shape):
    #         # (1, x)
    #         state = torch.unsqueeze(state, 0)
    #         action = torch.unsqueeze(action, 0)
    #         reward = torch.unsqueeze(reward, 0)
    #         nextState = torch.unsqueeze(nextState, 0)
    #         gameOver = (gameOver, )
    #
    #     # 1 predicted q values with current state
    #     pred = self.model(state)
    #
    #
    #     # Q new: reward + gamma * max(next_predicted_q_value) -> only do this if not game over
    #     target = pred.clone()
    #
    #     for i in range(len(gameOver)):
    #         qNew = reward[i]
    #
    #         if not gameOver[i]:
    #             qNew = reward[i] + self.gama * torch.max(self.model(nextState[i]))
    #
    #         target[i][torch.argmax(action).item()] = qNew
    #
    #
    #     self.optimizer.zero_grad()
    #     loss = self.criterion(target, pred)
    #     loss.backward()
    #     self.optimizer.step()


    def trainStep(self, state, action, reward, newState, gameOver):

        stateTensor = torch.tensor(state, dtype=torch.float)
        actionTensor = torch.tensor(action, dtype=torch.long)
        rewardTensor = torch.tensor(reward, dtype=torch.float)
        newStateTensor = torch.tensor(newState, dtype=torch.float)

        if len(stateTensor.shape) == 1:
            stateTensor = torch.unsqueeze(stateTensor, 0)
            newStateTensor = torch.unsqueeze(newStateTensor, 0)
            actionTensor = torch.unsqueeze(actionTensor, 0)
            rewardTensor = torch.unsqueeze(rewardTensor, 0)
            gameOver = (gameOver, )

        # 1. predicted q values with current state
        prediction = self.model(stateTensor)

        # Q_new = 2. reward + gamma * max(next predicted q value) -> only do this if not done
        target = prediction.clone()

        for i in range(len(gameOver)):
            Qnew = rewardTensor[i]

            if not gameOver[i]:
                Qnew = rewardTensor[i] + self.gama * torch.max(self.model(newStateTensor[i]))

            target[i][torch.argmax(actionTensor).item()] = Qnew


        self.optimizer.zero_grad()
        loss = self.criterion(target, prediction)
        loss.backward()

        self.optimizer.step()




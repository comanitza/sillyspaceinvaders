import torch
import random
import numpy as np

from gamerunner import GameRunner
from gameelements import Action

from collections import deque

from model import LinearQNet, QTrainner

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LEARNING_RATE = 0.01

class Agent:
    def __init__(self, numberOfExpectedIteration = 120):
        self.numberOfGames = 0
        self.epsilon = 0 # randomness
        self.gama = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = LinearQNet(8, 256, 128, 3)
        self.trainner = QTrainner(model=self.model, lr=LEARNING_RATE, gama=self.gama)
        self.numberOfExpectedIteration = numberOfExpectedIteration

    def getState(self, runner: GameRunner) -> []:
        return runner.getState()

    def remember(self, state, action, reward, nextState, gameOver):
        self.memory.append((state, action, reward, nextState, gameOver))


    def trainLongMemory(self):
        if len(self.memory) > BATCH_SIZE:
            miniSample = random.sample(self.memory, BATCH_SIZE)
        else:
            miniSample = self.memory

        states, actions, rewards, nextStates, gameOvers = zip(*miniSample)
        self.trainner.trainStep(states, actions, rewards, nextStates, gameOvers)


    def trainShortMemory(self, state, action, reward, nextState, gameOver):
        self.trainner.trainStep(state, action, reward, nextState, gameOver)

    def getAction(self, state) -> []:
        # still random
        self.epsilon = self.numberOfExpectedIteration - self.numberOfGames # era 80
        finalMove = [0, 0 ,0]

        if random.randint(0, self.numberOfExpectedIteration * 2) < self.epsilon:
            move = random.randint(0, 2)
            finalMove[move] = 1
        else:
            stateAsTensor = torch.tensor(state, dtype=torch.float)
            prediction = self.model(stateAsTensor)
            move = torch.argmax(prediction).item()
            finalMove[move] = 1

        return finalMove

# def trainAgentOld():
#     print("started training agent ...")
#     scores = []
#     averageScores = []
#     totalScore = 0
#     record = 0
#     agent = Agent()
#     gameRunner = GameRunner()
#
#
#
#     import time
#     displayOnScreen = True
#     lastLaserShotTime = time.time()
#
#
#     while True:
#         # get old state
#         currentState = agent.getState(gameRunner)
#
#         # get action
#         action = agent.getAction(currentState)
#
#         # perform move and get new state
#         # reward, done, score
#
#         reward, score, isGameOver = gameRunner.simulateGame()
#         gameRunner.performAction(gameRunner.convertAction(action))
#
#         newState = gameRunner.getState()
#
#         # train short memory
#         agent.trainShortMemory(currentState, action, reward, newState, isGameOver)
#
#         # remember
#         agent.remember(currentState, action, reward, newState, isGameOver)
#
#         if isGameOver:
#             # train long memory/replay memory
#             # plot the results
#             gameRunner.game.reset()
#             agent.numberOfGames += 1
#             agent.trainLongMemory()
#
#             if score > record:
#                 record = score
#                 # save the model agent.model.save()
#
#             print("Game", agent.numberOfGames, score, "record", record)
#             # todo do some plotting man
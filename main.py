# space invaders stuff
# https://youtu.be/PFMoo_dvhyw?t=7424
# https://youtu.be/L8ypSXwyBds?t=5749

from gamerunner import GameRunner
from gameelements import Action
from agent import Agent
import torch
import matplotlib.pyplot as plt
import time

print("starting silly space invaders")


# if False:
#     runner.playGame()
# else:
#     agent = Agent()
#     #agent.model.load_state_dict(torch.load("D:\pythonwork\games\sillyspaceinvaders\models\model1755893650.291997.pth", weights_only=True))
#     #agent.model.load_state_dict(torch.load("D:\pythonwork\games\sillyspaceinvaders\models\model_320_1755977226.7062056.pth", weights_only=True))
#     # agent.model.load_state_dict(torch.load("D:\pythonwork\games\sillyspaceinvaders\models\model_360_1755990345.0241191.pth", weights_only=True))
#     # agent.model.load_state_dict(torch.load("D:\pythonwork\games\sillyspaceinvaders\models\model_360_1755990345.0241191.pth", weights_only=True))


def playGameAsHuman():
    runner = GameRunner(playerName="HUMAN")
    runner.game.lives = 1

    runner.playGame()

def playSimulationWithModel(model: str, payerName: str)-> int:
    runner = GameRunner(playerName=payerName)
    runner.game.lives = 1

    agent = Agent()

    agent.model.load_state_dict(torch.load(model, weights_only=True))
    score = runner.simulate(agent)

    return score


def playSimulationAsLowerTrainedModel():
    score = playSimulationWithModel("models\model1755893650.291997.pth", "TRAINED 40")

    print(f"simulation score: {score}")

def playSimulationAsHighlyTrainedModel():
    score = playSimulationWithModel("models\model_360_1755990345.0241191.pth", "TRAINED 400")

    print(f"simulation score: {score}")


def simulateTwoModelsComparison(modelA, modelAName, modelB, modelBName, iterations: int = 10):
    labels = []
    scoresA = []
    scoresB = []

    for i in range(iterations):
        print(f"starting iteration {i}")
        scoresA.append(playSimulationWithModel(modelA, modelAName))
        scoresB.append(playSimulationWithModel(modelB, modelBName))

        labels.append(i)


    plt.plot(labels, scoresA, label = modelAName)
    plt.plot(labels, scoresB, label = modelBName)
    plt.savefig(f"graphs/{modelAName}_{modelBName}_{iterations}_{time.time()}.png")


def simulateLowAndHighlyTrainedModel():
    simulateTwoModelsComparison("models\model1755893650.291997.pth", "TRAINED 40", "models\model_360_1755990345.0241191.pth", "TRAINED 400", iterations=5)

# run things
simulateLowAndHighlyTrainedModel()

print("### ok, all done")
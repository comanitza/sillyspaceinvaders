# space invaders stuff
# https://youtu.be/PFMoo_dvhyw?t=7424
# https://youtu.be/L8ypSXwyBds?t=5749

from gamerunner import GameRunner
from agent import Agent
import torch
import matplotlib.pyplot as plt
import time

print("starting silly space invaders")

def playGameAsHuman():
    runner = GameRunner(playerName="HUMAN", includeObstacles=True)
    runner.game.lives = 3

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
    score = playSimulationWithModel("models\model_520_1756057607.2338269.pth", "TRAINED 520")

    print(f"simulation score: {score}")


def simulateTwoModelsComparison(modelTuples:[(str, str)], iterations: int = 10):
    labels = []
    scoresMap = {}

    for t in modelTuples:
        scoresMap[t[1]] = []

    for i in range(1, iterations + 1):
        print(f"starting iteration {i}")

        for t in modelTuples:
            score = playSimulationWithModel(t[0], t[1])
            scoresMap[t[1]].append(score)
            print(f"Model {t[1]} finished with score {score}")

        labels.append(i)

    mergedKeys = "_".join(str(k) for k in scoresMap.keys())

    plt.title("Models Comparison")

    for modelName, scores in scoresMap.items():
        plt.plot(labels, scores, label = modelName)

    plt.legend(scoresMap.keys(), loc="lower right")
    plt.savefig(f"graphs/comparison_{mergedKeys}_{iterations}_{time.time()}.png")
    plt.close()


def simulateTrainedModelComparison():
    simulateTwoModelsComparison(
        [("models\model_40_1755893650.291997.pth", "MODEL 40"),
         ("models\model_200_1755964576.2514975.pth", "MODEL 200"),
         ("models\model_562A_1756522638.3977141.pth", "MODEL 562A")], iterations=5)

# run things
simulateTrainedModelComparison()

# play as human
#playGameAsHuman()

print("### ok, all done")
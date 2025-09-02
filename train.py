# training stuff
from agent import Agent
from gamerunner import GameRunner
# [8100, 900, 7100, 5000, 3300, 4700, 5600, 1300, 1000, 8200, 6000, 3000, 4000, 6100, 5100, 200, 5700, 100, 3600, 9400, 6200, 2400, 7200, 7600, 6800, 1700, 1400, 1800, 5900, 6700, 5500, 5600, 2600, 5900, 6000, 1000, 4800, 2100, 700, 6400, 4700, 5500, 5500, 4000, 9900, 3900, 500, 2800, 100, 7300, 400, 300, 3800, 8100, 1000, 100, 8800, 5600, 7900, 3700, 5300, 1200, 1100, 5600, 7000, 5800, 4700, 1600, 6800, 500, 9100, 6800, 8200, 3900, 7700, 7500, 4100, 6200, 4300, 6100, 7700, 5300, 8400, 4400, 5700, 6500, 8600, 6000, 6700, 100, 100, 9400, 3300, 8400, 5500, 7500, 6000, 2100, 600, 5700, 4700, 200, 1600, 7300, 1800, 8200, 5600, 5000, 7400, 6200, 1800, 1700, 6300, 2100, 1800, 8500, 3200, 7800, 2800, 4200, 6200, 600, 8100, 9600, 9600, 100, 4100, 8000, 3800, 9900, 8400, 6200, 7400, 9900, 4200, 9900, 1900, 5000, 5700, 6800, 100, 2700, 300, 300, 6200, 6400, 8100, 9600, 6400, 8400, 2600, 100, 9400, 3800, 4000, 800, 7400, 4600, 5800, 600, 5400, 5700, 5600, 5700, 9000, 2000, 8600, 400, 9900, 2200, 9900, 600, 3900, 100, 9900, 100, 1700, 9900, 2300, 4500, 1100, 9400, 500, 3900, 3500, 2800, 2200, 5200, 4600, 4200, 100, 1600, 700, 5700, 7100, 6100, 4000, 9700, 500, 4900, 5900, 600, 4100, 8100, 7600, 4200, 400, 400, 3100, 5200, 7800, 6700, 3200, 9600, 9100, 2200, 9400, 3400, 2300, 700, 7700, 8400, 6700, 900, 6100, 8700, 9900, 7100, 1100, 9200, 8700, 1700, 6400, 1700, 7300, 7700, 7000, 6100, 600, 3400, 9900, 1400, 5700, 7100, 800, 100, 4100, 6900, 6600, 4500, 9200, 7200, 9900, 3200, 5200, 3100, 6200, 200, 4700, 8900, 800, 100, 9900, 1300, 4100, 5600, 5400, 500, 4200, 2200, 6800, 2300, 8400, 8200, 500, 2300, 7600, 4800, 1800, 3100, 2000, 3200, 7800, 5900, 1600, 2100, 9900, 7400, 8500, 9900, 4600, 3900, 2800, 6000, 7000, 3100, 9300, 6600, 9200, 6300, 4100, 4400, 100, 1100, 3300, 4000, 8000, 100, 4100, 9600, 100, 5700, 200, 6300, 1300, 2900, 5900, 3200, 9900, 3300, 9000, 8000, 4700, 8600, 3400, 4700, 8900, 300, 4300, 5500, 8100, 7900, 9000, 6500, 700, 4900, 6900, 2300, 3200, 4400, 7000, 1600, 5900, 9500, 6800, 7400, 7000, 3000, 4400, 7400, 4800, 5800, 500, 8000, 1600, 5800, 4700, 9600, 6900, 6400, 9000, 8500, 5600, 7600, 8000, 9900, 2500, 3100, 8200, 8100, 9900, 9300, 3500, 1200, 2200, 2600, 3800, 9900, 4100, 600, 4500, 5300, 4200, 6900, 1400, 7200, 7600, 100, 8900, 6400, 8900, 6100, 6000, 6700, 500, 9400, 2100, 1800, 6100, 6100, 2600, 200, 2500, 9600, 8300, 7300, 3500, 5500, 6200, 500, 9900, 6500, 5300, 100, 1800, 5400, 8500, 7100, 7300, 5300, 9500, 7100, 4600, 9600, 7800, 6800, 9900, 400, 6600, 8300, 200, 2900, 7100, 5800, 8500, 3200, 7000, 9900, 4400, 7700, 7000, 8300, 5700, 3200, 700, 6800, 3300, 900, 6100, 8100, 6300, 8600, 6800, 4300, 9900, 1800, 1800, 4800, 7100, 9900, 5400, 5800, 6000, 6900, 5900, 2300, 7000, 6700, 700, 100, 4600, 100, 5100, 3800, 4400, 3800, 3900, 5100, 500, 400, 3600, 4600, 2000, 4200, 3000, 800, 4000, 4800, 4500, 4400, 3600, 5000, 4100, 4200, 4800, 2200, 100, 4300, 4500, 4000, 4200, 4500, 1200, 3800, 4500, 4500, 1200, 4700, 4200, 3600, 4500, 4700, 4600, 9200, 5200, 4100, 4100, 4700, 4500, 4200, 1000, 3800, 400, 100, 4300, 4100, 3600, 300, 400, 100, 3800, 1700, 6000, 4300, 4000, 3600, 4000, 4300, 400, 3700, 100, 3600, 400, 6300, 100, 4800, 4500, 4500, 4500, 3700, 4200, 1300, 4000, 3100, 3900, 3600, 3600, 3700, 3600, 3500, 2700, 200]


def trainAgentWithDisaply():
    numberOfEpochs = 562
    print(f"started training agent with display on {numberOfEpochs} epochs ... ")
    scores = []
    averageScores = []
    totalScore = 0
    record = 0
    agent = Agent(numberOfEpochs)



    import pygame
    from utils import Colors
    import time

    # runner.playGame()
    # runner.simulateGame()
    # runner.simulateGame()
    # runner.performAction(Action.RIGHT)
    # runner.performAction(Action.RIGHT)
    # runner.performAction(Action.RIGHT)
    # runner.simulateGame()

    displayOnScreen = False
    lastLaserShotTime = time.time()
    gameSpeedMultiplier = 20
    laserCoolDown = 0.8


    for i in range(numberOfEpochs):
        localScore = 0

        gameRunner = GameRunner(playerName=f"MACHINE {i}")
        gameRunner.game.lives = 1

        gameRunner.game.reset()
        gameRunner.game.lives = 1
        gameRunner.resetState()

        stepsInIteration = 0

        startTime = time.time()
        print(f"starting game iteration {i}")

        while (gameRunner.game.isGameRunning()):

            # self.game.alienShotLaser() 1753996671.1572711

            stepsInIteration += 1

            if time.time() >= lastLaserShotTime + laserCoolDown:
                gameRunner.game.alienShotLaser()
                lastLaserShotTime = time.time()
                # todo sa vad pozitiile laserelor alienilor


            # currentState = gameRunner.getState()
            #
            # gameRunner.simulateGame()
            # gameRunner.performAction(gameRunner.computeNextAction())
            #
            # newState = gameRunner.getState()
            #
            # if newState[3] == 1:
            #     print("state is different!!!", newState)

            # get old state
            currentState = gameRunner.getState() #agent.getState(gameRunner) #todo de ce alta metoda ?!

            # get action
            action = agent.getAction(currentState)

            # perform move and get new state
            # reward, done, score

            actionToPerform = gameRunner.convertAction(action)

            gameRunner.performAction(actionToPerform)
            reward, score, isGameOver = gameRunner.simulateGame()

            localScore = score

            newState = gameRunner.getState()

            # train short memory
            agent.trainShortMemory(currentState, action, reward, newState, isGameOver)

            # remember
            agent.remember(currentState, action, reward, newState, isGameOver)

            if stepsInIteration >= 300000:
                agent.numberOfGames += 1
                agent.trainLongMemory()

                print(f"done training long memory on game over for iteration {i} in {time.time() - startTime} seconds and {stepsInIteration} steps")
                print("breaking due to steps")

                break


            if isGameOver:
                # train long memory/replay memory
                # plot the results
                agent.numberOfGames += 1
                agent.trainLongMemory()

                print(f"done training long memory on game over for iteration {i} in {time.time() - startTime} seconds and {stepsInIteration} steps")

                # if score > record:
                #     record = score
                #     # save the model agent.model.save()


            if displayOnScreen:
                # draw objects on screen
                gameRunner.screen.fill(Colors.GRAY)
                pygame.draw.rect(gameRunner.screen, Colors.YELLOW, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)
                pygame.draw.line(gameRunner.screen, Colors.YELLOW, (25, 730), (775, 730), 3)
                if gameRunner.game.run:
                    gameRunner.screen.blit(gameRunner.levelSurface, (570, 740, 50, 50))
                else:
                    if gameRunner.game.hasWonLevel:
                        gameRunner.screen.blit(gameRunner.levelFinishedSurface, (540, 740, 50, 50))
                    else:
                        gameRunner.screen.blit(gameRunner.gameOverSurface, (570, 740, 50, 50))

                for life in range(gameRunner.game.lives):
                    gameRunner.screen.blit(gameRunner.game.spaceshipGroup.sprite.image, (50 + (life * 50), 745))

                gameRunner.screen.blit(gameRunner.scoreTextSurface, (50, 15, 50, 50))
                scoreSurface = gameRunner.font.render(str(gameRunner.game.score), False, Colors.YELLOW)
                gameRunner.screen.blit(scoreSurface, (50, 40, 50, 50))

                gameRunner.screen.blit(gameRunner.playerTextSurface, (600, 15, 50, 50))
                gameRunner.screen.blit(gameRunner.playerNameSurface, (600, 40, 50, 50))


                gameRunner.game.spaceshipGroup.draw(gameRunner.screen)
                gameRunner.game.spaceshipGroup.sprite.lasersGroup.draw(gameRunner.screen)

                for obstacle in gameRunner.game.obstacles:
                    obstacle.blocksGroup.draw(gameRunner.screen)

                gameRunner.game.aliensGroup.draw(gameRunner.screen)
                gameRunner.game.alienLasersGroup.draw(gameRunner.screen)
                gameRunner.game.mysteryShipGroup.draw(gameRunner.screen)

                # updating positions
                pygame.display.update()

            gameRunner.clock.tick(60 * gameSpeedMultiplier)

        print(f"Game finished with score {localScore}")
        scores.append(localScore)

        if i in {40, 80, 120, 200, 400}:
            agent.model.save(epochs=i)

    print(scores)
    agent.model.save(epochs=numberOfEpochs)

print("starting training")

trainAgentWithDisaply()

print("### ok, all done")
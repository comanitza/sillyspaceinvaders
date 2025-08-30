# training stuff
from agent import Agent
from gamerunner import GameRunner


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

        if i in {5, 10, 20, 40, 80, 120, 200, 400}:
            agent.model.save(epochs=i)

    print(scores)
    agent.model.save(epochs=numberOfEpochs)

print("starting training")

trainAgentWithDisaply()

print("### ok, all done")
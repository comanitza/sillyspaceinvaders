import pygame
import sys, random, time
from gameelements import Spaceship, Obstacle, Action
from game import Game

from utils import Colors

class GameRunner:

    def __init__(self, playerName = "HUMAN", isAiPlaying = False, includeObstacles=False):
        SCREEN_WIDTH = 750
        SCREEN_HEIGHT = 700
        OFFSET = 50

        pygame.init()

        self.font = pygame.font.Font(None, 40)
        self.levelSurface = self.font.render("LEVEL 01", False, Colors.YELLOW)
        self.gameOverSurface = self.font.render("GAME OVER", False, Colors.YELLOW)
        self.scoreTextSurface = self.font.render("SCORE", False, Colors.YELLOW)
        self.playerTextSurface = self.font.render("PLAYER", False, Colors.YELLOW)
        self.playerNameSurface = self.font.render(playerName, False, Colors.YELLOW)
        self.levelFinishedSurface = self.font.render("LEVEL FINISHED", False, Colors.YELLOW)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT + (2 * OFFSET)))
        pygame.display.set_caption("Silly Space Invaders")

        self.clock = pygame.time.Clock()

        self.game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET, includeObstacles)
        self.SHOT_LASER = pygame.USEREVENT
        pygame.time.set_timer(self.SHOT_LASER, 1200)

        self.MYSTERY_SHIP = pygame.USEREVENT + 1
        pygame.time.set_timer(self.MYSTERY_SHIP, random.randint(10_000, 40_000))
        self.isAiPlaying = isAiPlaying

        # self.previousReward = 0

        self.state = [0, 0, 0, 0, 0, 0, 0, 0]
        # self.previousScore = 0



    def simulate(self, agent = None):

        # runner.playGame()
        # runner.simulateGame()
        # runner.simulateGame()
        # runner.performAction(Action.RIGHT)
        # runner.performAction(Action.RIGHT)
        # runner.performAction(Action.RIGHT)
        # runner.simulateGame()

        displayOnScreen = True
        lastLaserShotTime = time.time()


        while (self.game.isGameRunning()):

            # self.game.alienShotLaser() 1753996671.1572711

            if time.time() >= lastLaserShotTime + 2:
                self.game.alienShotLaser()
                lastLaserShotTime = time.time()

            if agent:
                currentState = self.getState()
                # print("agent is in charge")
                # get action
                action = agent.getAction(currentState)

                # perform move and get new state
                # reward, done, score

                actionToPerform = self.convertAction(action)

                self.performAction(actionToPerform)
            else:
                self.performAction(self.computeNextAction())


            self.simulateGame()


            # newState = self.getState()
            #
            # if newState[3] == 1:
            #     print("state is different!!!", newState)

            if self.game.run and self.game.isAlienBelowSpaceShip():
                print("Game over due to aliens too low")
                self.game.gameOver()

            if displayOnScreen:
                # draw objects on screen
                self.screen.fill(Colors.GRAY)
                pygame.draw.rect(self.screen, Colors.YELLOW, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)
                pygame.draw.line(self.screen, Colors.YELLOW, (25, 730), (775, 730), 3)
                if self.game.run:
                    self.screen.blit(self.levelSurface, (570, 740, 50, 50))
                else:
                    if self.game.hasWonLevel:
                        self.screen.blit(self.levelFinishedSurface, (540, 740, 50, 50))
                    else:
                        self.screen.blit(self.gameOverSurface, (570, 740, 50, 50))

                for life in range(self.game.lives):
                    self.screen.blit(self.game.spaceshipGroup.sprite.image, (50 + (life * 50), 745))

                self.screen.blit(self.scoreTextSurface, (50, 15, 50, 50))
                scoreSurface = self.font.render(str(self.game.score), False, Colors.YELLOW)
                self.screen.blit(scoreSurface, (50, 40, 50, 50))

                self.screen.blit(self.playerTextSurface, (600, 15, 50, 50))
                self.screen.blit(self.playerNameSurface, (600, 40, 50, 50))


                self.game.spaceshipGroup.draw(self.screen)
                self.game.spaceshipGroup.sprite.lasersGroup.draw(self.screen)
                for obstacle in self.game.obstacles:
                    obstacle.blocksGroup.draw(self.screen)

                self.game.aliensGroup.draw(self.screen)
                self.game.alienLasersGroup.draw(self.screen)
                self.game.mysteryShipGroup.draw(self.screen)

                # updating positions
                pygame.display.update()

            self.clock.tick(60)

        return self.game.score


    def getState(self):
        # [dangerStraigth, dangerRight, dangerLeft,
        #  isUnderCover,
        #  enemyStraigth, enemyRight, enemyLeft]

        return self.state

    # todo trebuie sa consider si actiunile facute de job, ge extraterestrii
    def performAction(self, action: Action):
        self.game.spaceship.performAction(action)

    def computeNextAction(self) -> Action:
        import random
        # from position import Move

        return random.choice(list(Action))

    def simulateGame(self):

        initialAlienCount = len(self.game.aliensGroup.sprites())

        # make sure to have fresh data
        self.game.spaceshipGroup.update()
        self.game.moveAliens()
        self.game.alienLasersGroup.update()
        self.game.mysteryShipGroup.update()
        self.game.checkForCollisions()
        self.game.checkLevelWasWon()

        # shoot alien laser
        # move aliens
        # draw/print objects
        # self.game.spaceshipGroup.draw(self.screen)
        # self.game.spaceshipGroup.sprite.lasersGroup.draw(self.screen)

        aliensPosition = list(map(lambda s: (s.rect.x, s.rect.y), self.game.aliensGroup.sprites()))
        # print(len(aliensPosition), self.game.score)

        # obstaclePositions = list(map(lambda s: (s.rect.x, s.rect.y), self.game.obstacles.sprites()))

        spaceshipPosition = (self.game.spaceship.rect.x, self.game.spaceship.rect.y)
        # self.performAction(Action.RIGHT)

        # print(spaceshipPosition)

        totalObstaclePixels = []

        for obstacle in self.game.obstacles:
            obstacle.blocksGroup.sprites()
            totalObstaclePixels.append(list(map(lambda s: (s.rect.x, s.rect.y), obstacle.blocksGroup.sprites())))

        # print(len(totalObstaclePixels))

        lasersPositions  = list(map(lambda s: (s.rect.x, s.rect.y), self.game.alienLasersGroup.sprites()))

        # print("laser frate!", lasersPositions)
        # rewardDelta = 100 * (50 - len(aliensPosition)) - self.previousReward
        # self.previousReward = 100 * (50 - len(aliensPosition))

        # [danger straight, danger right, danger left,
        # isUnderCover,
        # enemy straigth, enemy right, enemy left]

        dangerStraigth, dangerRight, dangerLeft = self.dangerPositionFromShip(spaceshipPosition, lasersPositions)

        # coverStraight = 0
        # coverRight = 0
        # coverLeft = 0

        isUnderCover = self.isShipUnderCover(spaceshipPosition, totalObstaclePixels)


        enemyStraigth, enemyRight, enemyLeft = self.enemyPositionFromShip(spaceshipPosition, aliensPosition)

        isSpaceshipInTheCenter = int(spaceshipPosition[0] > 320 and spaceshipPosition[0] < 600)

        state = [dangerStraigth, dangerRight, dangerLeft,
                 isUnderCover,
                 enemyStraigth, enemyRight, enemyLeft,
                 isSpaceshipInTheCenter]


        self.state = state

        # scoreToReturn = self.game.score - self.previousScore
        newReward = 0

        if initialAlienCount > len(aliensPosition):
            newReward += 100
            # print("got one")

        if isSpaceshipInTheCenter == 1 and dangerStraigth == 0:
            newReward += 50
            # print("in the middle baby!!!")

        if dangerStraigth:
            newReward = -100 #ovridde it

        if enemyStraigth == 1:
            newReward += 30
        else:
            newReward -= 5


        if self.game.run == False and self.game.hasWonLevel == False:
            newReward = -100

        return (newReward, self.game.score, not self.game.isGameRunning())


    def isShipUnderCover(self, spaceshipPosition: (int, int), totalObstaclePixels: [(int, int)]) -> int:

        pixelsAboveShip = 0

        for row in totalObstaclePixels:
            for pixel in row:
                if abs(pixel[0] - spaceshipPosition[0]) < 3:
                    pixelsAboveShip += 1

        if pixelsAboveShip >= 20:
            return 1
        else:
            return 0

    def dangerPositionFromShip(self, spaceshipPosition: (int, int), lasersPositions: [(int, int)]) -> []:

        coverStraight = 0
        coverRight = 0
        coverLeft = 0

        # if len(lasersPositions) >= 2:
        #     print(lasersPositions)

        # for laserPosition in lasersPositions:
        #     if abs(laserPosition[0] - spaceshipPosition[0]) < 10:
        #         coverStraight = 1
        #     elif laserPosition[0] > spaceshipPosition[0]:
        #         coverRight = 1
        #     elif laserPosition[0] < spaceshipPosition[0]:
        #         coverLeft = 1

        if lasersPositions:
            laserPosition = lasersPositions[0]

            if abs(laserPosition[0] - spaceshipPosition[0]) < 10:
                coverStraight = 1
            elif laserPosition[0] > spaceshipPosition[0]:
                coverRight = 1
            elif laserPosition[0] < spaceshipPosition[0]:
                coverLeft = 1


        # todo sa-l fac sa returneze doar una dintre pozitii, cea mai apropiata
        return [coverStraight, coverRight, coverLeft]


    def enemyPositionFromShip(self, spaceshipPosition: (int, int), aliensPosition:[(int, int)]) -> []:

        enemyStraigth = 0
        enemyRight = 0
        enemyLeft = 0

        for alienPosition in aliensPosition:
            if abs(alienPosition[0] - spaceshipPosition[0]) < 10:
                enemyStraigth = 1
            elif alienPosition[0] > spaceshipPosition[0]:
                enemyRight = 1
            elif alienPosition[0] < spaceshipPosition[0]:
                enemyLeft = 1

        return [enemyStraigth, enemyRight, enemyLeft]

    def playGame(self):
        while True:

            # todo handle player or AI inputs
            if self.isAiPlaying:
                self.game.spaceship.performAction(self.computeNextAction())
            else:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RIGHT]:
                    self.game.spaceship.performAction(Action.RIGHT)
                elif keys[pygame.K_LEFT]:
                    self.game.spaceship.performAction(Action.LEFT)

                if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                    self.game.spaceship.performAction(Action.SHOOT)

            # event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == self.SHOT_LASER and self.game.run:
                    self.game.alienShotLaser()

                if event.type == self.MYSTERY_SHIP and not self.game.mysteryShipGroup.sprites() and self.game.run:
                    self.game.createMysteryShip()
                    pygame.time.set_timer(self.MYSTERY_SHIP, random.randint(10_000, 40_000))

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and not self.game.run:
                    self.game.reset()

            # updateing
            if self.game.run:
                self.game.spaceshipGroup.update()
                self.game.moveAliens()
                self.game.alienLasersGroup.update()
                self.game.mysteryShipGroup.update()
                self.game.checkForCollisions()
                self.game.checkLevelWasWon()

            if self.game.run and self.game.isAlienBelowSpaceShip():
                print("Game over due to aliens too low")
                self.game.gameOver()

            # draw objects on screen
            self.screen.fill(Colors.GRAY)
            pygame.draw.rect(self.screen, Colors.YELLOW, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)
            pygame.draw.line(self.screen, Colors.YELLOW, (25, 730), (775, 730), 3)
            if self.game.run:
                self.screen.blit(self.levelSurface, (570, 740, 50, 50))
            else:
                if self.game.hasWonLevel:
                    self.screen.blit(self.levelFinishedSurface, (540, 740, 50, 50))
                else:
                    self.screen.blit(self.gameOverSurface, (570, 740, 50, 50))

            for life in range(self.game.lives):
                self.screen.blit(self.game.spaceshipGroup.sprite.image, (50 + (life * 50), 745))

            self.screen.blit(self.scoreTextSurface, (50, 15, 50, 50))
            scoreSurface = self.font.render(str(self.game.score), False, Colors.YELLOW)
            self.screen.blit(scoreSurface, (50, 40, 50, 50))

            self.screen.blit(self.playerTextSurface, (600, 15, 50, 50))
            self.screen.blit(self.playerNameSurface, (600, 40, 50, 50))


            self.game.spaceshipGroup.draw(self.screen)
            self.game.spaceshipGroup.sprite.lasersGroup.draw(self.screen)
            for obstacle in self.game.obstacles:
                obstacle.blocksGroup.draw(self.screen)

            self.game.aliensGroup.draw(self.screen)
            self.game.alienLasersGroup.draw(self.screen)
            self.game.mysteryShipGroup.draw(self.screen)

            # updating positions
            pygame.display.update()
            self.clock.tick(60)


    def resetState(self):
        self.state = [0, 0, 0, 0, 0, 0, 0, 0]

    def convertAction(self, arr: []) -> Action:

        if arr[0] == 1:
            return Action.LEFT

        if arr[1] == 1:
            return Action.RIGHT

        return Action.SHOOT
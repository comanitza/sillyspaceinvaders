import pygame, random
from gameelements import Spaceship, Obstacle, grid, Alien, Laser, MysteryShip, Colors


class Game:
    def __init__(self, screenWidth, screeHeight, offset, includeObstacles=False, infinityMode=False):

        self.screenWidth = screenWidth
        self.screeHeight = screeHeight
        self.offset = offset
        self.includeObstacles = includeObstacles

        self.spaceship = Spaceship(screenWidth, screeHeight, offset)
        self.spaceshipGroup = pygame.sprite.GroupSingle()
        self.spaceshipGroup.add(self.spaceship)

        self.obstacles = self.createObstacles()

        self.aliensGroup = pygame.sprite.Group()

        if infinityMode:
            self.createSparseAliens()
        else:
            self.createAliens()

        self.aliensDirection = 1
        self.alienLasersGroup = pygame.sprite.Group()

        self.mysteryShipGroup = pygame.sprite.GroupSingle()

        self.lives = 3
        self.run = True
        self.hasWonLevel = False

        self.score = 0


    def createObstacles(self):
        if not self.includeObstacles:
            return []

        obstacleWidth = len(grid[0]) * 3
        gap = ((self.screenWidth + self.offset) - (4 * obstacleWidth)) / 5

        obstacles = []

        for i in range(4):
            offsetX = (i + 1) * gap + i * obstacleWidth
            obstacles.append(Obstacle(offsetX, self.screeHeight - 100))

        return obstacles


    def createAliens(self):
        for row in range(5):
            for col in range(11):
                x = (col * 55) + 75
                y = (row * 55) + 110

                type = 1

                if row == 0:
                    type = 3

                if row == 1 or row == 2:
                    type = 2


                self.aliensGroup.add(Alien(type, x + (self.offset / 2), y))


    def createSparseAliens(self):
        for row in range(4):
            for col in range(11):
                x = (col * 55) + 75
                y = (row * 55) + 110

                type = random.randint(1, 3)

                if random.randint(0, 100) > 60:
                    self.aliensGroup.add(Alien(type, x + (self.offset / 2), y))


    def moveAliens(self):
        self.aliensGroup.update(self.aliensDirection)

        alienSprites = self.aliensGroup.sprites()

        for alien in alienSprites:
            if alien.rect.x + alien.rect.width >= self.screenWidth + (self.offset / 2):
                self.aliensDirection = -1
                self.moveAliensDown(2)
            if alien.rect.x <= self.offset / 2:
                self.aliensDirection = 1
                self.moveAliensDown(2)


    def moveAliensDown(self, distance):
        if self.aliensGroup:
            for alien in self.aliensGroup.sprites():
                alien.rect.y += distance


    def alienShotLaser(self):
        if self.aliensGroup.sprites():
            alien = random.choice(self.aliensGroup.sprites())

            self.alienLasersGroup.add(Laser(alien.rect.center, -4, self.screeHeight, Colors.GREEN))


    def createMysteryShip(self):
        self.mysteryShipGroup.add(MysteryShip(self.screenWidth, self.offset))

    def checkForCollisions(self):
        # spaceship lasers
        if self.spaceshipGroup.sprite.lasersGroup:
            for laser in self.spaceshipGroup.sprite.lasersGroup:
                aliensHit = pygame.sprite.spritecollide(laser, self.aliensGroup, True)

                if aliensHit:
                    laser.kill()

                for alien in aliensHit:
                    self.score += int(100 * alien.type)

                if pygame.sprite.spritecollide(laser, self.mysteryShipGroup, True):
                    laser.kill()
                    self.score += 1000

                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laser, obstacle.blocksGroup, True):
                        laser.kill()


        # aliens lasers

        if self.alienLasersGroup:
            for laser in self.alienLasersGroup:
                if pygame.sprite.spritecollide(laser, self.spaceshipGroup, False):
                    laser.kill()

                    self.lives -= 1

                    if self.lives <= 0:
                        self.gameOver()

                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laser, obstacle.blocksGroup, True):
                        laser.kill()

        if self.aliensGroup:
            for alien in self.aliensGroup:
                for obstacle in self.obstacles:
                    pygame.sprite.spritecollide(alien, obstacle.blocksGroup, True)

                if pygame.sprite.spritecollide(alien, self.spaceshipGroup, False):
                    self.lives -= 1

                    if self.lives <= 0:
                        self.gameOver()



    def gameOver(self):
        print("Game Over :( press ESC to restart")
        self.run = False

    def checkLevelWasWon(self):
        if not self.hasWonLevel and not self.aliensGroup:
            self.hasWonLevel = True
            self.run = False
            print("Level was won!")

    def addFreshAliensIFNeeded(self):
        if self.run and len(self.aliensGroup) <= 5:
            self.createSparseAliens()

    def reset(self):
        self.lives = 3

        self.spaceship.reset()
        self.aliensGroup.empty()
        self.alienLasersGroup.empty()
        self.mysteryShipGroup.empty()

        self.createAliens()
        self.obstacles = self.createObstacles()

        self.run = True
        self.hasWonLevel = False

        self.score = 0

    def isGameRunning(self):
        return self.run

    def isAlienBelowSpaceShip(self) -> bool:

        aliensPosition = list(map(lambda s: (s.rect.x, s.rect.y), self.aliensGroup.sprites()))
        spaceshipPosition = (self.spaceship.rect.x, self.spaceship.rect.y)

        for alien in aliensPosition:
            if alien[1] >= spaceshipPosition[1]:
                return True

        return False
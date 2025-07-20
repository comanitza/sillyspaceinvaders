# space invaders stuff
# https://youtu.be/PFMoo_dvhyw?t=7424

import pygame
import sys, random
from gameelements import Spaceship, Obstacle
from game import Game

from utils import Colors

class GameRunner:

    def __init__(self):
        SCREEN_WIDTH = 750
        SCREEN_HEIGHT = 700
        OFFSET = 50

        pygame.init()

        self.font = pygame.font.Font(None, 40)
        self.levelSurface = self.font.render("LEVEL 01", False, Colors.YELLOW)
        self.gameOverSurface = self.font.render("GAME OVER", False, Colors.YELLOW)
        self.scoreTextSurface = self.font.render("SCORE", False, Colors.YELLOW)
        self.playerTextSurface = self.font.render("PLAYER", False, Colors.YELLOW)
        self.playerNameSurface = self.font.render("STEFANITA", False, Colors.YELLOW)
        self.levelFinishedSurface = self.font.render("LEVEL FINISHED", False, Colors.YELLOW)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT + (2 * OFFSET)))
        pygame.display.set_caption("Silly Space Invaders")

        self.clock = pygame.time.Clock()

        self.game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET)
        self.SHOT_LASER = pygame.USEREVENT
        pygame.time.set_timer(self.SHOT_LASER, 1200)

        self.MYSTERY_SHIP = pygame.USEREVENT + 1
        pygame.time.set_timer(self.MYSTERY_SHIP, random.randint(10_000, 40_000))


    def playGame(self):
        while True:
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

print("starting silly space invaders")

runner = GameRunner()
runner.playGame()

print("### ok, all done")
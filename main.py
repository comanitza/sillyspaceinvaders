# space invaders stuff
# https://youtu.be/PFMoo_dvhyw?t=7424

import pygame
import sys, random
from gameelements import Spaceship, Obstacle
from game import Game

from utils import Colors

print("starting silly space invaders")

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 700
OFFSET = 50

pygame.init()

font = pygame.font.Font(None, 40)
levelSurface = font.render("LEVEL 01", False, Colors.YELLOW)
gameOverSurface = font.render("GAME OVER", False, Colors.YELLOW)
scoreTextSurface = font.render("SCORE", False, Colors.YELLOW)
playerTextSurface = font.render("PLAYER", False, Colors.YELLOW)
playerNameSurface = font.render("STEFANITA", False, Colors.YELLOW)
levelFinishedSurface = font.render("LEVEL FINISHED", False, Colors.YELLOW)

screen = pygame.display.set_mode((SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT + (2 * OFFSET)))
pygame.display.set_caption("Silly Space Invaders")

clock = pygame.time.Clock()

game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET)
SHOT_LASER = pygame.USEREVENT
pygame.time.set_timer(SHOT_LASER, 1200)

MYSTERY_SHIP = pygame.USEREVENT + 1
pygame.time.set_timer(MYSTERY_SHIP, random.randint(10_000, 40_000))


while True:
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SHOT_LASER and game.run:
            game.alienShotLaser()

        if event.type == MYSTERY_SHIP and not game.mysteryShipGroup.sprites() and game.run:
            game.createMysteryShip()
            pygame.time.set_timer(MYSTERY_SHIP, random.randint(10_000, 40_000))

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and not game.run:
            game.reset()

    # updateing
    if game.run:
        game.spaceshipGroup.update()
        game.moveAliens()
        game.alienLasersGroup.update()
        game.mysteryShipGroup.update()
        game.checkForCollisions()
        game.checkLevelWasWon()

    # draw objects on screen
    screen.fill(Colors.GRAY)
    pygame.draw.rect(screen, Colors.YELLOW, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)
    pygame.draw.line(screen, Colors.YELLOW, (25, 730), (775, 730), 3)
    if game.run:
        screen.blit(levelSurface, (570, 740, 50, 50))
    else:
        if game.hasWonLevel:
            screen.blit(levelFinishedSurface, (540, 740, 50, 50))
        else:
            screen.blit(gameOverSurface, (570, 740, 50, 50))

    for life in range(game.lives):
        screen.blit(game.spaceshipGroup.sprite.image, (50 + (life * 50), 745))

    screen.blit(scoreTextSurface, (50, 15, 50, 50))
    scoreSurface = font.render(str(game.score), False, Colors.YELLOW)
    screen.blit(scoreSurface, (50, 40, 50, 50))

    screen.blit(playerTextSurface, (600, 15, 50, 50))
    screen.blit(playerNameSurface, (600, 40, 50, 50))


    game.spaceshipGroup.draw(screen)
    game.spaceshipGroup.sprite.lasersGroup.draw(screen)
    for obstacle in game.obstacles:
        obstacle.blocksGroup.draw(screen)

    game.aliensGroup.draw(screen)
    game.alienLasersGroup.draw(screen)
    game.mysteryShipGroup.draw(screen)

    # updating positions
    pygame.display.update()
    clock.tick(60)

print("### ok, all done")
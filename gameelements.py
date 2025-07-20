import random

import pygame
from utils import Colors


from enum import Enum

class Action(Enum):
    LEFT = 1
    RIGHT = 2
    SHOOT = 3
    STAY = 4


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, screenWidth, screenHeight, offset, isAiPlayer = False):
        super(Spaceship, self).__init__()

        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.offset = offset

        self.image = pygame.image.load("resources/spaceship.png")
        self.rect = self.image.get_rect(midbottom=((screenWidth + offset) / 2, screenHeight))

        self.speed = 6

        self.lasersGroup = pygame.sprite.Group()
        self.laserReady = True
        self.laserTime = 0
        self.laserDelay = 300

        self.actions = []
        self.isAiPlayer = isAiPlayer


    def performAction(self, action: Action):
        self.actions.append(action)

    # todo aici trebuie sa schimb
    # todo fac metode de move si le chem din runner
    def getUserInput(self):
        actions = self.actions
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            if self.laserReady:
                self.lasersGroup.add(Laser(self.rect.center, 5, self.screenHeight))
                self.laserReady = False
                self.laserTime = pygame.time.get_ticks()


        self.actions.clear() # clear all


    def update(self):
        self.getUserInput()
        self.constraintMovement()
        self.lasersGroup.update()

        self.rechargeLaser()


    def constraintMovement(self):
        if self.rect.right > self.screenWidth:
            self.rect.right = self.screenWidth

        if self.rect.left < self.offset:
            self.rect.left = self.offset


    def rechargeLaser(self):
        if not self.laserReady:
            currentTime = pygame.time.get_ticks()
            if currentTime - self.laserTime >= 300:
                self.laserReady = True


    def reset(self):
        self.rect = self.image.get_rect(midbottom=((self.screenWidth + self.offset) / 2, self.screenHeight))
        self.lasersGroup.empty()


class Laser(pygame.sprite.Sprite):
    def __init__(self, position, speed, screenHeight, color = Colors.YELLOW):
        super(Laser, self).__init__()

        self.image = pygame.Surface((4, 15))
        self.image.fill(color)
        self.rect = self.image.get_rect(center = position)

        self.speed = speed
        self.screenHeight = screenHeight


    def update(self):
        self.rect.y -= self.speed

        if self.rect.y > self.screenHeight + self.rect.height or self.rect.y < 0:
            self.kill()


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Block, self).__init__()

        self.image = pygame.Surface((3, 3))
        self.image.fill(Colors.YELLOW)
        self.rect = self.image.get_rect(topleft = (x, y))


grid = [
[0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
[0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
[0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1],
[1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],
[1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1]]

class Obstacle:
    def __init__(self, x, y):
        self.blocksGroup = pygame.sprite.Group()

        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col]:
                    block_x = x + col * 3
                    block_y = y + row * 3
                    self.blocksGroup.add(Block(block_x, block_y))



class Alien(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        super(Alien, self).__init__()

        self.type = type
        self.path = f"resources/alien_{type}.png"

        self.image = pygame.image.load(self.path)
        self.rect = self.image.get_rect(topleft = (x, y))


    def update(self, direction):
        self.rect.x += direction


class MysteryShip(pygame.sprite.Sprite):
    def __init__(self, screenWidth, offset):
        super(MysteryShip, self).__init__()

        self.screenWidth = screenWidth
        self.offset = offset

        self.image = pygame.image.load("resources/mystery.png")
        x = random.choice([self.offset / 2, (screenWidth + (self.offset / 2)) - self.image.get_width()])
        self.rect = self.image.get_rect(topleft = (x, 40))

        self.speed = 2 if x == self.offset / 2 else -2


    def update(self):
        self.rect.x += self.speed

        if self.rect.x < self.offset / 2 or self.rect.x > self.screenWidth + (self.offset / 2):
            self.kill()



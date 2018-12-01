from Settings import *
from transitions import Machine
import pygame
import random


class Player(pygame.sprite.Sprite):
    states = ["Idle", "MoveLeft", "MoveRight"]

    def __init__(self, game):
        self.game = game

        # inherit Sprite
        pygame.sprite.Sprite.__init__(self)

        # load player image
        self.image = pygame.image.load("Tom.png")
        # scale image size
        self.image = pygame.transform.scale(self.image, (45, 60))
        # get the rectangle of the image
        self.rect = self.image.get_rect()
        # center image for start position
        self.rect.center = Vector2(screenWidth / 2, screenHeight / 2)

        # temp varable, for updata player position
        self.pos = Vector2(screenWidth / 2, screenHeight / 2)
        self.currentSpeed = Vector2(0, 0)
        self.accelerate = Vector2(0, 0)

        # State Machine
        self.machine = Machine(
            model=self, states=Player.states, initial='Idle')
        self.machine.add_transition(trigger='MouseIsLeft', source=[
                                    'Idle', "MoveLeft", "MoveRight"], dest='MoveLeft')
        self.machine.add_transition(trigger='MouseIsRight', source=[
                                    'Idle', "MoveLeft", "MoveRight"], dest='MoveRight')
        self.machine.add_transition(trigger='MouseIsMid', source=[
                                    'Idle', "MoveLeft", "MoveRight"], dest='Idle')

    def update(self):
        # Fall Down
        self.accelerate = Vector2(0, playerGravity)

        # Boost
        if(self.game.isBoost):
            self.currentSpeed.y = -playerJumpForce * 5
            self.game.isBoost = False

        # Player move triggers
        self.playerMove()

        # Player move states
        if self.state == "MoveLeft":
            self.accelerate.x = -playerAcc
        if self.state == "MoveRight":
            self.accelerate.x = playerAcc
        if self.state == "Idle":
            pass

        # horizontal accelerate
        self.accelerate.x -= self.currentSpeed.x * playerFriction

        # current Speed
        self.currentSpeed += self.accelerate

        # updata player temp position
        self.pos += self.currentSpeed + 0.5 * self.accelerate

        # wayPoint
        if self.pos.x > screenWidth:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = screenWidth

        # adjust player position
        self.rect.midbottom = self.pos

    def playerMove(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        if mouseX < screenWidth / 2 - 20:
            self.MouseIsLeft()
        elif mouseX > screenWidth / 2 + 20:
            self.MouseIsRight()
        else:
            self.MouseIsMid()

    # jump function 
    def jump(self):
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        if hits:
            if not (self.game.isBoost):
                self.currentSpeed.y = -playerJumpForce


class Platforms(pygame.sprite.Sprite):

    def __init__(self, x, y, w, h, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class PowerUp(pygame.sprite.Sprite):

    def __init__(self, platform, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.platform = platform
        self.imageList=["PowerUp.png","Boost.png","Candy.png"]

        # load Power up image
        self.image = pygame.image.load(random.choice(self.imageList))
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.platform.rect.centerx
        # intialize the powerup's position
        self.rect.bottom = self.platform.rect.top - 5

    def update(self):
        # adjust the powerup's position
        self.rect.bottom = self.platform.rect.top - 5
        # delete the candies when the platform was destroyed
        if not self.game.platforms.has(self.platform):
            self.kill()

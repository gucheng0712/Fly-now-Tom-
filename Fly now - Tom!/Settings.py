import pygame
# Game options/settings
screenWidth = 480
screenHeight = 600
title = "Fly now, Tom!"
FPS = 60
Vector2 = pygame.math.Vector2
# Player Properties
playerJumpForce = 25
playerAcc = 1.2
playerGravity = 1
playerFriction = 0.15


# DefineColors
white = (255, 255, 255)
black = (0, 0, 0)
red = (220, 30, 30)
green = (22, 255, 166)
blue = (66, 134, 244)
yellow = (255, 255, 0)
cyan = (0, 255, 255)
megenta = (219, 30, 118)
indigo = (125, 30, 219)
brown = (168, 112, 23)
colorArray = [white, red, green, blue, yellow, cyan, megenta, indigo, brown]

# Starting Platforms
platformList = [(0, screenHeight - 40, screenWidth, 40, white),
                (screenWidth / 2 - 50, screenHeight * 3 / 4, 100, 20, red),
                (125, screenHeight - 350, 100, 20, blue),
                (350, 200, 100, 20, green),
                (175, 100, 50, 20, cyan)
                ]

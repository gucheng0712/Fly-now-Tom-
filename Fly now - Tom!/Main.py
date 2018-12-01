import pygame
import random
import sys
from Settings import *
from Sprites import *
from transitions import Machine


class Game:
    states = ["Start", "Playing", "Die"]

    def __init__(self):
        # initialize pygame and create window
        pygame.init()
        self.screen = pygame.display.set_mode((screenWidth, screenHeight))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()

        # State Machine
        self.machine = Machine(model=self, states=Game.states, initial="Start")
        self.machine.add_transition(
            trigger="PressEnter", source="Start", dest="Playing")
        self.machine.add_transition(
            trigger="FallOver", source="Playing", dest="Die")

        # Rocket Image
        self.rocketImg = pygame.image.load("Rocket.png")
        self.rocketImg = pygame.transform.scale(self.rocketImg, (45, 60))
        self.rocketImgRect = self.rocketImg.get_rect()
        self.isBoost = False

        # Sound
        self.startSound = pygame.mixer.Sound("Start.ogg")
        self.jumpSound = pygame.mixer.Sound("Jump.ogg")
        self.superJumpSound = pygame.mixer.Sound("SuperJump.ogg")
        self.gameOverSound = pygame.mixer.Sound("GameOver.ogg")
        self.isPlayed = False

    def start(self):
        # start a new game
        self.score = 0

        #Sprite Groups
        self.platforms = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.allSprites = pygame.sprite.Group()

        # Platform List
        for platform in platformList:
            p = Platforms(*platform)
            self.allSprites.add(p)
            self.platforms.add(p)

        # Player Instance
        self.player = Player(self)
        self.allSprites.add(self.player)

    def running(self):
        self.clock.tick(FPS)
        self.events()
        self.update()
        self.draw()

    def update(self):

        if(self.state == "Playing"):
            self.allSprites.update()
            self.platformGenerator()
            self.playerUpdate()

    def playerUpdate(self):

        # make the rocket image a little higher than player image
        self.rocketImgRect.center = self.player.rect.midtop

        # Collide function
        self.collidePlatform()
        self.collidePowerUp()


        # if player reaches top 1/4 of screen, destroy the platform
        # add score
        if self.player.rect.top <= screenHeight / 4:
            self.player.pos.y += abs(self.player.currentSpeed.y)
            for platform in self.platforms:
                platform.rect.y += abs(self.player.currentSpeed.y)
                if(platform.rect.top >= screenHeight):
                    platform.kill()
                    self.score += 50

        # if player's position is lower than screen, then please die
        if(self.player.rect.bottom > screenHeight + 100):
            self.FallOver()

    # Collide with platform
    def collidePlatform(self):
        if(self.player.currentSpeed.y > 0):
            hits = pygame.sprite.spritecollide(
                self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.currentSpeed.y = 0
                self.player.jump()
                self.jumpSound.play()

    # Collide with PowerUp
    def collidePowerUp(self):
        hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
        if hits:
            if(self.player.currentSpeed.y > -25):
                self.isBoost = True
                self.superJumpSound.play()

    # generate platform
    def platformGenerator(self):
        # Spawn new platforms to keep same average number
        while len(self.platforms) < 7:

            # random width of the platforms 
            width = random.randrange(50, 100)
            # Make the platform not too close
            newWidth=0
            while(newWidth-width)>10 or (newWidth-width)<-10:
                newWidth=width
            p = Platforms(random.randrange(0, screenWidth - newWidth),
                          random.randrange(-75, -30),
                          newWidth, 20, random.choice(colorArray))
            # add them into the sprite group
            self.platforms.add(p)
            self.allSprites.add(p)

            # 10% chance to spawn power up
            if(random.randrange(10) == 1):
                powerUp = PowerUp(p, self)
                self.powerups.add(powerUp)
                self.allSprites.add(powerUp)

    def events(self):
        # Process input(events)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if(self.state == "Start"):
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.PressEnter()
                        self.startSound.play()

    def draw(self):
        # Draw background
        self.screen.fill(black)

        # Draw Rocket
        if(self.player.currentSpeed.y < 0):
            self.screen.blit(self.rocketImg, self.rocketImgRect)

        # Draw Sprites
        self.allSprites.draw(self.screen)

        # When die Play Sound(make it not repeat)
        # draw death menu texts
        if(self.state == "Die"):
            if not (self.isPlayed):
                self.gameOverSound.play()
                self.isPlayed = True

            self.drawText("Game Over", 60, white, screenWidth /
                          2, screenHeight / 2 - 200)
            self.drawText("Score", 50, yellow, screenWidth /
                          2, screenHeight / 2 - 60)
            self.drawText(str(self.score), 50, white,
                          screenWidth / 2, screenHeight / 2)
        # Updata scores
        else:
            self.drawText("Score", 30, yellow, screenWidth / 2, 20)
            self.drawText(str(self.score), 32, white, screenWidth / 2, 40)

        # after drawing update the display
        pygame.display.update()

        
    def drawText(self, text, size, color, x, y):
        font = pygame.font.SysFont("Arial", size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


game = Game()
game.start()
while True:
    game.running()

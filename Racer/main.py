# Imports
import pygame, sys
from pygame.locals import *
import random
import os

# Initialize pygame
pygame.init()
base_path = os.path.dirname(__file__)
img_path1 = os.path.join(base_path, "AnimatedStreet.png")
img_path2 = os.path.join(base_path, "Coin.png")
img_path3 = os.path.join(base_path, "Enemy.png")
img_path4 = os.path.join(base_path, "Player.png")
# FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Colors
RED   = (255, 0, 0)
BLACK = (0, 0, 0)

# Screen
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
DISPLAYSURF = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Game")

# Game variables
SPEED = 5
SCORE = 0
COINS_COLLECTED = 0

# Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)

# Background
background = pygame.image.load(img_path1)

# Game state
game_state = "PLAYING"
game_over_time = 0


#  ENEMY 
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(img_path3)
        self.image = pygame.transform.scale(self.image, (120, 60))
        self.image = pygame.transform.rotate(self.image, 90)

        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE

        self.rect.move_ip(0, SPEED)

        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


#  PLAYER 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(img_path4)
        self.image = pygame.transform.scale(self.image, (120, 60))
        self.image = pygame.transform.rotate(self.image, 90)

        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)

        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)


#  COIN 
class Coin(pygame.sprite.Sprite):
    def __init__(self, enemies):
        super().__init__()
        self.image = pygame.image.load(img_path2)
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.enemies = enemies
        self.spawn()

    def spawn(self):
        while True:
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
            if not pygame.sprite.spritecollideany(self, self.enemies):
                break

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.spawn()


#  OBJECTS 
P1 = Player()
E1 = Enemy()

enemies = pygame.sprite.Group()
enemies.add(E1)

C1 = Coin(enemies)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

# Speed increase event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)


#  GAME LOOP 
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == INC_SPEED and game_state == "PLAYING":
            SPEED += 0.5

    #  PLAYING 
    if game_state == "PLAYING":

        DISPLAYSURF.blit(background, (0, 0))

        score_text = font_small.render("Score: " + str(SCORE), True, BLACK)
        coin_text = font_small.render("Coins: " + str(COINS_COLLECTED), True, BLACK)

        DISPLAYSURF.blit(score_text, (10, 10))
        DISPLAYSURF.blit(coin_text, (250, 10))

        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)
            entity.move()

        # Coin collision
        if pygame.sprite.spritecollideany(P1, coins):
            COINS_COLLECTED += 1
            for coin in coins:
                coin.spawn()

        # Enemy collision → GAME OVER
        if pygame.sprite.spritecollideany(P1, enemies):
            game_state = "GAME_OVER"
            game_over_time = pygame.time.get_ticks()

    # GAME OVER 
    else:

        DISPLAYSURF.fill(RED)

        text = font.render("Game Over", True, BLACK)
        DISPLAYSURF.blit(text, (30, 200))

        score_text = font_small.render("Score: " + str(SCORE), True, BLACK)
        coin_text = font_small.render("Coins: " + str(COINS_COLLECTED), True, BLACK)

        DISPLAYSURF.blit(score_text, (150, 300))
        DISPLAYSURF.blit(coin_text, (150, 330))

        # hold screen for 5 seconds 
        if pygame.time.get_ticks() - game_over_time > 5000:
            pygame.quit()
            sys.exit()

        # quiting by yourself
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)
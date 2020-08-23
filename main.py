import pygame
import random
import math
from pygame import mixer

# Initializes pygame
pygame.init()

# Creates the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background1.png')

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Makes title & icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')  # Creates variable icon
pygame.display.set_icon(icon)  # Displays icon

# Player location
playerImg = pygame.image.load('spaceplayer.png')
playerX = 370
playerY = 480
playerX_change = 0

# Invader enemy location
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

# Makes multiple enemies
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('invader.png'))
    enemyX.append(random.randint(0, 735))  # Random x location
    enemyY.append(random.randint(50, 150))  # Random y location
    enemyX_change.append(3)
    enemyY_change.append(40)

# Bullet

# Ready state - can't see bullet on screen
# Fire state - bullet currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 4
bulletY_change = 10
bullet_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


# Makes player move
def player(x, y):
    screen.blit(playerImg, (x, y))  # Draws image on screen


# Makes enemy invader move
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))  # Draws image on screen


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


# Checks if collision
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game running loop
running = True
while running:

    screen.fill((0, 0, 0))  # Changes background color (RGB)
    # Background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Checks if closed button pressed (only exits if closed button pressed)
            running = False

        # If keystroke is pressed, check whether right or left
        if event.type == pygame.KEYDOWN:  # Key is being pressed (not released)
            if event.key == pygame.K_LEFT:  # If left arrow pressed
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX  # Saves x-coordinate so bullet doesn't move with spaceship
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    # Sets boundaries of spaceship
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Checks boundaries of enemy movement
    for i in range(num_of_enemies):
        # Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000  # Enemies moved off screen
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1  # Increases score when hit enemy
            enemyX[i] = random.randint(0, 735)  # Enemy goes to random location when hit
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()  # Always need to update display window

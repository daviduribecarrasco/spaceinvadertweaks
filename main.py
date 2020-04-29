import math
import random

import pygame
from pygame import mixer

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800
, 600))

# Background
background = pygame.image.load("background.png")
# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('special.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

#Special Alien

specialImg = []
specialX = []
specialY = []
specialX_change = []
specialY_change = []
num_of_special = 3

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 8






for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(i * 100)
    enemyY.append(0)
    enemyX_change.append(4)
    enemyY_change.append(40)


for i in range(num_of_special):
    specialImg.append(pygame.image.load('specialboss.png'))
    specialX.append(random.randint(0, 736))
    specialY.append(random.randint(50, 150))
    specialX_change.append(4)
    specialY_change.append(40)


# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

rocketImg = pygame.image.load('bomb.png')
rocketX = 0
rocketY = specialY[i]
rocketX_change = 0
rocketY_change = 8
rocket_state = "ready"

strikeImg = pygame.image.load('sad.png')
strikeX = 10
strikeY = 450


# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))




def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))

def special_alien(x, y, i):
    screen.blit(specialImg[i], (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def fire_rocket(x, y):
    global rocket_state
    rocket_state = "fire"
    screen.blit(rocketImg, (x + 16 , y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

def bossCollision(specialX, specialY, bulletX, bulletY):
    distance = math.sqrt(math.pow(specialX - bulletX, 2) + (math.pow(specialY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

def playerHit(playerX,playerY,rocketX,rocketY):
    distance = math.sqrt(math.pow(rocketX- playerX, 2) + (math.pow(rocketY - playerY, 2)))
    if distance < 35:
        return True
    else:
        return False

def danger_alert():
    mixer.music.load("alert.wav")
    mixer.music.play(1) 


# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement

    danger = False
    for i in range(num_of_enemies):

        if enemyY[i] > 350:
            danger = True

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
                
            game_over_text()
            danger = False
            
            
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i] 

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)
    
    for i in range(num_of_special):

        # Game Over
        if specialY[i] > 350:
            danger = True
        if specialY[i] > 440:
            for j in range(num_of_special):
                specialY[j] = 2000
                enemyY[i]= 2000
            game_over_text()
            danger = False
            
            
            break

        specialX[i] += specialX_change[i]
        if specialX[i] <= 0:
            specialX_change[i] = 4
            specialY[i] += specialY_change[i]
        if specialX[i] <= playerX + 5 and specialX[i] >= playerX - 5:
            for k in range(num_of_special):
                rocket_state = "ready"
                rocketX = specialX[i]
                rocketY = specialY[i]
                fire_rocket(rocketX,rocketY)


        elif specialX[i] >= 736:
            specialX_change[i] = -4
            specialY[i] += specialY_change[i]

        # Collision
        collision = bossCollision(specialX[i], specialY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            specialX[i] = random.randint(0, 736)
            specialY[i] = random.randint(50, 150)

        special_alien(specialX[i], specialY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    
    if rocketY <= 0:
        rocketY = 0
        rocket_state = "ready"

    if rocket_state is "fire":
        fire_rocket(rocketX, rocketY)
        rocketY += rocketY_change

    if danger == True:
        danger_alert()
    
    hit_counter = 0
    hit = playerHit(playerX,playerY,rocketX,rocketY)
    if hit:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            rocketY = 0
            rocket_state = "ready"
            hit_counter += 1
            if hit_counter <=3:
                enemyY[i] = 2000
                specialY [i] = 2000
                game_over_text() 
                danger = False

                               
                


    

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()

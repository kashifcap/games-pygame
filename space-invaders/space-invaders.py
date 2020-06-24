import pygame
from pygame import mixer
import random
import math


# Start screen display
def start_screen(START_SCREEN, SCREEN, font):
    SCREEN.blit(START_SCREEN, (0 , 0))
    game_start = font.render("PRESS ENTER TO START GAME", True, (255, 255, 255))
    SCREEN.blit(game_start, (150, 480))

# gameover display
def gameoverfunc(SCREEN, gameover_font):
    SCREEN.blit(gameover_font, (150, 200))

# player display 
def player(SCREEN, PLAYER, x , y):
    SCREEN.blit(PLAYER, (x, y))

# bullet display
def bulletfunc(SCREEN, BULLET, x, y):
    SCREEN.blit(BULLET, (x, y))

# alien display
def enemyfunc(SCREEN, ENEMY, x, y):
    SCREEN.blit(ENEMY, (x, y))

# collision checker
def iscollision(bullet_x, bullet_y, enemy_x, enemy_y):
    distance = math.sqrt(pow((bullet_x+16) - (enemy_x+32),2) + pow((bullet_y+16) - (enemy_y+32),2))
    if distance <= 30:
        return True
    return False


# main driver function
def main():
    pygame.init()
    SCREEN = pygame.display.set_mode((800,600))
    pygame.display.set_caption('Space Invaders')
    START_SCREEN = pygame.image.load('games-pygame/space-invaders/background.png')
    PLAYER = pygame.image.load('games-pygame/space-invaders/space-invaders.png')
    BACKGROUND_IMG = pygame.image.load('games-pygame/space-invaders/back.png')
    BULLET = pygame.image.load('games-pygame/space-invaders/bullet.png')
    ENEMY = pygame.image.load('games-pygame/space-invaders/alien.png')
    font = pygame.font.Font('freesansbold.ttf', 32)
    score_font = pygame.font.Font('freesansbold.ttf', 32)
    gameover_font = pygame.font.Font('freesansbold.ttf', 64)
    score = 0
    best_score = 0


    # player properties
    player_x = 380
    player_y = 480
    player_x_inc = 0

    # enemy properties
    enemy_x = []
    enemy_y = []
    enemy_x_inc = []
    enemy_y_inc = []
    number_of_enemy = 5
    for i in range(number_of_enemy):
        enemy_x.append(random.randint(0, 735))
        enemy_y.append(random.choice([0, 64]))
        enemy_x_inc.append(random.choice([-3, 3]))
        enemy_y_inc.append(64)


    # bullet properties
    bullet_x = 0
    bullet_y = 475
    bullet_y_inc = -5
    bullet_state = False

    running = True
    game_status = 'start'


    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_status = 'playing'
                    mixer.music.load('games-pygame/space-invaders/backgroundsound.wav')
                    mixer.music.play(-1)
                if event.key == pygame.K_LEFT:
                    player_x_inc = -5
                if event.key == pygame.K_RIGHT:
                    player_x_inc = 5
                if event.key == pygame.K_SPACE:
                    if bullet_state == False:
                        bullet_state = True
                        bullet_x = player_x + 19
                        bullet_y = 475
                        bullet_sound = mixer.Sound('games-pygame/space-invaders/shoot.wav')
                        bullet_sound.play()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_x_inc = 0 
        
        # If game is starting 
        if game_status == 'start':
            start_screen(START_SCREEN, SCREEN, font)

        # if game has started
        elif game_status == 'playing':
            SCREEN.blit(BACKGROUND_IMG, (0, 0))

            score_font_b = score_font.render("Score: " + str(score), True, (255, 255, 255))
            SCREEN.blit(score_font_b, (0, 0))
            
            for i in range(number_of_enemy):
                if enemy_y[i] > 440:
                    game_status = 'Game over'
                    best_score = score
                    score = 0

                if iscollision(bullet_x, bullet_y, enemy_x[i], enemy_y[i]) and bullet_state:
                    collision_sound = mixer.Sound('games-pygame/space-invaders/explosion.wav')
                    collision_sound.play()
                    bullet_state = False
                    enemy_x[i]  = random.randint(0, 735)
                    enemy_y[i] = random.choice([0, 64])
                    score +=1
                    
                    
                enemy_x[i] += enemy_x_inc[i]
                if enemy_x[i] < 0 or enemy_x[i] > 736:
                    enemy_y[i] += enemy_y_inc[i]
                    enemy_x_inc[i] = -(enemy_x_inc[i])
                enemyfunc(SCREEN, ENEMY, enemy_x[i], enemy_y[i])

                
            if bullet_state:
                bullet_y += bullet_y_inc
                if bullet_y < 0:
                    bullet_state = False
                bulletfunc(SCREEN, BULLET, bullet_x, bullet_y)
            if 0 < player_x + player_x_inc < 736:
                player_x += player_x_inc
            player(SCREEN, PLAYER, player_x, player_y)
        
            
                
        
        #game over
        else:
            SCREEN.blit(BACKGROUND_IMG, (0, 0))
            gameover_font_b = gameover_font.render("GAME OVER", True, (255,255,255))
            gameoverfunc(SCREEN, gameover_font_b)
        
        pygame.display.update()


if __name__ == "__main__":
    main()
import pygame
import random
import time

pygame.init()

screen = pygame.display.set_mode((800, 600))
running = True

#player a
player_a_x = 15
player_a_y = 250
player_a_y_inc = 0
player_a_score = 0
player_a_font = pygame.font.Font('freesansbold.ttf', 15)

# player b
player_b_x = 765
player_b_y = 250
player_b_y_inc = 0
player_b_score = 0
player_b_font = pygame.font.Font('freesansbold.ttf', 15)

# ball
ball_x = 400
ball_y = 300
ball_x_inc = random.choice([-1, 1])
ball_y_inc = random.choice([-1, 1])


# redrawing screen
def redraw():
    screen.fill((0, 0, 0))
    pygame.draw.line(screen, (255,255,255), (0,30), (800, 30))
    player_1 = player_a_font.render("Player 1 : " + str(player_a_score), True, (255, 255, 255))
    player_2 = player_b_font.render("Player 2 : " + str(player_b_score), True, (255, 255, 255))
    screen.blit(player_1, (150, 10))
    screen.blit(player_2, (550, 10))
    pygame.draw.rect(screen, (255, 255, 255), (player_a_x, player_a_y, 20, 100))
    pygame.draw.rect(screen, (255, 255, 255), (player_b_x, player_b_y, 20, 100))
    pygame.draw.circle(screen, (255, 255, 255), (ball_x, ball_y), 10)
    pygame.display.update()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player_a_y_inc = -1
            if event.key == pygame.K_s:
                player_a_y_inc = 1
            if event.key == pygame.K_UP:
                player_b_y_inc = -1
            if event.key == pygame.K_DOWN:
                player_b_y_inc = 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                player_a_y_inc = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player_b_y_inc = 0

    if 32 < player_a_y + player_a_y_inc < 495:
        player_a_y += player_a_y_inc
    
    if 32 < player_b_y + player_b_y_inc < 495:
        player_b_y += player_b_y_inc

    if ball_y + ball_y_inc < 40 or ball_y + ball_y_inc > 590:
        ball_y_inc = -(ball_y_inc)
    
    if ball_x == player_a_x + 15 and player_a_y < ball_y < player_a_y + 100:
        ball_x_inc = -(ball_x_inc)
    
    if ball_x == player_b_x - 15 and player_b_y< ball_y < player_b_y + 100:
        ball_x_inc = -(ball_x_inc)
    
    if ball_x < 0:
        player_b_score += 1
        ball_x = 400
        ball_y = 300
        ball_x_inc = -(ball_x_inc)
        ball_y_inc = random.choice([-1, 1])
    
    if ball_x > 800:
        player_a_score += 1
        ball_x = 400
        ball_y = 300
        ball_x_inc = -(ball_x_inc)
        ball_y_inc = random.choice([-1, 1])


    ball_x += ball_x_inc
    ball_y += ball_y_inc

    redraw()
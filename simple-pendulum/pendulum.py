import pygame
import math

pygame.init()

centre = (300,150)

start_x = 130
start_y = 500
start_font = pygame.font.Font('freesansbold.ttf', 30)
start = start_font.render("Start", True, (0, 0, 0))

stop_x = 400
stop_y = 500
stop_font = pygame.font.Font('freesansbold.ttf', 30)
stop = stop_font.render("Stop", True, (0, 0, 0))

def move(bob_x, bob_y, angle, angle_inc):
    if angle <= 0 or angle >= 180:
        angle_inc = -(angle_inc)
    
    if angle > 90:
        bob_x = centre[0] + (250 * math.cos(math.radians(180 - angle)))
        bob_y = centre[1] + (250 * math.sin(math.radians(180 - angle)))

    elif angle <= 90:
        bob_x = centre[0] - (250 * math.cos(math.radians(angle)))
        bob_y = centre[1] + (250 * math.sin(math.radians(angle)))

    angle += angle_inc

    return int(bob_x), int(bob_y), angle, angle_inc


def drawdiag(screen, bob_x, bob_y):
    pygame.draw.line(screen, (0, 0, 0), (centre[0], centre[1]), (bob_x, bob_y), 5)
    pygame.draw.circle(screen, (255, 0, 0), (bob_x, bob_y), 30)

def redrawscreen(screen, bob_x, bob_y):
    screen.fill((255, 255, 255))
    drawdiag(screen, bob_x, bob_y)
    screen.blit(start, (start_x, start_y))
    screen.blit(stop, (stop_x, stop_y))
    pygame.display.update()


def main():
    width = 600
    screen = pygame.display.set_mode((width, width))
    running = True

    bob_x = 300
    bob_y = 400
    angle = 90
    angle_inc = 1

    state = 'running'

    clock = pygame.time.Clock()

    while running:
        clock.tick(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if start_x < x < start_x + 80 and start_y < y < start_y + 80:
                    state = 'running'
                if stop_x < x < stop_x + 30 and stop_y < y < stop_y + 30:
                    state = 'stop'

        
        if state == 'running':
            redrawscreen(screen, bob_x, bob_y)
            bob_x, bob_y, angle, angle_inc = move(bob_x, bob_y, angle, angle_inc)

main()
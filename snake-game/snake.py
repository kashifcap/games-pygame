import pygame
import random

class cube(object):
    def __init__(self, start, color = (255, 255, 255)):
        self.pos = start
        self.color = color
        self.dirx = 1
        self.diry = 0
    
    def move(self, dirx, diry):
        self.dirx = dirx
        self.diry = diry
        self.pos = (self.pos[0] + self.dirx, self.pos[1] + self.diry)

    def draw(self, screen):
        dist = width // rows
        pygame.draw.rect(screen, self.color, (self.pos[0]*dist + 1, self.pos[1]*dist + 1, dist - 2, dist - 2))
        

class snake(object):
    body = []
    turns = {}
    def __init__(self, pos):
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirx = 0
        self.diry = 1
    
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirx = -1
                    self.diry = 0
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]

                elif keys[pygame.K_RIGHT]:
                    self.dirx = 1
                    self.diry = 0
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]

                elif keys[pygame.K_UP]:
                    self.dirx = 0
                    self.diry = -1
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]

                elif keys[pygame.K_DOWN]:
                    self.dirx = 0
                    self.diry = 1
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]
        
        for i, currcube in enumerate(self.body):
            posi = currcube.pos[:]
            if posi in self.turns:
                turn = self.turns[posi]
                currcube.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(posi)
            else:
                if currcube.dirx == -1 and currcube.pos[0] <= 0:
                    currcube.pos = (rows - 1, currcube.pos[1])
                elif currcube.dirx == 1 and currcube.pos[0] >= rows - 1:
                    currcube.pos = (0, currcube.pos[1])
                elif currcube.diry == 1 and currcube.pos[1] >= rows - 1:
                    currcube.pos = (currcube.pos[0], 0)
                elif currcube.diry == -1 and currcube.pos[1] <= 0:
                    currcube.pos = (currcube.pos[0], rows - 1)
                else:
                    currcube.move(currcube.dirx, currcube.diry)

    def draw(self, screen):
        for i, currcube in enumerate(self.body):
            currcube.draw(screen)
    

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirx = 0
        self.diry = 1

    def addcube(self):
        tail = self.body[-1]
        x, y = tail.dirx, tail.diry

        if x == 1 and y == 0:
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
        elif x == -1 and y == 0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        elif x == 0 and y == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        elif x == 0 and y == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))
        
        self.body[-1].dirx = x
        self.body[-1].diry = y


# food
def food():
    position = s.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)

        if len(list(filter(lambda x:x.pos == (x, y), position))) > 0:
            continue
        else:
            break
        
    return (x, y)


# draws everyting to the screen in every loop
def drawscreen(screen):
    screen.fill((0, 0, 0))
    s.draw(screen)
    snake_food.draw(screen)
    pygame.display.update()

# main function
def main():
    global width, rows, s, snake_food
    pygame.init()
    width = 500
    rows = 20
    screen = pygame.display.set_mode((width, width))
    s = snake((10, 10))
    snake_food = cube(food(), color = (0, 0, 255))

    clock = pygame.time.Clock()

    running = True
    game_status = True

    score = 0
    game_over = pygame.font.Font('freesansbold.ttf', 28)
    game_over_display = game_over.render(f'PRESS ENTER TO PLAY AGAIN', True, (255, 255, 255))
    score_font = pygame.font.Font('freesansbold.ttf', 32)

    while running:
        pygame.time.delay(50)
        clock.tick(10)

        for i in range(len(s.body)):
            if s.body[i].pos in list(map(lambda x:x.pos, s.body[i+1:])):
                game_status = False
                score = len(s.body)
                s.reset((10, 10))
                break

        if game_status:
            s.move()
            if s.body[0].pos == snake_food.pos:
                s.addcube()
                snake_food = cube(food(), color = (0, 0, 255))

            drawscreen(screen)
        else:
            screen.fill((0, 0, 0))
            score_font_display = score_font.render(f'Score = {score}', True, (255, 255, 255))
            screen.blit(game_over_display, (20, 200))
            screen.blit(score_font_display, (160, 250))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        score = 0
                        game_status = True
            pygame.display.update()

if __name__ == "__main__":
    main()
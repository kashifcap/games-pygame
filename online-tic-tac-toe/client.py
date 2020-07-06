import socket
import pickle
import pygame


def win(game, turn):
	# row check
	for i in range(3):
		if game[i][0] == game[i][1] == game[i][2] and game[i][0] == turn:
			return True
	# column check
	for i in range(3):
		if game[0][i] == game[1][i] == game[2][i] and game[0][i] == turn:
			return True
	# diagonal check
	if game[0][0] == game[1][1] == game[2][2] and game[0][0] == turn:
		return True
	#diagonal check
	if game[0][2] == game[1][1] == game[2][0] and game[0][2] == turn:
		return True

	return False

def drawline(screen, game, turn):
	start_x = 0
	start_y = 0
	end_x = 0
	end_y = 0
	for i in range(3):
		if game[i][0] == game[i][1] == game[i][2] and game[i][0] == turn:
			start_x = 10
			start_y = i*200 + 100
			end_x = 590
			end_y = i*200 + 100

	# column check
	for i in range(3):
		if game[0][i] == game[1][i] == game[2][i] and game[0][i] == turn:
			start_x = i*200 + 100
			start_y = 10
			end_x = i*200 + 100
			end_y = 590

	# diagonal check
	if game[0][0] == game[1][1] == game[2][2] and game[0][0] == turn:
		start_x = 10
		start_y = 10
		end_x = 590
		end_y = 590
	#diagonal check
	elif game[0][2] == game[1][1] == game[2][0] and game[0][2] == turn:
		start_x = 590
		start_y = 10
		end_x = 10
		end_y = 590
	pygame.draw.line(screen, (255, 0, 0), (start_x, start_y), (end_x, end_y), 10)



def updateboard(coord, player):
    if coord != None:
        if coord[0] < 200:
            col = 0
        elif 200 < coord[0] < 400:
        	col = 1
        elif 400 < coord[0] < 600:
            col = 2
        else:
            col = None
        if coord[1] < 200:
            row = 0
        elif 200 < coord[1] < 400:
            row = 1
        elif 400 < coord[1] < 600:
            row = 2
        else:
            row = None

        if row != None and col != None and board[row][col] == '0':
            board[row][col] = player
            pos[0] = row
            pos[1] = col
            return False


def redrawscreen(screen):
    screen.fill((0, 0, 255))
    pygame.draw.line(screen, (255, 255, 255), (0, 200), (600, 200), 10)
    pygame.draw.line(screen, (255, 255, 255), (0, 400), (600, 400), 10)
    pygame.draw.line(screen, (255, 255, 255), (200, 0), (200, 600), 10)
    pygame.draw.line(screen, (255, 255, 255), (400, 0), (400, 600), 10)
    for i in range(3):
        for j in range(3):
            if board[i][j] != '0':
                shape_font = pygame.font.Font('freesansbold.ttf', 100)
                if board[i][j] == 'x':
                    shape_text = shape_font.render('X', True, (255, 255, 255))
                    screen.blit(shape_text, (j*200 + 50, i*200 + 60))
                elif board[i][j] == 'o':
                    shape_text = shape_font.render('O', True, (255, 255, 255))
                    screen.blit(shape_text, (j*200 + 50, i*200 + 60))
    
    if win(board, player):
        drawline(screen, board, player)
    elif win(board, opponent):
        drawline(screen, board, opponent)

    pygame.display.update()



def main():
    global board
    global width
    global pos
    global player, opponent

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # ip and port of server
    server = ""
    port = 5555

    board = [['0', '0', '0'], ['0', '0', '0'], ['0', '0', '0']]
    running = True
    width = 600
    state = False
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, width))

    s.connect((server, port))

    player = s.recv(2048).decode()
    if player == 'x':
        opponent = 'o'
        state = True
    else:
        opponent = 'x'

    while running:
        clock.tick(60)
        coord = None
        pos = [-1, -1]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = True
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == True:
                    coord = pygame.mouse.get_pos()
                    state = updateboard(coord, player)
        
        redrawscreen(screen)

        s.send(pickle.dumps(pos))
        new_board = pickle.loads(s.recv(2048))
        for i in range(3):
            for j in range(3):
                if board[i][j] != new_board[i][j]:
                    board[i][j] = new_board[i][j]
                    print(state)
                    state = True


main()
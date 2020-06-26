import pygame
import random
import time

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


def evaluate(board):
	if win(board, player):
		return 10
	elif win(board, computer):
		return -10
	else:
		return 0


def isfull(game):
	draw = 0
	for i in range(3):
		for j in range(3):
			if game[i][j] == '0':
				return False
	return True


def minmax(board, depth, isMax):
	score = evaluate(board)

	if score == 10:
		return score-depth
	
	if score == -10:
		return score

	if isfull(board):
		return 0

	if isMax:
		best = -1000
		for i in range(3):
			for j in range(3):
				if board[i][j] == '0':
					board[i][j] = player
					best = max(best, minmax(board, depth + 1, not(isMax)))
					board[i][j] = '0'
		return best
	else:
		best = 1000
		for i in range(3):
			for j in range(3):
				if board[i][j] == '0':
					board[i][j] = computer
					best = min(best, minmax(board, depth + 1, not(isMax)))
					board[i][j] = '0'
		return best


def minmaxutil(board):
	bestmove = -1000
	pos = (-1, -1)
	for i in range(3):
		for j in range(3):
			if board[i][j] == '0':
				board[i][j] = player
				moveval = minmax(board, 0, False)
				board[i][j] = '0'
				if moveval > bestmove:
					pos = (i, j)
					bestmove = moveval
	return pos


def drawshape(screen,shape, x, y):
	shape_x = y*200 + 60
	shape_y = x*200 + 50
	if shape == 'x':
		shape_font = pygame.font.Font('freesansbold.ttf', 100)
		shape_text = shape_font.render('X', True, (255, 255, 255))
		screen.blit(shape_text, (shape_x, shape_y))

	elif shape == 'o':
		shape_font = pygame.font.Font('freesansbold.ttf', 100)
		shape_text = shape_font.render('O', True, (255, 255, 255))
		screen.blit(shape_text, (shape_x, shape_y))



def screendraw(screen, board):
	screen.fill((0, 0, 255))
	pygame.draw.line(screen, (255, 255, 255), (0, 200), (600, 200), 10)
	pygame.draw.line(screen, (255, 255, 255), (0, 400), (600, 400), 10)
	pygame.draw.line(screen, (255, 255, 255), (200, 0), (200, 600), 10)
	pygame.draw.line(screen, (255, 255, 255), (400, 0), (400, 600), 10)
	for i in range(3):
		for j in range(3):
			if board[i][j] !=0:
				if board[i][j] == 'x':
					drawshape(screen, 'x', i, j)
				elif board[i][j] == 'o':
					drawshape(screen, 'o', i, j)
	if win(board, 'x'):
		drawline(screen, board, 'x')
	elif win(board, 'o'):
		drawline(screen, board, 'o')
	pygame.display.update()


if __name__ == '__main__':
	global player, computer
	player = 'o'
	player_x = 1000
	player_y = 1000
	computer = 'x'

	#turn = random.choice(['o', 'x'])
	turn = 'x'

	board = [['0', '0', '0'],
			 ['0', '0', '0'],
			 ['0', '0', '0']]

	pygame.init()
	running = True
	game_status = True
	game_result_font = pygame.font.Font('freesansbold.ttf', 50)
	winner = ''

	screen = pygame.display.set_mode((600, 600))

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				pygame.quit()
			elif event.type is pygame.MOUSEBUTTONDOWN:
				if turn == 'x':
					player_x, player_y = pygame.mouse.get_pos()

		if game_status:

			if turn == 'o':
				position = minmaxutil(board)
				board[position[0]][position[1]] = 'o'
				turn = 'x'

			elif turn == 'x':
				if player_x < 200:
					col = 0
				elif 200 < player_x < 400:
					col = 1
				elif 400 < player_x < 600:
					col = 2
				else:
					col = None
				if player_y < 200:
					row = 0
				elif 200 < player_y < 400:
					row = 1
				elif 400 < player_y < 600:
					row = 2
				else:
					row = None
				print
				if row != None and col != None and board[row][col] == '0':
					board[row][col] = 'x'
					turn = 'o'
				


			screendraw(screen, board)

			if win(board, 'x'):
				game_status = False
				winner = 'player'
				time.sleep(3)

			elif win(board, 'o'):
				game_status = False
				winner = 'computer'
				time.sleep(3)

			elif isfull(board):
				game_status = False
				winner = 'draw'
				time.sleep(3)
		else:
			
			screen.fill((0, 0, 0))
			if winner == 'player':
				game_result = game_result_font.render('You Won!', True, (255, 255, 255))

			elif winner == 'computer':
				game_result = game_result_font.render('You Lost!', True, (255, 255, 255))

			elif winner == 'draw':
				game_result = game_result_font.render('Its a Draw!', True, (255, 255, 255))

			screen.blit(game_result, (200, 300))

			pygame.display.update()



		
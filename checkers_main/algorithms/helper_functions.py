import numpy as np
from copy import deepcopy
import pygame

# ---------------------------------------------------------------- Q-Learning ----------------------------------------------------------------

# returns the initial board as a 1d array
def get_board():
    return np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1])
	# return Board()

# number of opponent pieces captured (max = 12)
def num_captured(board):
	return 12 - np.sum(board < 0)
	# return 12 - board.red_left

# returns a 1d board ie. get_board() as 8x8 array
def expand(board): 
	b = np.zeros((8, 8), dtype='b')
	for i in range(0, 8):
		if (i%2 == 0):
			b[i] = np.array([0, board[i*4], 0, board[i*4 + 1], 0, board[i*4 + 2], 0, board[i*4 + 3]])
		else:
			b[i] = np.array([board[i*4], 0, board[i*4 + 1], 0, board[i*4 + 2], 0, board[i*4 + 3], 0])
	return b

# returns an 8x8 board as a 1d array
def compress(board):
	b = np.zeros((1,32), dtype='b')
	for i in range(0, 8):
		if (i%2 == 0):
			b[0, i*4 : i*4+4] = np.array([board[i, 1], board[i, 3], board[i, 5], board[i, 7]])
		else:
			b[0, i*4 : i*4+4] = np.array([board[i, 0], board[i, 2], board[i, 4], board[i, 6]])
	return b

#flips the board (switches pov)
def reverse(board):
	b = -board
	b = np.fliplr(b)
	b = np.flipud(b)
	return b

# return count of non-king pieces
def num_men(board):
	return np.sum(board == 1)
	# return board.white_left - board.white_kings

# return count of king pieces
def num_kings(board):
	return np.sum(board == 3)

# returns a count of pieces on enemy side
def at_enemy(board):
	count = 0
	for i in range(5, 8):
		count += np.sum(board[i] == 1) + np.sum(board[i] == 3)
	return count

# returns count of pieces in middle
def at_middle(board):
	count = 0
	for i in range(3, 5):
		count += np.sum(board[i] == 1) + np.sum(board[i] == 3)
	return count

# returns count of unprotected opponents pieces 
def capturables(board): 
	count = 0
	for i in range(1, 7):
		for j in range(1, 7):
			if (board[i, j] < 0):
				count += (board[i+1, j+1] >= 0 and board[i+1, j-1] >= 0 and  board[i-1, j+1] >= 0 and board[i-1, j-1] >= 0)
	return count

 # number of own pieces that can't be captured
def uncapturables(board):
	count = 0
	for i in range(1, 7):
		for j in range(1, 7):
			if (board[i, j] > 0):
				count += ((board[i+1, j+1] > 0 < board[i+1, j-1]) or (board[i-1, j+1] > 0 < board[i-1, j-1]) or (board[i+1, j+1] > 0 < board[i-1, j+1]) or (board[i+1, j-1] > 0 < board[i-1, j-1]))
	count += np.sum(board[0] == 1) + np.sum(board[0] == 3) + np.sum(board[1:7, 0] == 1) + np.sum(board[1:7, 0] == 3) + np.sum(board[7] == 1) + np.sum(board[7] == 3) + np.sum(board[1:7, 7] == 1) + np.sum(board[1:7, 7] == 3)
	return count

# number of own pieces with at least one support
def semicapturables(board): 
	return (12 - uncapturables(board) - capturables(reverse(board)))

# returns a random 1d board
def random_board():
    b = get_board()
    promote = 0.9
    remove = 0.4
    add = 0.1
    for ind, piece in enumerate(b):
        # randomly promote, remove, or add piece
        rand = np.random.random()
        if piece and rand > promote:
            b[ind] = piece * 3
            promote += 0.005
        elif piece and rand < remove and rand > add:
            b[ind] = 0
            remove -= 0.005
            add += 0.05
        elif not piece and rand < add:
            if np.random.random() > 0.5 and np.sum(b > 0) < 12:
                b[ind] = 1
            if np.random.random() < 0.5 and np.sum(b < 0) < 12:
                b[ind] = -1
    return b

# returns a count of all possible moves
def possible_moves(board):
	count = 0
	for i in range(0, 8):
		for j in range(0, 8):
			if (board[i, j] > 0):
				count += num_branches(board, i, j)
	if (count > 0):
		return count
	for i in range(0, 8):
		for j in range(0, 8):
			if (board[i, j] >= 1 and i < 7):
				if (j < 7):
					count += (board[i+1, j+1] == 0)
				if (j > 0):
					count += (board[i+1, j-1] == 0)
			if (board[i, j] == 3 and i > 0):
				if (j < 7):
					count += (board[i-1, j+1] == 0)
				elif (j > 0):
					count += (board[i-1, j-1] == 0)
	return count

# simulates capturing of pieces and returns count 
def num_branches(board, x, y):
	count = 0
	if (board[x, y] >= 1 and x < 6):
		if (y < 6):
			if (board[x+1, y+1] < 0 and board[x+2, y+2] == 0):
				board[x+2, y+2] = board[x, y]
				board[x, y] = 0
				temp = board[x+1, y+1]
				board[x+1, y+1] = 0
				count += num_branches(board, x+2, y+2) + 1
				board[x+1, y+1] = temp
				board[x, y] = board[x+2, y+2]
				board[x+2, y+2] = 0
		if (y > 1):
			if (board[x+1, y-1] < 0 and board[x+2, y-2] == 0):
				board[x+2, y-2] = board[x, y]
				board[x, y] = 0
				temp = board[x+1, y-1]
				board[x+1, y-1] = 0
				count += num_branches(board, x+2, y-2) + 1
				board[x+1, y-1] = temp
				board[x, y] = board[x+2, y-2]
				board[x+2, y-2] = 0
	if (board[x, y] == 3 and x > 1):
		if (y < 6):
			if (board[x-1, y+1] < 0 and board[x-2, y+2] == 0):
				board[x-2, y+2] = board[x, y]
				board[x, y] = 0
				temp = board[x-1, y+1]
				board[x-1, y+1] = 0
				count += num_branches(board, x-2, y+2) + 1
				board[x-1, y+1] = temp
				board[x, y] = board[x-2, y+2]
				board[x-2, y+2] = 0
		if (y > 1):
			if (board[x-1, y-1] < 0 and board[x-2, y-2] == 0):
				board[x-2, y-2] = board[x, y]
				board[x, y] = 0
				temp = board[x-1, y-1]
				board[x-1, y-1] = 0
				count += num_branches(board, x-2, y-2) + 1
				board[x-1, y-1] = temp
				board[x, y] = board[x-2, y-2]
				board[x-2, y-2] = 0
	return count

# return array of evaluation metrics for the board
def get_metrics(board): # returns [label, 10 labeling metrics]
	b = expand(board)

	capped = num_captured(b)
	potential = possible_moves(b) - possible_moves(reverse(b))
	men = num_men(b) - num_men(-b)
	kings = num_kings(b) - num_kings(-b)
	caps = capturables(b) - capturables(reverse(b))
	semicaps = semicapturables(b)
	uncaps = uncapturables(b) - uncapturables(reverse(b))
	mid = at_middle(b) - at_middle(-b)
	far = at_enemy(b) - at_enemy(reverse(b))
	won = game_winner(b)

	score = 4*capped + potential + men + 3*kings + caps + 2*semicaps + 3*uncaps + 2*mid + 3*far + 100*won
	if (score < 0):
		return np.array([-1, capped, potential, men, kings, caps, semicaps, uncaps, mid, far, won])
	else:
		return np.array([1, capped, potential, men, kings, caps, semicaps, uncaps, mid, far, won])
	
# returns the winner if a player has no pieces or no moves left, returns 0 otherwise
def game_winner(board):
    if (np.sum(board < 0) == 0):
        return 1
    elif (np.sum(board > 0) == 0):
        return -1
    if (possible_moves(board) == 0):
        return -1
    elif (possible_moves(reverse(board)) == 0):
        return 1
    else:
        return 0
	
# returns board before and after capture as a 2d array
def generate_branches(board, x, y):
	bb = compress(board)
	if (board[x, y] >= 1 and x < 6):
		temp_1 = board[x, y]
		if (y < 6):
			if (board[x+1, y+1] < 0 and board[x+2, y+2] == 0):
				board[x+2, y+2] = board[x, y]
				if (x+2 == 7):
					board[x+2, y+2] = 3
				temp = board[x+1, y+1]
				board[x+1, y+1] = 0
				if (board[x, y] != board[x+2, y+2]):
					board[x, y] = 0
					bb = np.vstack((bb, compress(board)))
				else:
					board[x, y] = 0
					bb = np.vstack((bb, generate_branches(board, x+2, y+2)))
				board[x+1, y+1] = temp
				board[x, y] = temp_1
				board[x+2, y+2] = 0
		if (y > 1):
			if (board[x+1, y-1] < 0 and board[x+2, y-2] == 0):
				board[x+2, y-2] = board[x, y]
				if (x+2 == 7):
					board[x+2, y-2] = 3
				temp = board[x+1, y-1]
				board[x+1, y-1] = 0
				if (board[x, y] != board[x+2, y-2]):
					board[x, y] = 0
					bb = np.vstack((bb, compress(board)))
				else:
					board[x, y] = 0
				bb = np.vstack((bb, generate_branches(board, x+2, y-2)))
				board[x+1, y-1] = temp
				board[x, y] = temp_1
				board[x+2, y-2] = 0
	if (board[x, y] == 3 and x > 0):
		if (y < 6):
			if (board[x-1, y+1] < 0 and board[x-2, y+2] == 0):
				board[x-2, y+2] = board[x, y]
				board[x, y] = 0
				temp = board[x-1, y+1]
				board[x-1, y+1] = 0
				bb = np.vstack((bb, generate_branches(board, x-2, y+2)))
				board[x-1, y+1] = temp
				board[x, y] = board[x-2, y+2]
				board[x-2, y+2] = 0
		if (y > 1):
			if (board[x-1, y-1] < 0 and board[x-2, y-2] == 0):
				board[x-2, y-2] = board[x, y]
				board[x, y] = 0
				temp = board[x-1, y-1]
				board[x-1, y-1] = 0
				bb = np.vstack((bb, generate_branches(board, x-2, y-2)))
				board[x-1, y-1] = temp
				board[x, y] = board[x-2, y-2]
				board[x-2, y-2] = 0
	return bb

# returns the new board after capturing
def generate_next(board):
    bb = np.array([get_board()])
    for i in range(0, 8):
        for j in range(0, 8):
            if board[i, j] > 0:
                bb = np.vstack((bb, generate_branches(board, i, j)[1:]))
    if len(bb) > 1:
        return bb[1:]
    for i in range(0, 8):
        for j in range(0, 8):
            if board[i, j] >= 1 and i < 7:
                temp = board[i, j]
                if j < 7:
                    if board[i + 1, j + 1] == 0:
                        board[i + 1, j + 1] = board[i, j]
                        if i + 1 == 7:
                            board[i + 1, j + 1] = 3
                        board[i, j] = 0
                        bb = np.vstack((bb, compress(board)))
                        board[i, j] = temp
                        board[i + 1, j + 1] = 0
                if j > 0:
                    if board[i + 1, j - 1] == 0:
                        board[i + 1, j - 1] = board[i, j]
                        if i + 1 == 7:
                            board[i + 1, j - 1] = 3
                        board[i, j] = 0
                        bb = np.vstack((bb, compress(board)))
                        board[i, j] = temp
                        board[i + 1, j - 1] = 0
            if board[i, j] == 3 and i > 0:
                if j < 7:
                    if board[i - 1, j + 1] == 0:
                        board[i - 1, j + 1] = board[i, j]
                        board[i, j] = 0
                        bb = np.vstack((bb, compress(board)))
                        board[i, j] = board[i - 1, j + 1]
                        board[i - 1, j + 1] = 0
                elif j > 0:
                    if board[i - 1, j - 1] == 0:
                        board[i - 1, j - 1] = board[i, j]
                        board[i, j] = 0
                        bb = np.vstack((bb, compress(board)))
                        board[i, j] = board[i - 1, j - 1]
                        board[i - 1, j - 1] = 0
    return bb[1:]

# ---------------------------------------------------------------- Minimax ----------------------------------------------------------------
def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board

#Figures out where valid moves are located
def get_all_moves(board, color, game):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            #draw_moves(game, board, piece)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)
    
    return moves

#Shows where the possible moves are 
def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0,255,0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    #pygame.time.delay(100)
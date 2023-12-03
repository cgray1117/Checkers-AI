from keras.models import model_from_json
from .helper_functions import *
from checkers.piece import Piece
from checkers.constants import WHITE, RED

json_file = open('checkers_main/reinforced.json', 'r')
board_json = json_file.read()
json_file.close()

disc_model = model_from_json(board_json)
disc_model.load_weights('checkers_main/reinforced.h5')
disc_model.compile(optimizer='adadelta', loss='mean_squared_error')

if __name__ == '__main__':
	data = np.zeros((1, 32))
	labels = np.zeros(1)
	win = lose = draw = 0
	winrates = []
	learning_rate = 0.5
	discount_factor = 0.95

	for gen in range(0, 500):
		for game in range(0, 200):
			temp_data = np.zeros((1, 32))
			board = expand(get_board())
			player = np.sign(np.random.random() - 0.5)
			turn = 0
			while (True):
				moved = False
				boards = np.zeros((0, 32))
				if (player == 1):
					boards = generate_next(board)
				else:
					boards = generate_next(reverse(board))

				scores = disc_model.predict_on_batch(boards)
				max_index = np.argmax(scores)
				best = boards[max_index]

				if (player == 1):
					board = expand(best)
					temp_data = np.vstack((temp_data, compress(board)))
				else:
					board = reverse(expand(best))

				player = -player

				# punish losing games, reward winners  & drawish games reaching more than 200 turns
				winner = game_winner(board)
				if (winner == 1 or (winner == 0 and turn >= 200) ):
					if winner == 1:
						win = win + 1
					else:
						draw = draw + 1
					reward = 10
					old_prediction = disc_model.predict_on_batch(temp_data[1:])
					optimal_futur_value = np.ones(old_prediction.shape)
					temp_labels = old_prediction + learning_rate * (reward + discount_factor * optimal_futur_value - old_prediction )
					data = np.vstack((data, temp_data[1:]))
					labels = np.vstack((labels, temp_labels))
					break
				elif (winner == -1):
					lose = lose + 1
					reward = -10
					old_prediction = disc_model.predict_on_batch(temp_data[1:])
					optimal_futur_value = -1*np.ones(old_prediction.shape)
					temp_labels = old_prediction + learning_rate * (reward + discount_factor * optimal_futur_value - old_prediction )
					data = np.vstack((data, temp_data[1:]))
					labels = np.vstack((labels, temp_labels))
					break
				turn = turn + 1

			if ((game+1) % 200 == 0):
				disc_model.fit(data[1:], labels[1:], epochs=16, batch_size=256, verbose=0)
				data = np.zeros((1, 32))
				labels = np.zeros(1)
			print(f'{game}/200 games complete')          
			
		winrate = int((win+draw)/(win+draw+lose)*100)
		winrates.append(winrate)
		print(f'{gen}/200 series complete')
	
		disc_model.save_weights('reinforced_model.h5')
	
	print('Checkers Board Model updated by reinforcement learning & saved to: reinforced_model.json/h5')

def convert_to_one_hot(board):
        converted_board = np.zeros((8,8))
        for row_ind, row in enumerate(board):
            for col_ind, piece in enumerate(row):
                if piece:
                    if piece.color == WHITE:
                        converted_board[row_ind, col_ind] = 1
                    else:
                        converted_board[row_ind, col_ind] = -1
        return converted_board
    
def convert_from_one_hot(board, game):
    print(game.board.board)
    new_board = []
    for row in range(8):
        new_board.append([0, 0, 0, 0, 0, 0, 0, 0])
       
    for row_ind, row in enumerate(board):
        for col_ind, piece in enumerate(row):
            if piece:
                if piece == 1:
                    new_board[row_ind][col_ind] = Piece(row_ind, col_ind, WHITE)
                elif piece == -1:
                    new_board[row_ind][col_ind] = Piece(row_ind, col_ind, RED) 
    game.board.board = new_board
    return game.board

def best_move(board, game):
    boards0 = np.array(compress(convert_to_one_hot(board.board)))
    #boards = generate_next(board)
    boards = get_all_moves(board, WHITE, game)
    for b in boards:
        boards0 = np.vstack((boards0, compress(convert_to_one_hot(b.board))))
    scores = disc_model.predict_on_batch(boards0[1:])
    max_index = np.argmax(scores)
    best = boards[max_index]
    return best

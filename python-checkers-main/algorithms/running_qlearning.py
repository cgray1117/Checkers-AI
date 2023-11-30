from keras.models import model_from_json
from algorithms.helper_functions import *
from checkers.piece import Piece
from checkers.constants import WHITE, RED
from checkers.board import Board

json_file = open('disc.json', 'r')
board_json = json_file.read()
json_file.close()

disc_model = model_from_json(board_json)
disc_model.load_weights('disc.h5')
disc_model.compile(optimizer='adadelta', loss='mean_squared_error')

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

def best_move(board):
  boards = np.zeros((0, 32))
  boards = generate_next(board)
  scores = disc_model.predict_on_batch(boards)
  max_index = np.argmax(scores)
  best = boards[max_index]
  return best

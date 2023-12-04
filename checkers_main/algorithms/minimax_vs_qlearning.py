from helper_functions import *
import numpy as np
from keras.models import model_from_json

RED = (255, 0, 0)
WHITE = (255, 255, 255)

json_file = open('checkers_main/reinforced.json', 'r')
board_json = json_file.read()
json_file.close()

reinforced_model = model_from_json(board_json)
reinforced_model.load_weights('checkers_main/reinforced.h5')
reinforced_model.compile(optimizer='adadelta', loss='mean_squared_error')

def convert_to_one_hot(board):
        converted_board = np.zeros((8,8))
        for row_ind, row in enumerate(board):
            for col_ind, piece in enumerate(row):
                if piece:
                    if piece == WHITE:
                        converted_board[row_ind, col_ind] = 1
                    else:
                        converted_board[row_ind, col_ind] = -1
        return converted_board

def best_move(board):
  compressed_board = compress(reverse(board))
  boards = np.zeros((0, 32))
  boards = generate_next(reverse(board))
  scores = reinforced_model.predict_on_batch(boards)
  max_index = np.argmax(scores)
  best = boards[max_index]
  return best

def print_board(board):
  for row in board:
    for square in row:
        if square == 1:
            caracter = "|O"
        elif square == -1:
            caracter = "|X"
        elif square == 3:
            caracter = "|Ko"
        elif square == -3:
            caracter = "|Kx"
        else:
            caracter = "| "
    
        print(str(caracter), end='')
    print('|')

board = [[0, (255, 255, 255), 0, (255, 255, 255), 0, (255, 255, 255), 0, (255, 255, 255)], [(255, 255, 255), 0, (255, 255, 255), 0, (255, 255, 255), 0, (255, 255, 255), 0], [0, (255, 255, 255), 0, (255, 255, 255), 0, (255, 255, 255), 0, 0], [0, 0, 0, 0, 0, 0, (255, 255, 255), 0], [0, 0, 0, 0, 0, 0, 0, (255, 0, 0)], [(255, 0, 0), 0, (255, 0, 0), 0, (255, 0, 0), 0, 0, 0], [0, (255, 0, 0), 0, (255, 0, 0), 0, (255, 0, 0), 0, (255, 0, 0)], [(255, 0, 0), 0, (255, 0, 0), 0, (255, 0, 0), 0, (255, 0, 0), 0]]

board = convert_to_one_hot(board)

print_board(expand(best_move(board)))


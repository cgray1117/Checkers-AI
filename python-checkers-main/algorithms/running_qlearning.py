from keras.models import model_from_json
from helper_functions import *

json_file = open('disc.json', 'r')
board_json = json_file.read()
json_file.close()

disc_model = model_from_json(board_json)
disc_model.load_weights('disc.h5')
disc_model.compile(optimizer='adadelta', loss='mean_squared_error')

def best_move(board):
  boards = np.zeros((0, 32))
  boards = generate_next(board)
  scores = disc_model.predict_on_batch(boards)
  max_index = np.argmax(scores)
  best = boards[max_index]
  return best

print(expand(best_move(expand(get_board()))))
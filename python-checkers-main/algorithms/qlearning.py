import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras import regularizers
from keras.models import model_from_json
from helper_functions import *

# American checkers: wikipedia.org/wiki/English_draughts
# 	on a 8x8 checkerboard, both players start with 12 men
#	Black plays the first move
#	all pieces can only move and capture diagonally
#	men can only move/capture diagonally forward
#	kings can move/capture in any diagonal direction
#	if a man reaches the other side of the board, the turn ends and it becomes a king
#	captures are made by moving any piece diagonally over an opponent's
#	if a capture can be made, it must be taken
#	mutliple captures can be made in a single turn and with a single piece
#	the game ends when a players captures all the opponent's pieces
#	a player also whens when the opponent can not make a legal move

#	example board: 
#	/b/b/b/b	b/w = Black/White man {1, -1}
#	b/b/b/b/	B/W = Black/White king {3, -3}
#	/b/b/b/b	_ = empty square {0}
#	_/_/_/_/	/ = unusable square
#	/_/_/_/_
#	w/w/w/w/
#	/w/w/w/w
#	w/w/w/w/	* since pieces only move diagonally, only 32 squares are used

if __name__ == '__main__':
	# generative model, which only looks at heuristic scoring metrics used for labeling
	gen_model = Sequential()
	gen_model.add(Dense(32, input_dim=10)) 
	gen_model.add(Dense(4, activation='relu',  kernel_regularizer=regularizers.l2(0.01)))

	# output is passed to relu() because labels are binary
	gen_model.add(Dense(1, activation='sigmoid',  kernel_regularizer=regularizers.l2(0.01)))
	gen_model.compile(optimizer='adam', loss='binary_crossentropy')


	# generate 5 sets of 1000 game states, used to train generative model
	for i in range(0, 5):
		board_0 = expand(random_board())
		boards_1 = generate_next(board_0)
		boards_2 = np.zeros((0,32))
		counter_1 = counter_2 = 0
		while (len(boards_1) + len(boards_2) < 1000):
			temp = counter_1
			for counter_1 in range(temp, min(temp + 10, len(boards_1))):
				if (possible_moves(reverse(expand(boards_1[counter_1]))) > 0):
					boards_2 = np.vstack((boards_2, generate_next(reverse(expand(boards_1[counter_1])))))
			temp = counter_2
			for counter_2 in range(temp, min(temp + 10, len(boards_2))):
				if (possible_moves(expand(boards_2[counter_2])) > 0):
					boards_1 = np.vstack((boards_1, generate_next(expand(boards_2[counter_2]))))

		# concat 1000 game states
		data = np.vstack((boards_1, boards_2))
		boards_2 = np.zeros((0, 32))
		counter_2 = 0
		boards_1 = np.vstack((boards_1[-10:], generate_next(board_0)))
		counter_1 = len(boards_1) - 1
		metrics = np.zeros((0, 11))

		# calculate/save heuristic metrics for each game state
		for board in iter(data):
			metrics = np.vstack((metrics, get_metrics(board)))

		# pass to generative model
		gen_model.fit(metrics[:, 1:], metrics[:, 0], epochs=32, batch_size=64, verbose=0)

	# discriminative model
	disc_model = Sequential()

	# input dimensions is 32 board position values (and 10 heuristic metrics - removed)
	disc_model.add(Dense(32 , activation='relu', input_dim=32))

	# use regularizers, to prevent fitting noisy labels
	disc_model.add(Dense(16 , activation='relu', kernel_regularizer=regularizers.l2(0.01)))
	disc_model.add(Dense(8 , activation='relu', kernel_regularizer=regularizers.l2(0.01))) # 16
	disc_model.add(Dense(4 , activation='relu', kernel_regularizer=regularizers.l2(0.01))) # 8

	# output isn't squashed, because it might lose information
	disc_model.add(Dense(1 , activation='linear', kernel_regularizer=regularizers.l2(0.01)))
	disc_model.compile(optimizer='adam', loss='binary_crossentropy')


	# generative 32 sets of 1000 game states, used to train discriminative model
	for i in range(0, 32):
		boards_1 = generate_next(expand(random_board()))
		boards_2 = np.zeros((0,32))
		counter_1 = counter_2 = 0
		while (len(boards_1) + len(boards_2) < 1000):
			temp = counter_1
			for counter_1 in range(temp, min(temp + 10, len(boards_1))):
				if (possible_moves(reverse(expand(boards_1[counter_1]))) > 0):
					boards_2 = np.vstack((boards_2, generate_next(reverse(expand(boards_1[counter_1])))))
			temp = counter_2
			for counter_2 in range(temp, min(temp + 10, len(boards_2))):
				if (possible_moves(expand(boards_2[counter_2])) > 0):
					boards_1 = np.vstack((boards_1, generate_next(expand(boards_2[counter_2]))))

		data = np.vstack((boards_1, boards_2))
		boards_2 = np.zeros((0, 32))
		counter_2 = 0
		boards_1 = np.vstack((boards_1[-10:], generate_next(board_0)))
		counter_1 = len(boards_1) - 1

		# calculate heuristic metric for data
		metrics = np.zeros((0, 11))
		for board in iter(data):
			metrics = np.vstack((metrics, get_metrics(board)))

		# calculate probilistic (noisy) labels
		probabilistic = gen_model.predict_on_batch(metrics[:, 1:])

		# calculate confidence score for each probabilistic label using error between probabilistic and weak label
		confidence = 1/(1 + np.absolute(metrics[:, 0] - probabilistic[:, 0]))

		# fit labels to {-1, 1}
		probabilistic = np.sign(probabilistic)

		# concat board position data with heurstic metric and pass for training - removed
		# data = np.hstack((data, metrics[:, 1:]))
		disc_model.fit(data, probabilistic, epochs=16, batch_size=64, sample_weight=confidence, verbose=0)

	# save models
	gen_json = gen_model.to_json()
	with open('gen.json', 'w') as json_file:
		json_file.write(gen_json)
	gen_model.save_weights('gen.h5')

	disc_json = disc_model.to_json()
	with open('disc.json', 'w') as json_file:
		json_file.write(disc_json)
	disc_model.save_weights('disc.h5')

	print('Checkers Model saved to: gen.json/h5 and disc.json/h5')

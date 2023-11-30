import pygame
from .helper_functions import *

RED = (255,0,0)
WHITE = (255, 255, 255)
MAX = float('inf')
MIN = float('-inf')


#Defining the MINIMAX algorithm
#Evaluates best move 
def minimax(position, depth, max_player, game, ALPHA=MIN, BETA=MAX):
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position
    #Finds the maximum win
    if max_player:
        maxEval = MIN
        best_move = None
        for move in get_all_moves(position, WHITE, game):
            evaluation = minimax(move, depth-1, False, game, ALPHA, BETA)[0]
            maxEval = max(maxEval, evaluation)
            ALPHA = max(ALPHA, maxEval)
            if BETA <= ALPHA:
                break
            if maxEval == evaluation:
                best_move = move
        
        return maxEval, best_move
    
    else: #evaluates the move that brings the minimum win for the opponent
        minEval = MAX
        best_move = None
        for move in get_all_moves(position, RED, game):
            evaluation = minimax(move, depth-1, True, game, ALPHA, BETA)[0]
            minEval = min(minEval, evaluation)
            BETA = min(BETA, minEval)
            if BETA <= ALPHA:
                break
            if minEval == evaluation:
                best_move = move
        
        return minEval, best_move


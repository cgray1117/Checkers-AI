#Neccesities 
import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from minimax.algorithm import minimax

#Frames per second for gameplay
FPS = 60

#Define the window and title
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

#Set row and columns 
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

#Set the game flow, runs until the quit condition is met
#Gets which players turn it is
#Gets possible move positions
#Shapes on top of shapes moving within the rules of checkers 
def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)
        #Checks whos turn is it, if its the computers turn or white then use minimax algorithm to find best move on the board
        if game.turn == WHITE:
            value, new_board = minimax(game.get_board(), 4, WHITE, game)
            game.ai_move(new_board)
        #If there is no winner after the move then keep playing
        if game.winner() != None:
            print(game.winner())
            run = False
        #identifies the event then if it doesnt equal quit it keeps running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #identifies type of event then whereever theres a click it moves the piece to that location after getting the possible moves
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()
    
    pygame.quit()

main()
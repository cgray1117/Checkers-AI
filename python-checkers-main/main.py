#Neccesities 
import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from algorithms.minimax import minimax
from button import Button
import sys

pygame.init()

#Frames per second for gameplay 
FPS = 60

#Define the window and title
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

# main menu background image
BG = pygame.image.load("assets/main_menu_bg.png")
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

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

def play():
    run = True
    clock = pygame.time.Clock()
    game = Game(WINDOW)
    WINDOW.fill("black")
    pygame.display.set_caption('Checkers')


    while run:
        clock.tick(FPS)
        #Checks whos turn is it, if its the computers turn or white then use minimax algorithm to find best move on the board
        if game.turn == WHITE:
            value, new_board = minimax(game.get_board(), 3, WHITE, game)
            game.ai_move(new_board)
            print(value)
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

def options():

    MINIMAX_BUTTON = Button(image=None, pos=(400, 300), 
                            text_input="MINIMAX", font=get_font(65), base_color="black", hovering_color="#d7fcd4")
    QLEARNING_BUTTON = Button(image=None, pos=(400, 450), 
                        text_input="Q-LEARNING", font=get_font(65), base_color="#d7fcd4", hovering_color='black')
    OPTIONS_BACK = Button(image=None, pos=(400, 600), 
                        text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        WINDOW.fill('white')

        CHOOSE_TEXT = get_font(45).render("CHOOSE ALGORITHM", True, "Black")
        CHOOSE_RECT = CHOOSE_TEXT.get_rect(center=(400, 100))

        DEFAULT_TEXT = get_font(20).render("DEFAULT: MINIMAX", True, "Black")
        DEFAULT_RECT = CHOOSE_TEXT.get_rect(center=(600, 200))

        WINDOW.blit(CHOOSE_TEXT, CHOOSE_RECT)
        WINDOW.blit(DEFAULT_TEXT, DEFAULT_RECT)

        for button in [MINIMAX_BUTTON, QLEARNING_BUTTON, OPTIONS_BACK]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(WINDOW)
    
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                if MINIMAX_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    MINIMAX_BUTTON.change_base_color('Black')
                    QLEARNING_BUTTON.change_base_color('#d7fcd4', True)
                    MINIMAX_BUTTON.update(WINDOW)
                    QLEARNING_BUTTON.update(WINDOW)
                elif QLEARNING_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    QLEARNING_BUTTON.change_base_color('Black')
                    MINIMAX_BUTTON.change_base_color('#d7fcd4', True)
                    QLEARNING_BUTTON.update(WINDOW)
                    MINIMAX_BUTTON.update(WINDOW)

        pygame.display.update()

def main_menu():
    

    while True:
        pygame.display.set_caption('Main Menu')
        WINDOW.blit(BG, (0,0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(80).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/main_menu_button_rect.png"), pos=(400, 300), 
                            text_input="PLAY", font=get_font(65), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/main_menu_button_rect.png"), pos=(400, 450), 
                            text_input="OPTIONS", font=get_font(65), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/main_menu_button_rect.png"), pos=(400, 600), 
                            text_input="QUIT", font=get_font(65), base_color="#d7fcd4", hovering_color="White")
        
        WINDOW.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WINDOW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
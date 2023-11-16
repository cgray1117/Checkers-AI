import pygame

#Defines the shape of the board
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

#RGB
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128,128,128)

#Defines the kings when a player kings a piece
CROWN = pygame.transform.scale(pygame.image.load('assets/king.png'), (44, 25))
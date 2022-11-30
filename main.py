import pygame
from pygame.locals import *

pygame.init()

# set up the game window
screen_width = 600
screen_height = 500


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Evil Pong")

# define game variable
margin = 50
cpu_score = 0
player_score = 0


# set clock
Clock = pygame.time.Clock()

# define colors
# background color:
bg = (36, 36, 36)
light_grey = (200, 200, 200)

# define font:
font = pygame.font.SysFont('Helvetica', 18)


def draw_board():
    # filling the screen with one color (bg)
    screen.fill((bg))
    # drawing a line in the middle of the screen
    pygame.draw.aaline(screen, light_grey, (300, 500), (300, 50))
    # drawing a line in the upper part of the screen
    pygame.draw.line(screen, light_grey, (0, margin), (screen_width, margin))


# function for displaying text on screen

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))



run = True
while run:

    draw_board()
    draw_text('CPU: ' + str(cpu_score), font, light_grey, 30, 15)
    draw_text('P1: ' + str(player_score), font, light_grey, screen_width  -70, 15)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()

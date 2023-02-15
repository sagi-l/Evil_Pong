import pygame


# general variables for the main game
class GeneralMainVariables:
    # set up the game window
    screen_width = 600
    screen_height = 500
    screen = pygame.display.set_mode((screen_width, screen_height))

    # for random movement
    angle1 = 0
    angle2 = 0

    # defining players
    p1 = "P1: "
    cpu_score = 0
    player_score = 0

    # paddle color change
    z = True
    zz = True

    # Game loop variables
    live_ball = False
    margin = 50
    fps = 60
    winner = 0
    speed_increase = 0

    # for random number generator
    random_num = [0]

    # for math function
    x = 5
    y = 5

    # set clock
    Clock = pygame.time.Clock()
    timer = 0
    fpsClock = pygame.time.Clock()

    # define colors
    # background color:
    bg = (36, 36, 36)
    bg2 = (38, 38, 38)

    # objects colors:
    light_grey = (200, 200, 200)

    # more colors
    deep_sky = (0, 191, 255)
    red = (238, 44, 44)
    violet = (255, 62, 150)
    violet2 = (230, 230, 50)

    # define font:
    font = pygame.font.SysFont('Helvetica', 18)
    font2 = pygame.font.SysFont('Helvetica', 24)

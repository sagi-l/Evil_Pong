import pygame
from GameStat import *
run = True
run2 = True
run_options = False
run_start = False
run_scores = False
pygame.init()

gs2 = SecondGameState()

def start():
    print("start screen!")
    run_start = True
    while run_start:
        screen_width = 600
        screen_height = 500
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Evil Pong Main Menu")
        screen.fill((36, 36, 36))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_paused = True

                    print("pause")
                elif event.key == pygame.K_o:
                    game_paused = False
                    run_start = False

                if event.key == pygame.K_ESCAPE:
                    run2 = True
                    run_start = False
                    gs2.test = 10

                    print("test1 = ", gs2.test)

            if event.type == pygame.QUIT:
                run_start = False
                run2 = True

        pygame.display.update()
def options():
    print("options screen")


def scores():
    print("scores screen")


def run2(run=True, game_paused=False):
    # setting up the game menu screen
    screen_width = 600
    screen_height = 500
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Evil Pong Main Menu")

    def draw_text(text, font, color, x, y):
        img = font.render(text, True, color)
        screen.blit(img, (x, y))

    # define fonts
    font =  pygame.font.SysFont('Helvetica', 24)
    font2 = pygame.font.SysFont('Helvetica', 90)

    # define colors
    violet = (255, 62, 150)
    light_violet = (255, 153, 204)

    # game variables
    run2 = True
    while run2:
        screen.fill((36, 36, 36))

        # check if the game is paused:
        if game_paused:
            draw_text("Game paused, press O to continue", font, violet, 150, 220)
        else:
            draw_text("EVIL PONG", font2, violet, 105, 20)

            # start button
            start_rect = pygame.Rect(260, 200, 80, 40)
            mouse_pos = pygame.mouse.get_pos()
            if start_rect.collidepoint(mouse_pos):
                draw_text("Start", font, light_violet, 270, 200)
                if pygame.mouse.get_pressed()[0]:
                    print("Start button pressed")
                    start()

            else:
                draw_text("Start", font, violet, 270, 200)

            # options button
            options_rect = pygame.Rect(260, 240, 100, 40)
            if options_rect.collidepoint(mouse_pos):
                draw_text("Options", font, light_violet, 260, 240)
                if pygame.mouse.get_pressed()[0]:
                    print("Options button pressed")
                    options()
            else:
                draw_text("Options", font, violet, 260, 240)

            # scores button
            scores_rect = pygame.Rect(260, 280, 80, 40)
            if scores_rect.collidepoint(mouse_pos):
                draw_text("Scores", font, light_violet, 260, 280)
                if pygame.mouse.get_pressed()[0]:
                    print("Scores button pressed")
                    scores()
            else:
                draw_text("Scores", font, violet, 260, 280)

            # exit button
            exit_rect = pygame.Rect(275, 320, 50, 40)
            if exit_rect.collidepoint(mouse_pos):
                draw_text("Exit", font, light_violet, 275, 320)
                if pygame.mouse.get_pressed()[0]:
                    print("Exit button pressed")
                    run2 = False
            else:
                draw_text("Exit", font, violet, 275, 320)


        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_paused = True

                    print("pause")
                elif event.key == pygame.K_o:
                    game_paused = False
                    run2 = False

                if event.key == pygame.K_ESCAPE:
                    run2 = False
                    gs2.test = 10

                    print("test1 = ", gs2.test)

            if event.type == pygame.QUIT:
                run2 = False

        pygame.display.update()

run2()



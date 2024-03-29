import sys
import pygame
import pygame_gui
import json
from GameState import *

# menu file variables
pygame.init()


class GeneralMenuVariables:
    # define fonts
    font = pygame.font.SysFont('Helvetica', 24)
    font2 = pygame.font.SysFont('Helvetica', 100)

    # define colors
    violet = (255, 62, 150)
    light_violet = (255, 153, 204)
    # define the screen
    screen_width = 650
    screen_height = 500
    screen = pygame.display.set_mode((screen_width, screen_height))
    manager = pygame_gui.UIManager((screen_width, screen_height))
    # Create a slider
    slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((250, 200), (150, 20)),
        start_value=0.7,
        value_range=(0, 1.0),
        manager=manager
    )
    slider2 = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((250, 270), (150, 20)),
        start_value=0.5,
        value_range=(0, 1.0),
        manager=manager
    )


# initiate the classes
gs2 = SecondGameState()
gv = GeneralMenuVariables()


def game_exit():
    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gs2.run_start = False
                gs2.run_options = False
                gs2.run_scores = False
                gs2.run2 = True

        if event.type == pygame.QUIT:
            gs2.run_scores = False
            gs2.run_options = False
            gs2.run_start = False
            gs2.run2 = False
            gs2.run = False


def start_screen():
    print("start screen!")

    while gs2.run_start:

        pygame.display.set_caption("Evil Pong Main Menu")
        gv.screen.fill((36, 36, 36))
        draw_text("Press ESC to return to main menu", gv.font, gv.light_violet, gv.screen_width // 2, 450)

        # drawing rectangles for capturing the mouse key press
        diff_1 = pygame.Rect(140, 150, 300, 30)
        diff_2 = pygame.Rect(140, 230, 300, 20)
        diff_3 = pygame.Rect(140, 285, 300, 20)
        mouse_pos = pygame.mouse.get_pos()

        # drawing the text difficulty levels and redirecting to the main.py file
        if diff_1.collidepoint(mouse_pos):
            draw_text("Difficulty 1 - no random events", gv.font, gv.light_violet, gv.screen_width // 2, 150)
            if pygame.mouse.get_pressed()[0]:
                print("difficulty 1 selected")
                gs2.difficulty = 1
                print(gs2.difficulty)
                reset_vars()
        else:
            draw_text("Difficulty 1 - no random events", gv.font, gv.violet, gv.screen_width // 2, 150)

        if diff_2.collidepoint(mouse_pos):
            draw_text("Diffuculty 2 - Some random events", gv.font, gv.light_violet, gv.screen_width // 2, 222)

            if pygame.mouse.get_pressed()[0]:
                print("difficulty 2 selected")
                gs2.difficulty = 2
                print(gs2.difficulty)
                reset_vars()
        else:
            draw_text("Diffuculty 2 - Some random events", gv.font, gv.violet, gv.screen_width // 2, 222)

        if diff_3.collidepoint(mouse_pos):
            draw_text("Difficulty 3 - May the gods of probability save you", gv.font, gv.light_violet,
                      gv.screen_width // 2, 290)

            if pygame.mouse.get_pressed()[0]:
                print("difficulty 3 selected")
                gs2.difficulty = 3
                print(gs2.difficulty)
                reset_vars()
        else:
            draw_text("Difficulty 3 - May the gods of probability save you", gv.font, gv.violet, gv.screen_width // 2,
                      290)

        game_exit()

        pygame.display.update()


def options():
    print("options screen")
    while gs2.run_options:
        # time_delta is for the drawing the sliders in real time
        time_delta = pygame.time.Clock().tick(60) / 1000.0
        # getting the current value from the sliders
        # sound slider
        slider_value = gv.slider2.get_current_value()
        # music slider
        slider_value2 = gv.slider.get_current_value()
        pygame.display.set_caption("Evil Pong Options Menu")
        gv.screen.fill((36, 36, 36))

        # draw text on screen
        draw_text("Music", gv.font, gv.violet, gv.screen_width // 2, 180)
        draw_text("Sound", gv.font, gv.violet, gv.screen_width // 2, 250)
        draw_text("Press ESC to return to main menu", gv.font, gv.light_violet, gv.screen_width // 2, 450)

        gv.manager.draw_ui(gv.screen)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gs2.run_options = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # get value from the slider
            gv.manager.process_events(event)
            gs2.volume = slider_value
            gs2.volume2 = slider_value2

            # loop for setting the volume of all the sounds in the "sounds" list
            for sound in gs2.sounds:
                sound.set_volume(gs2.volume)

            pygame.mixer.music.set_volume(gs2.volume2)

        gv.manager.update(time_delta)

        game_exit()
        pygame.display.update()


def scores():
    print("scores screen")
    while gs2.run_scores:

        pygame.display.set_caption("Evil Pong Scores Menu")
        gv.screen.fill((36, 36, 36))
        draw_text("Press ESC to return to main menu", gv.font, gv.light_violet, gv.screen_width // 2, 450)
        try:
            with open("scores.json", "r") as scores:
                data = json.load(scores)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            print("File not found")
            return

        scores = data["scores"]
        scores = scores[-8:]  # get the last 10 scores

        # Display scores on screen
        y = 50
        for score in scores:
            date = score["date"]
            player_score = score["Player"]
            cpu_score = score["CPU"]
            difficulty = score["difficulty"]
            rounds = score["rounds"]

            text = gv.font.render(
                f"{date}: Player: {player_score}, CPU: {cpu_score}, Difficulty: {difficulty}, Rounds: {rounds}", True,
                (200, 80, 240))
            gv.screen.blit(text, (40, y))
            y += 50

        game_exit()

        pygame.display.update()


pygame.display.set_caption("Evil Pong Main Menu")


def draw_text(text, font, color, x, y):
    img = gv.font.render(text, True, color)
    text_rect = img.get_rect()
    text_rect.center = (x, y)
    gv.screen.blit(img, text_rect)


def draw_large_text(text, font, color, x, y):
    img = gv.font2.render(text, True, color)
    text_rect = img.get_rect()
    text_rect.center = (x, y)
    gv.screen.blit(img, text_rect)


def reset_vars():
    gs2.run_start = False
    gs2.run2 = False
    gs2.player_score = 0
    gs2.cpu_score = 0
    gs2.rounds = 0


# Main game loop
def run2(game_paused=False):
    # setting up the game menu screen
    pygame.mixer.music.load(gs2.menu_music)
    pygame.mixer.music.play(-1)

    pygame.display.set_caption("Evil Pong Main Menu")
    # setting up the game sounds volume:
    while gs2.run2:
        for sound in gs2.sounds:
            sound.set_volume(gs2.volume)

        # game variables
        gv.screen.fill((36, 36, 36))
        gs2.run_start = True
        gs2.run_options = True
        gs2.run_scores = True
        # check if the game is paused:
        if game_paused:
            draw_text("Game paused, press O to continue", gv.font, gv.violet, gv.screen_width // 2, 220)
        else:
            draw_large_text("EVIL PONG", gv.font2, gv.violet, gv.screen_width // 2, 80)

            # start button
            start_rect = pygame.Rect(260, 200, 80, 40)
            mouse_pos = pygame.mouse.get_pos()
            if start_rect.collidepoint(mouse_pos):
                draw_text("Start", gv.font, gv.light_violet, gv.screen_width // 2, 200)
                if pygame.mouse.get_pressed()[0]:
                    print("Start button pressed")
                    start_screen()
            else:
                draw_text("Start", gv.font, gv.violet, gv.screen_width // 2, 200)

            # options button
            options_rect = pygame.Rect(260, 240, 100, 40)

            if options_rect.collidepoint(mouse_pos):
                draw_text("Options", gv.font, gv.light_violet, gv.screen_width // 2, 240)
                if pygame.mouse.get_pressed()[0]:
                    print("Options button pressed")
                    options()
            else:
                draw_text("Options", gv.font, gv.violet, gv.screen_width // 2, 240)

            # scores button
            scores_rect = pygame.Rect(260, 280, 80, 40)

            if scores_rect.collidepoint(mouse_pos):
                draw_text("Scores", gv.font, gv.light_violet, gv.screen_width // 2, 280)
                if pygame.mouse.get_pressed()[0]:
                    print("Scores button pressed")
                    scores()
            else:
                draw_text("Scores", gv.font, gv.violet, gv.screen_width // 2, 280)

            # exit button
            exit_rect = pygame.Rect(285, 320, 50, 40)
            if exit_rect.collidepoint(mouse_pos):
                draw_text("Exit", gv.font, gv.light_violet, gv.screen_width // 2, 320)
                if pygame.mouse.get_pressed()[0]:
                    print("Exit button pressed")
                    sys.exit()

            else:
                draw_text("Exit", gv.font, gv.violet, gv.screen_width // 2, 320)

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_paused = True
                    gs2.run = False
                    print("pause")
                elif event.key == pygame.K_o:
                    game_paused = False
                    gs2.run2 = False
                    gs2.run = True
                if event.key == pygame.K_ESCAPE:
                    gs2.run2 = False
                    if gs2.run:
                        gs2.run2 = True
            if event.type == pygame.QUIT:
                gs2.run2 = False
                gs2.run = False
                sys.exit()

        pygame.display.update()


run2()

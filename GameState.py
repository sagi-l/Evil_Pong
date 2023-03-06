# a class with the game variables that both the main.py and menu.py uses
import pygame.mixer
from pygame.mixer import Sound
pygame.mixer.init()


class GameState:

    def __init__(self, player_size=False, many_balls=False, ai_size=False, reverse_keys=False,
                 random_movement=False, invisible=False, ball_size=False,
                 ball_size2=False, static=False, static2=False, reverse_roles=False, evil_score=False):
        self.ai_size = ai_size
        self.many_balls = many_balls
        self.player_size = player_size
        self.reverse_keys = reverse_keys
        self.random_movement = random_movement
        self.invisible = invisible
        self.ball_size = ball_size
        self.ball_size2 = ball_size2
        self.static = static
        self.static2 = static2
        self.reverse_roles = reverse_roles
        self.evil_score = evil_score
        # game difficulty


# a class with the game variable that both the main.py and menu.py uses and does not reset after each game
class SecondGameState:
    random_event = False
    difficulty = 0
    run = True
    run2 = True
    run_start = True
    run_options = True
    run_scores = True
    cpu_score = 0
    player_score = 0
    rounds = 0
    volume = 0.5
    volume2 = 0.5
    menu_music = ('Assets/Menu_music.wav')
    #game_music =
    #random_event_music =

    sounds: list[Sound] = [pygame.mixer.Sound('Assets/player_paddle_1.wav'),
                           pygame.mixer.Sound('Assets/Cpu_paddle_1.wav'), pygame.mixer.Sound('Assets/Margin_1.wav'),
                           pygame.mixer.Sound('Assets/Bottom_1.wav'), pygame.mixer.Sound('Assets/WON.wav'),
                           pygame.mixer.Sound('Assets/LOST.wav'), pygame.mixer.Sound('Assets/player_paddle_WOB.wav'),
                           pygame.mixer.Sound('Assets/Cpu_paddle_WOB.wav'), pygame.mixer.Sound('Assets/Margin_WOB.wav'),
                           pygame.mixer.Sound('Assets/Bottom_WOB.wav'), pygame.mixer.Sound('Assets/WON_WOB.wav'),
                           pygame.mixer.Sound('Assets/WON_WOB.wav')]
    """""
    sounds list index: player_paddle: 0, Cpu_paddle: 1, Margin_1: 2, Bottom_1: 3, WON: 4, LOST: 5, Player_WOB: 6,
    CPU_WOB: 7, Margin_WOB: 8, Bottom_WOB: 9, WON_WOB: 10, LOST_WOB: 11
    """""
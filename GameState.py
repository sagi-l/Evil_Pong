# class with the game variables that both the main.py and menu.py uses
import pygame.mixer
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
    difficulty = 0
    run = True
    run2 = True
    run_start = True
    run_options = True
    run_scores = True
    cpu_score = 0
    player_score = 0
    rounds = 0


    channel = pygame.mixer.Channel(0)
    sound1 = pygame.mixer.Sound('Assets/player_paddle_1.wav')
    sound2 = pygame.mixer.Sound('Assets/Cpu_paddle_1.wav')
    sound3 = pygame.mixer.Sound('Assets/Margin_1.wav')
    sound4 = pygame.mixer.Sound('Assets/Bottom_1.wav')
    sound5 = pygame.mixer.Sound('Assets/WON.wav')
    sound6 = pygame.mixer.Sound('Assets/LOST.wav')
    # sound effects:
    # wobble
    sound1W = pygame.mixer.Sound('Assets/player_paddle_WOB.wav')
    sound2W = pygame.mixer.Sound('Assets/Cpu_paddle_WOB.wav')
    sound3W = pygame.mixer.Sound('Assets/Margin_WOB.wav')
    sound4W = pygame.mixer.Sound('Assets/Bottom_WOB.wav')
    sound5W = pygame.mixer.Sound('Assets/WON_WOB.wav')
    sound6W = pygame.mixer.Sound('Assets/LOST_WOB.wav')

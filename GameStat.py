

class GameState:
    def __init__(self, player_size = False, many_balls = False, ai_size = False, reverse_keys =  False,
                 random_movement = False, invisible = False, ball_size = False,
                 ball_size2 = False, static = False, difficulty = None):

        self.many_balls = many_balls
        self.player_size = player_size
        self.ai_size = ai_size
        self.reverse_keys = reverse_keys
        self.random_movement = random_movement
        self.invisible = invisible
        self.ball_size = ball_size
        self.ball_size2 = ball_size2
        self.static = static
        # game difficulty
        self.difficulty = difficulty

class SecondGameState:
    test = None


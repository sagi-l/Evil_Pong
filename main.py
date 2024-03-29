import math
import random
from datetime import datetime
import pygame.time
import pygame.mixer
import pygame.mixer_music
from pygame.locals import *
from menu import *
from GameState import *
from GeneralMainVariables import *

# initiating pygame
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Evil Pong")

# initiating GameState class
gs = GameState()
gmv = GeneralMainVariables()
difficulty = gs2.difficulty
random_num = gmv.random_num

# setting up sounds
pygame.mixer.init()


class Paddle:
    color_1 = (200, 200, 200)

    def __init__(self, x, y):
        self.reset(x, y)

    def move(self):
        if not gs.reverse_keys:
            key = pygame.key.get_pressed()
            if key[pygame.K_UP] and self.rect.top > gmv.margin:
                self.rect.move_ip(0, -1 * self.speed)
            if key[pygame.K_DOWN] and self.rect.bottom < gmv.screen_height:
                self.rect.move_ip(0, self.speed)
        else:
            key = pygame.key.get_pressed()
            if key[pygame.K_DOWN] and self.rect.top > gmv.margin:
                self.rect.move_ip(0, -1 * self.speed)
            if key[pygame.K_UP] and self.rect.bottom < gmv.screen_height:
                self.rect.move_ip(0, self.speed)

    def ai(self):
        # ai to move the paddle automatically
        # move down
        if self.rect.centery < game_object.pong.rect.top and self.rect.bottom < gmv.screen_height:
            self.rect.move_ip(0, self.ai_speed)
        # move up
        if self.rect.centery > game_object.pong.rect.bottom and self.rect.top > gmv.margin:
            self.rect.move_ip(0, -1 * self.ai_speed)

    def draw(self, color1):
        if gs.invisible:
            # a random event that make the paddle almost invisible
            pygame.draw.rect(gmv.screen, gmv.bg2, self.rect)
        else:
            pygame.draw.rect(gmv.screen, color1, self.rect)
            # make the paddle red (when losing)
            if not gmv.red_paddle:
                pygame.draw.rect(gmv.screen, gmv.red, self.rect)


    def draw2(self):
        pygame.draw.rect(gmv.screen, gmv.light_grey, self.rect)
        if not gmv.red_cpu_paddle:
            pygame.draw.rect(gmv.screen, gmv.red, self.rect)

    def update(self):

        if self.rect.height >= self.max_size:
            self.size_direction = -3
        elif self.rect.height <= self.min_size:
            self.size_direction = 1
        self.rect.height += self.size_change * self.size_direction

        middle_y = self.rect.centery

        # Adjust the paddle height and y-coordinate based on the size change
        self.rect.height += self.size_change * self.size_direction
        if self.rect.top == gmv.margin:
            self.rect.height -= self.size_change
        if self.rect.bottom >= gmv.screen_height:
            self.rect.height += self.size_change
        self.rect.centery = middle_y


    def reset(self, x, y):
        self.x = x
        self.y = y
        # defining the size and width of the paddles:
        self.rect = Rect(self.x, self.y, 8, 60)
        self.speed = 5
        self.ai_speed = 5
        self.min_size = 10
        self.max_size = 100
        self.size_change = 1
        self.size_direction = 1
        if gs.ai_size:
            self.min_size = 50
            self.max_size = 180


class StaticPaddle(Paddle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = Rect(self.x, self.y, 8, 100)


class Ball:

    def __init__(self, x, y):
        self.reset(x, y)

    def move(self):

        # check collision with top gmv.margin
        if self.rect.top < gmv.margin:
            self.speed_y *= -1
            if not gs.ball_size and not gs.ball_size2:
                pygame.mixer.Sound.play(gs2.sounds[2])
            else:
                pygame.mixer.Sound.play(gs2.sounds[8])
        # check collision with bottom of the screen
        if self.rect.bottom > gmv.screen_height:
            self.speed_y *= -1
            if not gs.ball_size and not gs.ball_size2:
                pygame.mixer.Sound.play(gs2.sounds[3])

            else:
                pygame.mixer.Sound.play(gs2.sounds[9])
        # check collision with cpu paddle
        if self.rect.colliderect(game_object.cpu2):
            if abs(self.rect.left - game_object.cpu2.rect.right) < 10:
                self.speed_x *= -1
                if gs.evil_score:
                    gs2.cpu_score += 1
            elif abs(self.rect.bottom - game_object.cpu2.rect.top) < 10 and self.speed_y > 0:
                self.speed_x *= -1
                self.speed_y *= -1
            elif abs(self.rect.top - game_object.cpu2.rect.bottom) < 10 and self.speed_y < 0:
                self.speed_x *= -1
                self.speed_y *= -1
            if not gs.ball_size and not gs.ball_size2:
                pygame.mixer.Sound.play(gs2.sounds[1])
            else:
                pygame.mixer.Sound.play(gs2.sounds[7])

        # check collision with player paddle
        if self.rect.colliderect(game_object.player_paddle) and self.speed_x > 0:
            if abs(self.rect.right - game_object.player_paddle.rect.left) < 20:
                self.speed_x *= -1
            elif abs(self.rect.bottom - game_object.player_paddle.rect.top) < 20 and self.speed_y > 0:
                self.speed_x *= -1
                self.speed_y *= -1
            elif abs(self.rect.top - game_object.player_paddle.rect.bottom) < 20 and self.speed_y < 0:
                self.speed_x *= -1
                self.speed_y *= -1
            if not gs.ball_size and not gs.ball_size2:

                pygame.mixer.Sound.play(gs2.sounds[0])
            else:

                pygame.mixer.Sound.play(gs2.sounds[6])
        # check for out of bounds
        if self.rect.left < 0:
            self.winner = 1

        if self.rect.left > gmv.screen_width:
            self.winner = -1

        # update ball position and activate random movement
        if gs.random_movement:
            self.rect.y += self.speed_y
            self.rect.x += self.speed_x * (gmv.y * math.cos(gmv.angle2) - 100 and gmv.x * math.sin(gmv.angle2) / 5)
        else:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

        return self.winner

    # collision detection with static paddles from a random event
    def static1(self):

        if self.rect.colliderect(game_object.static_paddle1) or self.rect.colliderect(game_object.static_paddle2):
            self.speed_x *= -1

            pygame.mixer.Sound.play(gs2.sounds[3])

    def static2(self):

        if self.rect.colliderect(game_object.static_paddle3) or self.rect.colliderect(game_object.static_paddle4) \
                or self.rect.colliderect(game_object.static_paddle5) or self.rect.colliderect(
            game_object.static_paddle6):
            self.speed_x *= -1
            pygame.mixer.Sound.play(gs2.sounds[3])

    def draw(self):
        pygame.draw.circle(gmv.screen, gmv.light_grey, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad),
                           self.ball_rad)

    def draw2(self):
        pygame.draw.circle(gmv.screen, gmv.violet, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad),
                           self.ball_rad)

    # ball size change random event
    def ball_size(self):

        self.max_size = 100
        self.min_size = 30

        if self.ball_rad >= self.max_size:
            self.size_direction = -1
        elif self.ball_rad <= self.min_size:
            self.size_direction = 1
        self.ball_rad += self.size_change * self.size_direction

    def ball_size2(self):

        if self.ball_rad >= self.max_size:
            self.size_direction = -1
        elif self.ball_rad <= self.min_size:
            self.size_direction = 1
        self.ball_rad += self.size_change * self.size_direction

    def reset(self, x, y):
        self.size_change = 1
        self.size_direction = 1
        self.max_size = 20
        self.min_size = 1
        self.x = x
        self.y = y
        self.ball_rad = 6
        self.rect = Rect(x, y, self.ball_rad * 2, self.ball_rad * 2)
        self.speed_x = random.choice([3, -3])
        self.speed_y = random.choice([4, -4])
        self.winner = 0  # 1 is the player and -1 is the CPU
        return self.winner


class GameObjects:
    # create paddles:
    player_paddle = Paddle(gmv.screen_width - 30, gmv.screen_height // 2 - 20)
    cpu2 = Paddle(25, gmv.screen_height // 2 - 20)

    # static paddles (walls):
    static_paddle1 = StaticPaddle(gmv.screen_width // 2, gmv.screen_height // 10)
    static_paddle2 = StaticPaddle(gmv.screen_width // 2, gmv.screen_height - 100)
    # static paddles 2 (more walls):
    static_paddle3 = StaticPaddle(random.randrange(40,600), random.randrange(20,400))
    static_paddle4 = StaticPaddle(random.randrange(40,600), random.randrange(20,400))
    static_paddle5 = StaticPaddle(random.randrange(40,600), random.randrange(20,400))
    static_paddle6 = StaticPaddle(random.randrange(40,600), random.randrange(20,400))
    # create balls:
    pong = Ball(gmv.screen_width - 60, gmv.screen_height // 2 + 15)
    pong2 = Ball(gmv.screen_width - 80, gmv.screen_height // 2 + 15)
    pong3 = Ball(gmv.screen_width - 80, gmv.screen_height // 2 + 15)
    pong4 = Ball(gmv.screen_width - 80, gmv.screen_height // 2 + 15)


game_object = GameObjects


# general game functions
# creating the game board and background
def draw_board():
    # filling the screen with one color (gmv.bg)
    gmv.screen.fill(gmv.bg)
    # drawing a line in the middle of the screen
    pygame.draw.aaline(gmv.screen, gmv.light_grey, (gv.screen_width // 2, 500), (gv.screen_width // 2, 50))
    # drawing a line in the upper part of the screen
    pygame.draw.line(gmv.screen, gmv.light_grey, (0, gmv.margin), (gmv.screen_width, gmv.margin))


# functions for displaying text on screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    gmv.screen.blit(img, (x, y))


def draw_text2(text, font, text_col, x, y, bg):
    img = font.render(text, True, text_col, bg)
    text_rect = img.get_rect()
    text_rect.center = (x, y)
    gmv.screen.blit(img, text_rect)


# random events generator
def random_gen(random_number):
    num_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    w = [1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6]
    for i in range(1):
        choice = (random.choices(num_list, w, k=1))
    return choice


# gradual speed increase function
def speed_increase():
    if gmv.speed_increase > 500:
        gmv.speed_increase = 0
        if game_object.pong.speed_x < 0:
            game_object.pong.speed_x -= 1
        if game_object.pong.speed_x > 0:
            game_object.pong.speed_x += 1
        if game_object.pong.speed_y < 0:
            game_object.pong.speed_y -= 1
        if game_object.pong.speed_y > 0:
            game_object.pong.speed_y += 1


# resetting game objects locations
def objects_reset():
    game_object.player_paddle.reset(gmv.screen_width - 30, gmv.screen_height // 2 - 20)
    game_object.cpu2.reset(25, gmv.screen_height // 2 - 20)
    game_object.pong.reset(gmv.screen_width - 300, gmv.screen_height // 2 + 5)
    game_object.pong2.reset(gmv.screen_width - 300, gmv.screen_height // 2 + 5)
    game_object.pong3.reset(gmv.screen_width - 300, gmv.screen_height // 2 + 5)
    game_object.pong4.reset(gmv.screen_width - 300, gmv.screen_height // 2 + 5)
    game_object.static_paddle3.reset(random.randrange(40,600), random.randrange(50, 400))
    game_object.static_paddle4.reset(random.randrange(40,600), random.randrange(50, 400))
    game_object.static_paddle5.reset(random.randrange(40,600), random.randrange(50, 400))
    game_object.static_paddle6.reset(random.randrange(40,600), random.randrange(50, 400))

# function to write the scores to a file
def write_score_to_json(player_score, cpu_score, difficulty):
    # get current date
    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    try:
        with open("scores.json", "r") as score_file:
            data = json.load(score_file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        data = {"scores": []}

    data["scores"].append({"date": date, "Player": gs2.player_score, "CPU": gs2.cpu_score, "difficulty": difficulty,
                           "rounds": gs2.rounds})

    with open("scores.json", "w") as score_file:
        json.dump(data, score_file, separators=(",", ": "), indent=4)
        score_file.write("\n")


start_time = pygame.time.get_ticks()

# main game loop
while gs2.run:
    gmv.angle1 += 0.01
    gmv.angle2 += 0.01
    gmv.timer += 1
    gmv.fpsClock.tick(gmv.fps)
    draw_board()
    draw_text('CPU: ' + str(gs2.cpu_score), gmv.font, gmv.light_grey, 30, 15)
    draw_text(gmv.p1 + str(gs2.player_score), gmv.font, gmv.light_grey, gmv.screen_width - 70, 15)
    draw_text('Speed: ' + str(abs(game_object.pong.speed_x) - 2), gmv.font, gmv.light_grey, gv.screen_width - 320, 15)
    draw_text('Rounds: ' + str(gs2.rounds), gmv.font, gmv.light_grey, gv.screen_width - 400, 15)
    # drawing the two puddles:
    game_object.player_paddle.draw(Paddle.color_1)
    game_object.cpu2.draw2()
    if gs2.random_event:
        draw_text2('RANDOM EVENT', gmv.font, gmv.violet, gmv.screen_width // 2, gmv.screen_height - 450, gmv.bg)
    else:
        pass

    if gmv.live_ball:
        gmv.speed_increase += 1

        # stopping the menu_music first
        pygame.mixer.music.stop()
        gmv.winner = game_object.pong.move()

        if gmv.winner == 0:
            game_object.pong.draw2()
            # draw ball

            # adding more balls random event
            if gs.many_balls:
                game_object.pong2.draw2()
                game_object.pong2.move()
                game_object.pong3.draw2()
                game_object.pong3.move()
                game_object.pong4.draw2()
                game_object.pong4.move()

            # changing the player paddle size
            if gs.player_size:
                game_object.player_paddle.update()
            # changing the ball size #1
            if gs.ball_size:
                game_object.pong.ball_size()
            # changing the ball size#2
            if gs.ball_size2:
                game_object.pong.ball_size2()
            # changing the cpu_paddle size
            if gs.ai_size:
                game_object.cpu2.update()
            # adding static paddles (as walls)
            if gs.static:
                game_object.static_paddle1.draw2()
                game_object.static_paddle2.draw2()
                game_object.pong.static1()
            # adding more static paddles (as walls)
            if gs.static2:
                game_object.static_paddle3.draw2()
                game_object.static_paddle3.update()
                game_object.static_paddle4.draw2()
                game_object.static_paddle4.update()
                game_object.static_paddle5.draw2()
                game_object.static_paddle5.update()
                game_object.static_paddle6.draw2()
                game_object.static_paddle6.update()
                game_object.pong.static2()

            # move paddles
            if gs.reverse_roles:
                game_object.player_paddle.ai()
                game_object.cpu2.move()
            else:
                game_object.player_paddle.move()
                game_object.cpu2.ai()

        else:
            gmv.live_ball = False
            if not gs.reverse_roles:
                if gmv.winner == 1:
                    if not gs.ball_size2 and not gs.ball_size:
                        pygame.mixer.Sound.play(gs2.sounds[4])
                    else:
                        pygame.mixer.Sound.play(gs2.sounds[10])
                    gs2.player_score += 1
                    gs2.rounds += 1
                    gmv.red_cpu_paddle = False
                elif gmv.winner == -1:
                    if not gs.ball_size2 and not gs.ball_size:
                        pygame.mixer.Sound.play(gs2.sounds[5])
                    else:
                        pygame.mixer.Sound.play(gs2.sounds[11])
                    gs2.cpu_score += 1
                    gs2.rounds += 1
                    gmv.red_paddle = False
            else:
                if gmv.winner == -1:
                    gs2.player_score += 1

                    gmv.red_paddle = False
                elif gmv.winner == 1:
                    gs2.cpu_score += 1
                    gs2.rounds += 1
                    gmv.red_cpu_paddle = False

    # txt on screen while reset

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            write_score_to_json(gs2.player_score, gmv.cpu_score, difficulty)
            gs2.run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                write_score_to_json(gs2.player_score, gmv.cpu_score, difficulty)
                gs2.run2 = True
                gs2.run = False
                run2()
                gmv.live_ball = False
                gs2.run = True
            if event.key == pygame.K_p:
                game_paused = True
                gs2.run2 = True
                run2(game_paused == True)
                print(game_paused)

        if event.type == pygame.MOUSEBUTTONDOWN and not gmv.live_ball:
            gmv.live_ball = True

            print("difficulty: ", gs2.difficulty)
            # resetting events triggers every time the game start
            gs = GameState()
            # resetting FPS after the FPS change random event
            gmv.fps = 60
            # difficulty selector
            if gs2.difficulty == 1:
                print(gs2.difficulty)
                choice = None
                gs2.random_event = False
            elif gs2.difficulty == 2:

                gs2.run = True
                choice2 = random_gen(random_num)
                print(f"first random: {choice2}")
                if choice2 == [2] or choice2 == [4] or choice2 == [6] or choice2 == [10]:
                    choice = random_gen(random_num)
                else:
                    choice = None
                    gs2.random_event = False
            elif gs2.difficulty == 3:
                choice2 = random_gen(random_num)
                print(f"first random: {choice2}")
                if choice2 == [1] or choice2 == [3] or choice2 == [5] or choice2 == [7] \
                        or choice2 == [9] or choice2 == [11] or choice2 == [12] or choice2 == [13] \
                        or choice2 == [14] or choice2 == [15]:
                    choice = random_gen(random_num)

                else:
                    choice = None
                    gs2.random_event = False

                    # random events
            if choice == [1]:
                gs2.random_event = True
                gs.static = True
                print(choice)
            if choice == [2]:
                gs2.random_event = True
                gs.random_movement = True
                print(choice)
            if choice == [3]:
                gs2.random_event = True
                gs.invisible = True
                print(choice)
            if choice == [4]:
                gs2.random_event = True
                gs.ball_size2 = True
                print(choice)
            if choice == [5]:
                gs2.random_event = True
                gmv.fps = 40
                gs.ball_size = True
                print(choice)
            if choice == [6]:
                gs2.random_event = True
                gs.ai_size = True
                print(choice)
            if choice == [7]:
                gs2.random_event = True
                gs.reverse_keys = True
                print(choice)
            if choice == [8]:
                gs2.random_event = True
                gs.many_balls = True
                print(choice)
            if choice == [9]:
                gs2.random_event = True
                gs.player_size = True
                print(choice)
            if choice == [10]:
                gs2.random_event = True
                gs.evil_score = True
                print(choice)
            if choice == [11]:
                gs2.random_event = True
                gs.reverse_roles = True
                print(choice)
            if choice == [12]:
                gs2.random_event = True
                gs.static2 = True
                print(choice)
            # mixed events:
            if choice == [13]:
                gs2.random_event = True
                gs.invisible = True
                gs.static2 = True
                gs.ai_size = True
                print(choice)
            if choice == [14]:
                gs2.random_event = True
                gs.static = True
                gs.static = True
                gs.many_balls = True
                print(choice)
            if choice == [15]:
                gs2.random_event = True
                gs.ball_size2 = True
                gs.reverse_keys = True
                gs.reverse_roles = True
                print("super evil")
            objects_reset()

            gmv.red_paddle = True
            gmv.red_cpu_paddle = True

        speed_increase()

    if not gmv.live_ball:
        if gmv.winner == 0:
            draw_text2('CLICK ANYWHERE TO START', gmv.font2, gmv.deep_sky, gmv.screen_width // 2, gmv.screen_height // 2, gmv.bg)

        if gmv.winner == 1:
            draw_text('YOU SCORED!', gmv.font, gmv.violet, 390, 15)
            draw_text2('CLICK ANYWHERE TO START', gmv.font2, gmv.deep_sky, gmv.screen_width // 2, gmv.screen_height // 2 , gmv.bg)

        if gmv.winner == -1:
            draw_text('CPU SCORED!', gmv.font, gmv.violet, 110, 15)
            draw_text2('CLICK ANYWHERE TO START', gmv.font2, gmv.deep_sky, gmv.screen_width // 2, gmv.screen_height // 2 , gmv.bg)

    pygame.display.update()

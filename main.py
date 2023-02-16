import math
import random
from datetime import datetime
from pygame.locals import *
from menu import *
from GameStat import *
from GeneralMainVariables import *

# initiating pygame
pygame.init()
pygame.display.set_caption("Evil Pong")

# initiating GameState class
gmv = GeneralMainVariables
gs = GameState()
difficulty = gs2.difficulty
random_num = gmv.random_num
bg = gmv.bg
bg2 = gmv.bg2


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
            pygame.draw.rect(gmv.screen, gmv.bg, self.rect)
        else:
            pygame.draw.rect(gmv.screen, color1, self.rect)
            # make the paddle red (when losing)
            if not gmv.z:
                pygame.draw.rect(gmv.screen, gmv.red, self.rect)
            # a random event that make the paddle almost invisible

    def draw2(self):
        pygame.draw.rect(gmv.screen, gmv.light_grey, self.rect)
        if not gmv.zz:
            pygame.draw.rect(gmv.screen, gmv.red, self.rect)

    def update(self):

        if self.rect.height >= self.max_size:
            self.size_direction = -1
        elif self.rect.height <= self.min_size:
            self.size_direction = 1
        self.rect.height += self.size_change * self.size_direction

    def reset(self, x, y):
        self.x = x
        self.y = y
        # defining the size and width of the paddles:
        self.rect = Rect(self.x, self.y, 8, 60)
        self.speed = 5
        self.ai_speed = 5
        self.min_size = 10
        self.max_size = 60
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
        # check collision with bottom of the screen
        if self.rect.bottom > gmv.screen_height:
            self.speed_y *= -1
        if self.rect.colliderect(game_object.player_paddle) or self.rect.colliderect(game_object.cpu2):
            self.speed_x *= -1

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
    player_paddle = Paddle(gmv.screen_width - 40, gmv.screen_height // 2 - 20)
    static_paddle1 = StaticPaddle(300, gmv.screen_height // 10)
    static_paddle2 = StaticPaddle(300, gmv.screen_height - 100)
    cpu2 = Paddle(25, gmv.screen_height // 2 - 20)
    # create balls:
    pong = Ball(gmv.screen_width - 60, gmv.screen_height // 2 + 15)
    pong2 = Ball(gmv.screen_width - 80, gmv.screen_height // 2 + 15)
    pong3 = Ball(gmv.screen_width - 80, gmv.screen_height // 2 + 15)
    pong4 = Ball(gmv.screen_width - 80, gmv.screen_height // 2 + 15)


game_object = GameObjects


# general game functions
def draw_board():
    # filling the screen with one color (gmv.bg)
    gmv.screen.fill(gmv.bg)
    # drawing a line in the middle of the screen
    pygame.draw.aaline(gmv.screen, gmv.light_grey, (300, 500), (300, 50))
    # drawing a line in the upper part of the screen
    pygame.draw.line(gmv.screen, gmv.light_grey, (0, gmv.margin), (gmv.screen_width, gmv.margin))


# function for displaying text on screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    gmv.screen.blit(img, (x, y))


def draw_text2(text, font, text_col, x, y, bg):
    img = font.render(text, True, text_col, bg)
    gmv.screen.blit(img, (x, y))


# random events generator
def random_gen(random_number):
    num_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    w = [1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6]
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


def objects_reset():
    game_object.player_paddle.reset(gmv.screen_width - 40, gmv.screen_height // 2 - 20)
    game_object.cpu2.reset(25, gmv.screen_height // 2 - 20)
    game_object.pong.reset(gmv.screen_width - 300, gmv.screen_height // 2 + 5)
    game_object.pong2.reset(gmv.screen_width - 300, gmv.screen_height // 2 + 5)
    game_object.pong3.reset(gmv.screen_width - 300, gmv.screen_height // 2 + 5)
    game_object.pong4.reset(gmv.screen_width - 300, gmv.screen_height // 2 + 5)


# function to write the scores to a file
def write_score_to_json(player_score, cpu_score, difficulty):
    # get current date
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open("scores.json", "r") as score_file:
            data = json.load(score_file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        data = {"scores": []}

    data["scores"].append({"date": date, "Player": gmv.player_score, "CPU": gmv.cpu_score, "difficulty": difficulty})

    with open("scores.json", "w") as score_file:
        json.dump(data, score_file, separators=(",", ": "), indent=4)
        score_file.write("\n")


# main game loop
while gs2.run:

    gmv.angle1 += 0.01
    gmv.angle2 += 0.01
    gmv.timer += 1
    gmv.fpsClock.tick(gmv.fps)
    draw_board()
    draw_text('CPU: ' + str(gmv.cpu_score), gmv.font, gmv.light_grey, 30, 15)
    draw_text(gmv.p1 + str(gmv.player_score), gmv.font, gmv.light_grey, gmv.screen_width - 70, 15)
    draw_text('Ball Speed: ' + str(abs(game_object.pong.speed_x)), gmv.font, gmv.light_grey, 255, 15)
    # drawing the two puddles:
    game_object.player_paddle.draw(Paddle.color_1)
    game_object.cpu2.draw2()

    if gmv.live_ball:
        gmv.speed_increase += 1

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

            # move paddles
            game_object.player_paddle.move()
            game_object.cpu2.ai()

        else:
            gmv.live_ball = False
            if gmv.winner == 1:
                gmv.player_score += 1
                gmv.zz = False
            elif gmv.winner == -1:
                gmv.cpu_score += 1
                gmv.z = False

    # txt on screen while reset
    if not gmv.live_ball:
        if gmv.winner == 0:
            draw_text2('CLICK ANYWHERE TO START', gmv.font2, gmv.deep_sky, 160, gmv.screen_height // 2 - 6, gmv.bg)

        if gmv.winner == 1:
            draw_text('YOU SCORED!', gmv.font, gmv.violet, 390, 15)
            draw_text2('CLICK ANYWHERE TO START', gmv.font2, gmv.deep_sky, 160, gmv.screen_height // 2 - 6, gmv.bg)
        if gmv.winner == -1:
            draw_text('CPU SCORED!', gmv.font, gmv.violet, 110, 15)
            draw_text2('CLICK ANYWHERE TO START', gmv.font2, gmv.deep_sky, 160, gmv.screen_height // 2 - 6, gmv.bg)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            write_score_to_json(gmv.player_score, gmv.cpu_score, difficulty)
            gs2.run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                write_score_to_json(gmv.player_score, gmv.cpu_score, difficulty)
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
        print(gs2.difficulty)
        # resetting events triggers every time the game start
        gs = GameState()

        # difficulty selector
        if gs2.difficulty == 1:

            print(gs2.difficulty)
            choice = None

        elif gs2.difficulty == 2:

            gs2.run = True
            choice2 = random_gen(random_num)
            print(f"first random: {choice2}")
            if choice2 == [2] or choice2 == [4] or choice2 == [6]:
                choice = random_gen(random_num)
            else:
                choice = None
        elif gs2.difficulty == 3:
            choice2 = random_gen(random_num)
            print(f"first random: {choice2}")
            if choice2 == [1] or choice2 == [3] or choice2 == [5] or choice2 == [7] \
                    or choice2 == [9] or choice2 == [11]:
                choice = random_gen(random_num)
            else:
                choice = None

        # random events
        if choice == [1]:
            print(choice)
            gs.static = True
        if choice == [2]:
            print(choice)
            gs.random_movement = True
        if choice == [3]:
            gs.invisible = True
            print(choice)
        if choice == [4]:
            gs.ball_size2 = True
            print(choice)
        if choice == [5]:
            gs.ball_size = True
            print(choice)
        if choice == [6]:
            gs.ai_size = True
            print(choice)
        if choice == [7]:
            gs.reverse_keys = True
            print(choice)
        if choice == [8]:
            gs.many_balls = True
            print(choice)
        if choice == [9]:
            gs.player_size = True
            print(choice)
        # mixed events:
        if choice == [10]:
            gs.ball_size = True
            gs.reverse_keys = True
            print(choice)
        if choice == [11]:
            gs.ball_size2 = True
            gs.invisible = True
            print(choice)
        if choice == [12]:
            gs.ai_size = True
            gs.static = True
            gs.random_movement = True
            print(choice)

        objects_reset()

        gmv.z = True
        gmv.zz = True

    speed_increase()

    pygame.display.update()

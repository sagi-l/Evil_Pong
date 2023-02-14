import math
import random
from datetime import datetime
import pygame.time
from pygame.locals import *
from menu import *
from GameStat import *

# initiating pygame
pygame.init()

# set up the game window
screen_width = 600
screen_height = 500

fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Evil Pong")

# define game variable
choice = None
z = True
zz = True
live_ball = False
margin = 50
cpu_score = 0
player_score = 0
fps = 60
p1 = "P1: "
winner = 0
ai_speed = 0
speed_increase = 0
random_num = [0]
angle1 = 0
angle2 = 0
x = 5
y = 5

# setting up random events triggers

# initiating GameState class

gs = GameState()
difficulty = gs2.difficulty


# function to write the scors to a file
def write_score_to_json(player_score, cpu_score, difficulty):
    # get current date
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open("scores.json", "r") as score_file:
            data = json.load(score_file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        data = {"scores": []}

    data["scores"].append({"date": date, "Player": player_score, "CPU": cpu_score, "difficulty": difficulty})

    with open("scores.json", "w") as score_file:
        json.dump(data, score_file, separators=(",", ": "), indent=4)
        score_file.write("\n")


class Paddle:
    color_1 = (200, 200, 200)

    def __init__(self, x, y):
        self.reset(x, y)

    def move(self):
        if not gs.reverse_keys:
            key = pygame.key.get_pressed()
            if key[pygame.K_UP] and self.rect.top > margin:
                self.rect.move_ip(0, -1 * self.speed)
            if key[pygame.K_DOWN] and self.rect.bottom < screen_height:
                self.rect.move_ip(0, self.speed)
        else:
            key = pygame.key.get_pressed()
            if key[pygame.K_DOWN] and self.rect.top > margin:
                self.rect.move_ip(0, -1 * self.speed)
            if key[pygame.K_UP] and self.rect.bottom < screen_height:
                self.rect.move_ip(0, self.speed)

    def ai(self):
        # ai to move the paddle automatically
        # move down
        if self.rect.centery < pong.rect.top and self.rect.bottom < screen_height:
            self.rect.move_ip(0, self.ai_speed)
        # move up
        if self.rect.centery > pong.rect.bottom and self.rect.top > margin:
            self.rect.move_ip(0, -1 * self.ai_speed)

    def draw(self, color1):
        if gs.invisible == True:
            pygame.draw.rect(screen, bg2, self.rect)
        else:
            pygame.draw.rect(screen, color1, self.rect)
            # make the paddel red (when losing)
            if z == False:
                pygame.draw.rect(screen, red, self.rect)
            # a random event that make the paddle almost invisible

    def draw2(self):
        pygame.draw.rect(screen, light_grey, self.rect)
        if not zz:
            pygame.draw.rect(screen, red, self.rect)

    def update(self):

        if self.rect.height >= self.max_size:
            self.size_direction = -1
        elif self.rect.height <= self.min_size:
            self.size_direction = 1
        self.rect.height += self.size_change * self.size_direction

    def reset(self, x, y):
        self.x = x
        self.y = y
        # defining the size and width of the paddels:
        self.rect = Rect(self.x, self.y, 8, 60)
        self.speed = 5
        self.ai_speed = 5
        self.min_size = 10
        self.max_size = 60
        self.size_change = 1
        self.size_direction = 1
        if gs.ai_size == True:
            self.min_size = 50
            self.max_size = 180


class StaticPaddle(Paddle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = Rect(self.x, self.y, 8, 100)


class Ball():

    def __init__(self, x, y):
        self.reset(x, y)

    def move(self):

        # check collision with top margin
        if self.rect.top < margin:
            self.speed_y *= -1
        # check collision with bottom of the screen
        if self.rect.bottom > screen_height:
            self.speed_y *= -1
        if self.rect.colliderect(player_paddle) or self.rect.colliderect(cpu2):
            self.speed_x *= -1

        # check for out of bounds
        if self.rect.left < 0:
            self.winner = 1
        if self.rect.left > screen_width:
            self.winner = -1

        # update ball position and activate random movement
        if gs.random_movement:
            self.rect.y += self.speed_y
            self.rect.x += self.speed_x * (y * math.cos(angle2) - 100 and x * math.sin(angle2) / 5)
        else:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

        return self.winner

    def static1(self):

        if self.rect.colliderect(static_paddle1) or self.rect.colliderect(static_paddle2):
            self.speed_x *= -1

    def draw(self):
        pygame.draw.circle(screen, light_grey, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad),
                           self.ball_rad)

    def draw2(self):
        pygame.draw.circle(screen, violet, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)

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


# create puddles:
player_paddle = Paddle(screen_width - 40, screen_height // 2 - 20)
static_paddle1 = StaticPaddle(300, screen_height // 10)
static_paddle2 = StaticPaddle(300, screen_height - 100)
cpu2 = Paddle(25, screen_height // 2 - 20)
# create ball:
pong = Ball(screen_width - 60, screen_height // 2 + 15)
pong2 = Ball(screen_width - 80, screen_height // 2 + 15)
pong3 = Ball(screen_width - 80, screen_height // 2 + 15)
pong4 = Ball(screen_width - 80, screen_height // 2 + 15)

# set clock
Clock = pygame.time.Clock()
timer = 0
# define colors
# background color:
bg = (36, 36, 36)
bg2 = (38, 38, 38)

# objects colors:
light_grey = (200, 200, 200)

deep_sky = (0, 191, 255)
red = (238, 44, 44)
violet = (255, 62, 150)
violet2 = (230, 230, 50)

# define font:
font = pygame.font.SysFont('Helvetica', 18)
font2 = pygame.font.SysFont('Helvetica', 24)

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


def draw_text2(text, font, text_col, x, y, bg):
    img = font.render(text, True, text_col, bg)
    screen.blit(img, (x, y))


# random events generator
def random_gen(random_num):
    num_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    w = [1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6]
    for i in range(1):
        choice = (random.choices(num_list, w, k=1))
    return choice


# main game loop
while gs2.run:

    angle1 += 0.01
    angle2 += 0.01
    timer += 1
    fpsClock.tick(fps)
    draw_board()
    draw_text('CPU: ' + str(cpu_score), font, light_grey, 30, 15)
    draw_text(p1 + str(player_score), font, light_grey, screen_width - 70, 15)
    draw_text('Ball Speed: ' + str(abs(pong.speed_x)), font, light_grey, 255, 15)
    # drawing the two puddles:
    player_paddle.draw(Paddle.color_1)
    cpu2.draw2()

    if live_ball:
        speed_increase += 1

        winner = pong.move()

        if winner == 0:
            pong.draw2()
            # draw ball

            # adding more balls random event
            if gs.many_balls:
                pong2.draw2()
                pong2.move()
                pong3.draw2()
                pong3.move()
                pong4.draw2()
                pong4.move()

            # changing the player paddle size
            if gs.player_size:
                player_paddle.update()
            # changing the ball size #1
            if gs.ball_size:
                pong.ball_size()
            # changing the ball size#2
            if gs.ball_size2:
                pong.ball_size2()
            # changing the cpu_paddle size
            if gs.ai_size:
                cpu2.update()
            # adding static paddles (as walls)
            if gs.static:
                static_paddle1.draw2()
                static_paddle2.draw2()
                pong.static1()

            # move paddles
            player_paddle.move()
            cpu2.ai()

        else:
            live_ball = False
            if winner == 1:
                player_score += 1
                zz = False
            elif winner == -1:
                cpu_score += 1
                z = False

    # txt on screen while reset
    if live_ball == False:
        if winner == 0:
            draw_text2('CLICK ANYWHERE TO START', font2, deep_sky, 160, screen_height // 2 - 6, bg)
        if winner == 1:
            draw_text('YOU SCORED!', font, violet, 390, 15)
            draw_text2('CLICK ANYWHERE TO START', font2, deep_sky, 160, screen_height // 2 - 6, bg)
        if winner == -1:
            draw_text('CPU SCORED!', font, violet, 110, 15)
            draw_text2('CLICK ANYWHERE TO START', font2, deep_sky, 160, screen_height // 2 - 6, bg)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            write_score_to_json(player_score, cpu_score, difficulty)
            gs2.run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                write_score_to_json(player_score, cpu_score, difficulty)
                gs2.run2 = True
                gs2.run = False
                run2()
                live_ball = False
                gs2.run = True
            if event.key == pygame.K_p:
                game_paused = True
                gs2.run2 = True
                run2(game_paused == True)
                print(game_paused)

    if event.type == pygame.MOUSEBUTTONDOWN and not live_ball:
        live_ball = True
        print(gs2.difficulty)
        # resetting events triggers every time the game start
        gs = GameState()

        if gs2.difficulty == 1:
            print(gs2.difficulty)
            choice = None

        elif gs2.difficulty == 2:
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

        player_paddle.reset(screen_width - 40, screen_height // 2 - 20)
        cpu2.reset(25, screen_height // 2 - 20)
        pong.reset(screen_width - 300, screen_height // 2 + 5)
        pong2.reset(screen_width - 300, screen_height // 2 + 5)
        pong3.reset(screen_width - 300, screen_height // 2 + 5)
        pong4.reset(screen_width - 300, screen_height // 2 + 5)

        z = True
        zz = True

    if speed_increase > 500:
        speed_increase = 0
        if pong.speed_x < 0:
            pong.speed_x -= 1

        if pong.speed_x > 0:
            pong.speed_x += 1
        if pong.speed_y < 0:
            pong.speed_y -= 1
        if pong.speed_y > 0:
            pong.speed_y += 1

    pygame.display.update()

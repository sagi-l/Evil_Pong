import math
import pygame
from pygame.locals import *
from time import sleep
import random
import pygame_gui
import random_gen

pygame.init()

# set up the game window
screen_width = 600
screen_height = 500

MANAGER = pygame_gui.UIManager((screen_width, screen_height))

fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Evil Pong")

# define game variable
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
num_list = [1, 2, 3, 4]
w = [1 / 6, 1 / 6, 1 / 2, 1 / 24]
angle1 = 0
angle2 = 0
x = 5
y = 5

# random events triggers:
player_size = False
ai_size = False
paddel_size = False
reverse_keys = False
random_movment = False
invisible = False
ball_size = False
ball_size2 = False
static = False

class Paddle:
    color_1 = (200, 200, 200)

    def __init__(self, x, y):
        self.reset(x, y)

    def move(self):
        if reverse_keys == False:
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
        pygame.draw.rect(screen, color1, self.rect)
        # make the paddel red (when losing)
        if z == False:
            pygame.draw.rect(screen, red, self.rect)
        # a random event that make the paddle almost invisible
        if invisible == True:
            pygame.draw.rect(screen, bg2, self.rect)

    def draw2(self):
        pygame.draw.rect(screen, light_grey, self.rect)
        if zz == False:
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


class CPUPaddle(Paddle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.min_size = 50
        self.max_size = 180
        self.size_change = 1
        self.size_direction = 1


class static_paddle(Paddle):
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
        if self.rect.colliderect(player_paddle) or self.rect.colliderect(static_paddle1) or self.rect.colliderect(
                static_paddle2) or self.rect.colliderect(cpu2):
            self.speed_x *= -1
        if static == False:
            if self.rect.colliderect(static_paddle1) or self.rect.colliderect(static_paddle2):
                self.speed_x *= -1

        # check for out of bounds
        if self.rect.left < 0:
            self.winner = 1
        if self.rect.left > screen_width:
            self.winner = -1

        # update ball position

        if random_movment == True:
            self.rect.y += self.speed_y
            self.rect.x += self.speed_x * (y * math.cos(angle2) - 100 and x * math.sin(angle2) / 5)
        else:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

        return self.winner

    def draw(self):
        pygame.draw.circle(screen, light_grey, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad),
                           self.ball_rad)

    def draw2(self):
        pygame.draw.circle(screen, violet, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)

    def ball_size(self):
        if ball_size2 == True:
            self.max_size = 100
            self.min_size = 30

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
static_paddle1 = static_paddle(300, screen_height // 10)
static_paddle2 = static_paddle(300, screen_height - 100)
cpu2 = CPUPaddle(25, screen_height // 2 - 20)
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


run = True
"""
loggedInPLayer = readUserInput()
with("sagie.leibman.txt") as f:
    player_score_line = f.readline()
    player_name, player_score = player_score_line.split(' ')
    if loggedInPLayer == player_name:
        scoreScreen.update_player_score(player_score)

with(file("sagie.leibman.txt")) as f:
    f.writeline(f'{player_name} {player_score}', line_index)

# p1 = input("please enter your name: ")
"""

# main game loop
while run:
    timer += 1
    fpsClock.tick(fps)
    draw_board()
    draw_text('CPU: ' + str(cpu_score), font, light_grey, 30, 15)
    draw_text(p1 + str(player_score), font, light_grey, screen_width - 70, 15)
    draw_text('Ball Speed: ' + str(abs(pong.speed_x)), font, light_grey, 255, 15)
    angle1 += 0.01
    angle2 += 0.01
    # drawing the two puddles:
    player_paddle.draw(Paddle.color_1)
    cpu2.draw2()
    if timer == 400:
        print("tick")
        timer = 0

    if live_ball == True:
        speed_increase += 1
        speed_increase += 1
        winner = pong.move()
        if ball_size == True:
            pong.ball_size()
        if player_size == True:
            player_paddle.update()
        if ai_size == True:
            cpu2.update()
        if static == True:
            static_paddle1.draw2()
            static_paddle2.draw2()

        if winner == 0:
            # draw ball
            pong.draw2()
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

    # to create a second ball (pong) with a diffrent color (i've creating a seconed draw method at the Ball class:
    # pong2.draw2()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
            live_ball = True
            pong.reset(screen_width - 300, screen_height // 2 + 5)
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

""" 

while not game.finished():
    CPUPaddle.updatePosition()
    PlayerPaddle.updatePosition()

    if random(10) == 1:
        ball.update_speed(100)

    if CPUPaddle.game_lost() or PlayerPaddle.game_lost():
        CPUPaddle.update_score()
        game.draw_summary()
        sleep(3)
    if keyboard.keypressed("q):
        game.set_finished()
    pygame.display.update()
"""

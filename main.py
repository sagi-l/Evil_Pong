import pygame
from pygame.locals import *
from time import sleep

pygame.init()

# set up the game window
screen_width = 600
screen_height = 500


fpsClock= pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Evil Pong")

# define game variable
live_ball = False
margin = 50
cpu_score = 0
player_score = 0
fps = 60
p1 = "P1: "
winner = 0
ai_speed = 1

class Paddle():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # defining the size and width of the paddels:
        self.rect = Rect(self.x, self.y, 10, 70)
        self.speed = 5
        self.ai_speed = 4
    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and self.rect.top > margin:
            self.rect.move_ip(0, -1 * self.speed)
        if key[pygame.K_DOWN]and self.rect.bottom < screen_height:
            self.rect.move_ip(0, self.speed)

    def ai(self):
        # ai to move the paddle automatically
        # move down
        if self.rect.centery < pong.rect.top and self.rect.bottom < screen_height:
            self.rect.move_ip(0, self.ai_speed)
        # move up
        if self.rect.centery > pong.rect.bottom and self.rect.top > margin:
            self.rect.move_ip(0, -1 * self.ai_speed)

    def draw(self):
        pygame.draw.rect(screen, light_grey, self.rect)

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
        if self.rect.colliderect(player_paddle) or self.rect.colliderect(cpu_paddle):
            self.speed_x *= -1

        # check for out of bounds
        if self.rect.left < 0:
            self.winner = 1
        if self.rect.left > screen_width:
            self.winner = -1

        # update ball position
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.winner

    def draw(self):
        pygame.draw.circle(screen, light_grey, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad),self.ball_rad)

    def draw2(self):
        pygame.draw.circle(screen, violet, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad),self.ball_rad)


    def reset(self, x, y):
        self.x = x
        self.y = y
        self.ball_rad = 8
        self.rect = Rect(x, y, self.ball_rad * 2, self.ball_rad * 2)
        self.speed_x = -4
        self.speed_y = 4
        self.winner = 0  # 1 is the player and -1 is the CPU



# create puddles:
player_paddle = Paddle(screen_width - 40, screen_height // 2 -20)
cpu_paddle = Paddle(20, screen_height // 2 -20)


# create ball:
pong = Ball(screen_width -60, screen_height // 2 + 15)
pong2 = Ball(screen_width -80, screen_height // 2 + 15)

# set clock
Clock = pygame.time.Clock()

# define colors
# background color:
bg = (36, 36, 36)

#objects colors:
light_grey = (200, 200, 200)
deep_sky = (0,191,255)
red = (238,44,44)
violet = (255,62,150)

# define font:
font = pygame.font.SysFont('Helvetica', 18)


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


run = True

#p1 = input("please enter your name: ")

#main game loop
while run:
    fpsClock.tick(fps)
    draw_board()
    draw_text('CPU: ' + str(cpu_score), font, light_grey, 30, 15)
    draw_text(p1 + str(player_score), font, light_grey, screen_width - 70, 15)

    # drawing the two puddles:
    player_paddle.draw()
    cpu_paddle.draw()

    if live_ball == True:

        winner = pong.move()
        if winner == 0:
            # draw ball
            pong.draw2()

            # move paddles
            player_paddle.move()
            cpu_paddle.ai()


        else:
            live_ball = False
            if winner == 1:
                player_score += 1
            elif winner == -1:
                cpu_score += 1




    #to create a second ball (pong) with a diffrent color (i've creating a seconed draw method at the Ball class:
    #pong2.draw2()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
            live_ball = True
            pong.reset(screen_width - 60, screen_height // 2 + 50)

    pygame.display.update()

pygame.quit()

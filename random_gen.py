import random

player_size = False
ai_size = False
paddel_size = False
reverse_keys = False
random_movment = False
invisible = False
ball_size = False
ball_size2 = False
static = False
def random_events():
    num_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    w = [1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6]
    for i in range(1):
        x = (random.choices(num_list, w, k=1))
        # draw_text('RANDOM EVENT!!!', font, violet, 255, 15)
        if x == [1]:
            # big ball
            return ball_size2 == True
        elif x == [2]:
            # randomly changing the ball size
            print("2")
            # samll ball
            return ball_size == True

        elif x == [3]:
            print("3")
            # adding more evil balls
            pass
            """"
            pong2.draw2()
            pong3.draw2()
            pong4.draw2()
            pong2.move()
            pong3.move()
            pong4.move()
            """

        elif x == [4]:
            print("4")
            # changing the ball behavior
            return random_movment == True

        elif x == [5]:
            print("5")
            # chaning the cpu paddle size
            return ai_size == True
        elif x == [6]:
            print("6")
            return player_size == True
        elif x == [7]:
            print("7")
            # reversing the player keys
            return reverse_keys == True

        elif x == [8]:
            print("8")
            # making the player paddle invisible:
            return invisible == True
        elif x == [9]:
            print("9")
            # adding static paddles in the middle of the screen
            return static == True

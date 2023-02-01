import pygame

pygame.init()

screen_width = 600
screen_height = 500

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Evil Pong Main Menu")

def draw_text(text,font, text_col, x,y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

#define fonts
font =  pygame.font.SysFont('Helvetica', 24)
font2 = pygame.font.SysFont('Helvetica', 90)



# define colors
txt_col = (255, 62, 150)

# game variables
game_paused = False

run = True
while run:
    screen.fill((36, 36, 36))

    #check if the games is pasued:
    if game_paused == True:
        draw_text("Game pasued,  press O to continue ", font, txt_col, 150, 220)
        #display menu
    else:
        #draw_text("Press P to pause", font, txt_col, 230, 220)
        draw_text("EVIL PONG", font2, txt_col, 105, 20)
        draw_text("Start", font, txt_col, 270, 200)
        draw_text("Options", font, txt_col, 260, 240)
        draw_text("Scores", font, txt_col, 260, 280)
        draw_text("Exit", font, txt_col, 275, 320)



    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                game_paused = True
                print("pause")
            elif event.key == pygame.K_o:
                game_paused = False
                print ("unpause")

            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
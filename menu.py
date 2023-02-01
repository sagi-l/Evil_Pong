import pygame
run = True
pygame.init()

def run2(run=True, game_paused=False):
    screen_width = 600
    screen_height = 500

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Evil Pong Main Menu")

    def draw_text(text,font, violet, x,y):
        img = font.render(text, True, violet)
        screen.blit(img, (x,y))

    #define fonts
    font =  pygame.font.SysFont('Helvetica', 24)
    font2 = pygame.font.SysFont('Helvetica', 90)



    # define colors
    violet = (255, 62, 150)

    # game variables


    run2 = True

    while run2:
        screen.fill((36, 36, 36))

        #check if the games is pasued:
        if game_paused == True:
            draw_text("Game pasued,  press O to continue ", font, violet, 150, 220)

            #display menu
        else:
            #draw_text("Press P to pause", font, txt_col, 230, 220)
            draw_text("EVIL PONG", font2, violet, 105, 20)
            draw_text("Start", font, violet, 270, 200)
            draw_text("Options", font, violet, 260, 240)
            draw_text("Scores", font, violet, 260, 280)
            draw_text("Exit", font, violet, 275, 320)



        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_paused = True

                    print("pause")
                elif event.key == pygame.K_o:
                    game_paused = False
                    run2 = False

                if event.key == pygame.K_ESCAPE:
                    run2 = False

            if event.type == pygame.QUIT:
                run2 = False

        pygame.display.update()
run2()
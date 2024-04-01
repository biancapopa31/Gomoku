import pygame
import game
import button
import sys
import constants as const

def displayModes():
    alg1Button = button.Button((const.SCREEN_WIDTH - const.BUTTON_WIDTH)//2, 
                           const.SCREEN_HEIGHT *3/10, const.BUTTON_WIDTH, const.BUTTON_HEIGHT, "Mini-max", screen, font)

    alg2Button = button.Button((const.SCREEN_WIDTH - const.BUTTON_WIDTH)//2, 
                            const.SCREEN_HEIGHT *4/10, const.BUTTON_WIDTH, const.BUTTON_HEIGHT, "Algoritm 2", screen, font)

    alg3Button = button.Button((const.SCREEN_WIDTH - const.BUTTON_WIDTH)//2, 
                           const.SCREEN_HEIGHT *5/10, const.BUTTON_WIDTH, const.BUTTON_HEIGHT, "Algoritm 3", screen, font)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if alg1Button.pressed(pygame.mouse.get_pos()):
                    return const.MINIMAX
                if alg2Button.pressed(pygame.mouse.get_pos()):
                    return 2
                if alg3Button.pressed(pygame.mouse.get_pos()):
                    return 3

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(const.BACKGROUND_COLOR)

        # RENDER YOUR GAME HERE
        alg1Button.draw()
        alg2Button.draw()
        alg3Button.draw()
        

        # flip() the display to put your work on screen
        pygame.display.flip()


def displayDifficulty():
    easyButton = button.Button((const.SCREEN_WIDTH - const.BUTTON_WIDTH)//2, 
                           const.SCREEN_HEIGHT *3/10, const.BUTTON_WIDTH, const.BUTTON_HEIGHT, "Easy", screen, font)

    mediumButton = button.Button((const.SCREEN_WIDTH - const.BUTTON_WIDTH)//2, 
                            const.SCREEN_HEIGHT *4/10, const.BUTTON_WIDTH, const.BUTTON_HEIGHT, "Medium", screen, font)

    hardButton = button.Button((const.SCREEN_WIDTH - const.BUTTON_WIDTH)//2, 
                           const.SCREEN_HEIGHT *5/10, const.BUTTON_WIDTH, const.BUTTON_HEIGHT, "Hard", screen, font)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easyButton.pressed(pygame.mouse.get_pos()):
                    return 1
                if mediumButton.pressed(pygame.mouse.get_pos()):
                    return 2
                if hardButton.pressed(pygame.mouse.get_pos()):
                    return 3

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(const.BACKGROUND_COLOR)

        # RENDER YOUR GAME HERE
        easyButton.draw()
        mediumButton.draw()
        hardButton.draw()
        

        # flip() the display to put your work on screen
        pygame.display.flip()

# pygame setup
pygame.init()

# screen setup
screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
pygame.display.set_caption("Go-Moku")
screen.fill(const.BACKGROUND_COLOR)
running = True

#font setup
font = pygame.font.SysFont(None, 30)

#title setup
title = font.render("Play Gomoku!", True, const.LINE_COLOR)
title_rect = title.get_rect(center=(const.SCREEN_WIDTH // 2, const.SCREEN_HEIGHT *1/10))

#alert setup
alert = font.render("", True, "red")
alert_rect = alert.get_rect(center=(const.SCREEN_WIDTH // 2, const.SCREEN_HEIGHT *7/10))

#buttons setup

modeButton = button.Button((const.SCREEN_WIDTH - const.BUTTON_WIDTH)//2, 
                           const.SCREEN_HEIGHT *3/10, const.BUTTON_WIDTH, const.BUTTON_HEIGHT, "Mode", screen, font)

difficultyButton = button.Button((const.SCREEN_WIDTH - const.BUTTON_WIDTH)//2, 
                           const.SCREEN_HEIGHT *4/10, const.BUTTON_WIDTH, const.BUTTON_HEIGHT, "Difficulty", screen, font)

playButton = button.Button((const.SCREEN_WIDTH - const.BUTTON_WIDTH)//2, 
                           const.SCREEN_HEIGHT *5/10, const.BUTTON_WIDTH, const.BUTTON_HEIGHT, "Play", screen, font)

exitButton = button.Button((const.SCREEN_WIDTH - const.BUTTON_WIDTH)//2, 
                           const.SCREEN_HEIGHT *6/10, const.BUTTON_WIDTH, const.BUTTON_HEIGHT, "Exit", screen, font)

alg = dif = -1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if exitButton.pressed(pygame.mouse.get_pos()):
                pygame.quit()
                sys.exit()
            if modeButton.pressed(pygame.mouse.get_pos()):
                alert = font.render("", True, "red")
                alg = displayModes()

            if difficultyButton.pressed(pygame.mouse.get_pos()):
                alert = font.render("", True, "red")
                dif = displayDifficulty()

            if playButton.pressed(pygame.mouse.get_pos()):
                if alg != -1 and dif != -1:
                    running = False
                else:
                    alert = font.render("Please select both mode and difficulty", True, "red")
                    alert_rect = alert.get_rect(center=(const.SCREEN_WIDTH // 2, const.SCREEN_HEIGHT *8/10))            
            

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(const.BACKGROUND_COLOR)

    # RENDER YOUR GAME HERE
    screen.blit(title, title_rect)
    modeButton.draw()
    difficultyButton.draw()
    playButton.draw()
    exitButton.draw()
    screen.blit(alert, alert_rect)
    

    # flip() the display to put your work on screen
    pygame.display.flip()

g = game.Game(alg, dif)


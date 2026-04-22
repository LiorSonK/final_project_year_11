import pygame

pygame.init()

screen = pygame.display.set_mode((640,  640))

running = True

while running:

    #close the game when the X button is pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

pygame.quit()
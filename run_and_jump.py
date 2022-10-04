import pygame
from sys import exit

pygame.init() #start pygame
#initiate screen
screen = pygame.display.set_mode((800,600)) #width,height
pygame.display.set_caption('run_and_jump_man')
clock = pygame.time.Clock() #helps with time and framerate

#test_surface = pygame.Surface((100,200)) #w,h
#test_surface.fill('Green')

background_surface = pygame.image.load('graphics/hills.jpg')
ground_surface = pygame.image.load('graphics/ground1.png')

while True:
    #event loop - checking for player inpute
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() #pygame.quit is stopping pygame.init - will show error
            exit() #finishes the code without error message
    #draw all elements
    #update everything
    screen.blit(background_surface,(0,-200)) #blit - block image transfer (surface,position in display surface)
    screen.blit(ground_surface,(0,-200))

    pygame.display.update() #it updates the display surface
    clock.tick(60) #while True loop should not run faster than 60 times per sec
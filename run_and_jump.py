import pygame
from sys import exit

pygame.init() #start pygame
#initiate screen
screen = pygame.display.set_mode((800,500)) #width,height
pygame.display.set_caption('run_and_jump_man')
clock = pygame.time.Clock() #helps with time and framerate
test_font = pygame.font.Font("fonts/DiabloHeavy.ttf", 50) #font type, font size

#test_surface = pygame.Surface((100,200)) #w,h
#test_surface.fill('Green')

background_surface = pygame.image.load('graphics/hills.jpg').convert_alpha() #.convert() - pygame can work with imported images more easely
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()
text_surface = test_font.render('szymobox', False, 'Purple') #txt, anty-alias, color

#animations
dino_surface = pygame.image.load("graphics/dino.png").convert_alpha()
dino_rect = dino_surface.get_rect(midbottom = (600,420))

player_surface = pygame.image.load('graphics/szom-right.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom = (200,420)) #takes surface and draws rectangle around it (topleft = (x,y))


while True:
    #event loop - checking for player inpute
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() #pygame.quit is stopping pygame.init - will show error
            exit() #finishes the code without error message
    #draw all elements
    #update everything
    #always draw proper background to previous surface
    screen.blit(background_surface,(0,-200)) #blit - block image transfer (surface,position in display surface)
    screen.blit(ground_surface,(-5,400))
    screen.blit(text_surface,(250,50))
    dino_rect.x -= 4
    if dino_rect.right <= 0: dino_rect.left = 800
    screen.blit(dino_surface, dino_rect)
    #print(player_rect.left) #prints exact position of left side of rectangle
    screen.blit(player_surface,player_rect)

    pygame.display.update() #it updates the display surface
    clock.tick(60) #while True loop should not run faster than 60 times per sec
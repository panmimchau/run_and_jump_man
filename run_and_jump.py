import pygame
from sys import exit

pygame.init() #start pygame
#initiate screen
screen = pygame.display.set_mode((800,500)) #width,height
pygame.display.set_caption('run_and_jump_man')
clock = pygame.time.Clock() #helps with time and framerate
test_font = pygame.font.Font("fonts/DiabloHeavy.ttf", 50) #font type, font size

#test_surf = pygame.surf((100,200)) #w,h
#test_surf.fill('Green')

background_surf = pygame.image.load('graphics/hills.jpg').convert_alpha() #.convert() - pygame can work with imported images more easely
ground_surf = pygame.image.load('graphics/ground.png').convert_alpha()

score_surf = test_font.render('szymobox', False, (64,64,64)) #txt, anty-alias, color
score_rect = score_surf.get_rect(center = (400, 50))

#animations
dino_surf = pygame.image.load("graphics/dino.png").convert_alpha()
dino_rect = dino_surf.get_rect(midbottom = (600,420))

player_surf = pygame.image.load('graphics/szom-right.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (200,420)) #takes surf and draws rectangle around it (topleft = (x,y))
player_gravity = 0


while True:
    #event loop - checking for player inpute
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() #pygame.quit is stopping pygame.init - will show error
            exit() #finishes the code without error message

        if event.type == pygame.MOUSEBUTTONDOWN:
            if player_rect.collidepoint(event.pos):
                player_gravity = -20

        #keyboard input on the event loop: 1.check if any button was pressed 2.work with specific button
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_gravity = -20


    #draw all elements
    #update everything
    #always draw proper background to previous surf
    screen.blit(background_surf,(0,-200)) #blit - block image transfer (surf,position in display surf)
    screen.blit(ground_surf,(-5,400))
    #drawing the score rectangle (surface to draw, color, what to draw)
    pygame.draw.rect(screen, "#c0e8ec", score_rect)
    pygame.draw.rect(screen, "#c0e8ec", score_rect, 10)
    screen.blit(score_surf,score_rect)
    dino_rect.x -= 4
    if dino_rect.right <= 0: dino_rect.left = 800
    screen.blit(dino_surf, dino_rect)

    #player
    #print(player_rect.left) #prints exact position of left side of rectangle
    player_gravity += 1
    player_rect.y += player_gravity
    screen.blit(player_surf,player_rect)

    #keyboard input
    #keys = pygame.key.get_pressed()
    #if keys[pygame.K_SPACE]:
    #    print("jump")

    #collisions rect1.colliderect(rect2) gives False or True
    #if player_rect.colliderect(dino_rect):
    #    print('flejter')

    # rect1.collidepoint((x,y)) - usefull when using mouse
    #mouse_pos = pygame.mouse.get_pos()
    #if player_rect.collidepoint(mouse_pos):
    #    print(pygame.mouse.get_pressed()) #print boolean value for every mouse button

    pygame.display.update() #it updates the display surf
    clock.tick(60) #while True loop should not run faster than 60 times per sec
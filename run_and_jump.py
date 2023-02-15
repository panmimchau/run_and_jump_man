import pygame
from sys import exit
from random import randint, choice

# classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  # initializing the Sprite class inside Player class
        player_walk_1 = pygame.image.load("graphics/szom-right1.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphics/szom-right2.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("sounds/jump.wav")
        self.jump_sound.set_volume(0.1)  # 0-1

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 420:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 420:
            self.rect.bottom = 420

    def animation_state(self):
        # TODO
        # if self.rect.bottom < 420:
        # self.image = self.player_jump
        # else:
        self.player_index += 0.1  # it takes a couple of frames to get to walk_2
        if self.player_index >= len(self.player_walk):
            self.player_index = 0
        self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == "tax":
            tax_1 = pygame.image.load("graphics/tax1.png").convert_alpha()
            tax_2 = pygame.image.load("graphics/tax2.png").convert_alpha()
            self.frames = [tax_1, tax_2]
            y_pos = 210
        else:
            dino_1 = pygame.image.load("graphics/dino1.png").convert_alpha()
            dino_2 = pygame.image.load("graphics/dino2.png").convert_alpha()
            self.frames = [dino_1, dino_2]
            y_pos = 420

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 5
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f"Score: {current_time}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time  # we can access the variable later in the code


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            # spawn dino/tax rects
            if obstacle_rect.bottom == 420:
                screen.blit(dino_surf, obstacle_rect)
            else:
                screen.blit(tax_surf, obstacle_rect)

        obstacle_list = [
            obstacle for obstacle in obstacle_list if obstacle.x > -100
        ]  # only copy existing item from list if x attribute is > -100 (if obstacle on screen)

        return obstacle_list
    else:
        return []


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 420:
        player_surf = player_walk_1
    else:
        player_index += 0.1  # it takes a couple of frames to get to walk_2
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]


pygame.init()  # start pygame
# initiate screen
screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption("szymo_jump")
clock = pygame.time.Clock()  # helps with time and framerate
test_font = pygame.font.Font("fonts/DiabloHeavy.ttf", 50)  # font type, font size
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound("sounds/main.wav")
bg_music.play(loops=-1)  # -1 - loops track forever

# groups
player = pygame.sprite.GroupSingle()  # needs to be in seperate group than obsticles
player.add(Player())

obstacle_group = pygame.sprite.Group()

background_surf = pygame.image.load(
    "graphics/hills.jpg"
).convert_alpha()  # .convert() - pygame can work with imported images more easely
ground_surf = pygame.image.load("graphics/ground.png").convert_alpha()

# score_surf = test_font.render('szymobox', False, (64,64,64)) #txt, anty-alias, color
# score_rect = score_surf.get_rect(center = (400, 50))

# obstancles

# dino
dino_frame_1 = pygame.image.load("graphics/dino1.png").convert_alpha()
dino_frame_2 = pygame.image.load("graphics/dino2.png").convert_alpha()
dino_frames = [dino_frame_1, dino_frame_2]
dino_frame_index = 0
dino_surf = dino_frames[dino_frame_index]

# tax
tax_frame_1 = pygame.image.load("graphics/tax1.png").convert_alpha()
tax_frame_2 = pygame.image.load("graphics/tax2.png").convert_alpha()
tax_frames = [tax_frame_1, tax_frame_2]
tax_frame_index = 0
tax_surf = tax_frames[tax_frame_index]

obstacle_rect_list = []

# player_surf = pygame.image.load('graphics/szom-right.png').convert_alpha()
player_walk_1 = pygame.image.load("graphics/szom-right1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/szom-right2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(
    midbottom=(200, 420)
)  # takes surf and draws rectangle around it (topleft = (x,y))
player_gravity = 0

# start screen
player_stand = pygame.image.load("graphics/szom-right1.png").convert_alpha()
player_stand = pygame.transform.rotozoom(
    player_stand, 0, 2
)  # scales the player graphic for intro
player_stand_rect = player_stand.get_rect(center=(400, 250))

game_name = test_font.render("szymojump", False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 100))

game_message = test_font.render("Press space to run", False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 360))

# timer
obstacle_timer = (
    pygame.USEREVENT + 1
)  # +1 - some events reserved for pygame, so we need to add 1
pygame.time.set_timer(obstacle_timer, 1000)  # obstacles will show up every 900ms

dino_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(dino_animation_timer, 500)

tax_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(tax_animation_timer, 200)

while True:
    # event loop - checking for player inpute
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # pygame.quit is stopping pygame.init - will show error
            exit()  # finishes the code without error message

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 420:
                    player_gravity = -20

            # keyboard input on the event loop: 1.check if any button was pressed 2.work with specific button
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 420:
                    player_gravity = -23

        else:
            if (
                event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
            ):  # reseting game after collision
                game_active = True
                # dino_rect.left = 800
                start_time = int(pygame.time.get_ticks() / 1000)

        if game_active:
            if event.type == obstacle_timer and game_active:
                obstacle_group.add(
                    Obstacle(choice(["tax", "dino", "dino"]))
                )  # will pick one of items from list; 75% te pick dino
                # if randint(0,2):
                #    obstacle_rect_list.append(dino_surf.get_rect(midbottom = (randint(900,1100),420))) #position of obstacles
                # else:
                #    obstacle_rect_list.append(tax_surf.get_rect(midbottom = (randint(900,1100),210)))

            if event.type == dino_animation_timer:  # animation timer for dino
                if dino_frame_index == 0:
                    dino_frame_index = 1
                else:
                    dino_frame_index = 0
                dino_surf = dino_frames[dino_frame_index]

            if event.type == tax_animation_timer:  # animation timer for tax
                if tax_frame_index == 0:
                    tax_frame_index = 1
                else:
                    tax_frame_index = 0
                tax_surf = tax_frames[tax_frame_index]

    # draw all elements
    # update everything
    if game_active:
        # always draw proper background to previous surf
        screen.blit(
            background_surf, (0, -200)
        )  # blit - block image transfer (surf,position in display surf)
        screen.blit(ground_surf, (-5, 400))
        # drawing the score rectangle (surface to draw, color, what to draw)
        # pygame.draw.rect(screen, "#c0e8ec", score_rect)
        # pygame.draw.rect(screen, "#c0e8ec", score_rect, 10)
        # screen.blit(score_surf,score_rect)
        score = display_score()  # we can access the score at any time

        # dino_rect.x -= 4
        # if dino_rect.right <= 0: dino_rect.left = 800
        # screen.blit(dino_surf, dino_rect)

        # player
        # print(player_rect.left) #prints exact position of left side of rectangle
        # player_gravity += 1
        # player_rect.y += player_gravity
        # if player_rect.bottom >= 420: player_rect.bottom = 420 #"creates" a ground for player to stand on
        # player_animation()
        # screen.blit(player_surf,player_rect)
        # sprite groups have 2  functions
        player.draw(screen)  # draw sprites
        player.update()  # update sprites

        obstacle_group.draw(screen)
        obstacle_group.update()

        # obstancle movement
        # obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        # obstacle_group.update()

        # keyboard input
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
        #    print("jump")

        # collisions
        game_active = collision_sprite()
        # if dino_rect.colliderect(player_rect):
        #   game_active = False
        # game_active = collisions(player_rect,obstacle_rect_list) #returns True or False

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()  # removing items form obstacle_rect_list after game over
        player_rect.midbottom = (80, 420)  # players alwyas starts at the bottom
        player_gravity = 0

        score_message = test_font.render(f"your score: {score}", False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 360))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)
    # collisions rect1.colliderect(rect2) gives False or True
    # if player_rect.colliderect(dino_rect):
    #    print('flejter')

    # rect1.collidepoint((x,y)) - usefull when using mouse
    # mouse_pos = pygame.mouse.get_pos()
    # if player_rect.collidepoint(mouse_pos):
    #    print(pygame.mouse.get_pressed()) #print boolean value for every mouse button

    pygame.display.update()  # it updates the display surf
    clock.tick(60)  # while True loop should not run faster than 60 times per sec

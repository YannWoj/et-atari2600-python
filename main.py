# E.T. THE EXTRA-TERRESTRIAL (Python Remake)
# Original game        : Copyright 1982 Atari, Inc. (Atari 2600)
# Designer             : Howard Scott Warshaw
# Artist               : Jerome Domurat
# Python Remake Author : Yann W.
# This is an unofficial remake created for educational and non-commercial purposes.

# main.py
import pygame
from graphics import draw_background, draw_center_area, LIGHT_BLUE2_HEIGHT
from player import ET

# constants
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 566
FPS = 60

# init
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("E.T. the Extra-Terrestrial (Atari 2600 Remake)")
clock = pygame.time.Clock()

# images
# title screen images
et_head_title_image = pygame.image.load("assets/images/title/et_head_title.png")
et_title_image = pygame.image.load("assets/images/title/et_title.png")
copyright_title_image = pygame.image.load("assets/images/title/copyright_atari.png")

# game screen images
forest1_image = pygame.image.load("assets/images/forest/forest1.png")
pit_image = pygame.image.load("assets/images/pit/pit.png")

# music
pygame.mixer.init()
music_playing = False
pygame.mixer.music.load("assets/music/title_music.wav")
pygame.mixer.music.play(-1)  # -1 = infinite loop

# sound effects
# E.T.
et_walk = pygame.mixer.Sound("assets/sounds/E.T/walk.wav")
et_run = pygame.mixer.Sound("assets/sounds/E.T/run.wav")
et_head_raise = pygame.mixer.Sound("assets/sounds/E.T/head_raise.wav")
et_head_raise.set_volume(0.75)
et_fall = pygame.mixer.Sound("assets/sounds/E.T/fall.wav")

# game states (TITLE/FOREST1/FOREST2/FOREST3/FOREST4/FOREST5/FOREST6/BUILDING/PIT/HOUSE):
game_state = "TITLE" # initial game state (start with title screen)

# get E.T. centered
et = ET((SCREEN_WIDTH - 48) // 2, (SCREEN_HEIGHT - 48) // 2, et_walk, et_run, et_head_raise)

# main loop
running = True
while running:
    # track single space key presses
    space_pressed_once = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                space_pressed_once = True

    # get pressed keys
    keys = pygame.key.get_pressed()

    # handle different game screens
    if game_state == "TITLE":
        # show title screen with E.T. logo
        draw_background(screen, SCREEN_WIDTH, SCREEN_HEIGHT, game_state)
        draw_center_area(screen, SCREEN_WIDTH, "TITLE")

        # get center area dimensions for positioning
        center_x, center_y, center_width, center_height = draw_center_area(screen, SCREEN_WIDTH, "TITLE")

        # draw E.T. title logo
        et_title_rect = et_title_image.get_rect(midtop=(
            center_x + center_width // 2 - 15,
            center_y + 53
        ))
        screen.blit(et_title_image, et_title_rect)

        # draw E.T. head image
        et_head_title_rect = et_head_title_image.get_rect(midbottom=(
            center_x + center_width // 2 - 4,
            center_y + center_height - 63
        ))
        screen.blit(et_head_title_image, et_head_title_rect)

        # draw copyright notice in bottom bar
        copyright_rect = copyright_title_image.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT - LIGHT_BLUE2_HEIGHT // 2 
            )
        )
        screen.blit(copyright_title_image, copyright_rect)

        # start music when entering title screen
        if not music_playing:
            pygame.mixer.music.load("assets/music/title_music.wav")
            pygame.mixer.music.play(-1)
            music_playing = True

        # start game when space is pressed
        if keys[pygame.K_SPACE]:
            game_state = "FOREST1"
            pygame.mixer.music.stop()
            music_playing = False

    # forest1 screen:
    elif game_state == "FOREST1":
        draw_background(screen, SCREEN_WIDTH, SCREEN_HEIGHT, game_state)
        center_x, center_y, center_width, center_height = draw_center_area(screen, SCREEN_WIDTH, "FOREST1")
        screen.blit(forest1_image, (center_x, center_y))
        et.handle_input(keys, space_pressed_once)
        
        # check if E.T. walks off right edge to fall into pit
        if et.x > center_x + center_width - et.image.get_width():
            # position E.T. at top center of pit
            et.x = center_x + (center_width - et.image.get_width()) // 2
            et.y = center_y
            et_fall.play()

            # reset position and start falling animation
            et.x = center_x + (center_width - et.image.get_width()) // 2
            et.y = center_y
            et.is_falling_into_pit = True
            et.pit_target_y = center_y + 360 - et.image.get_height()

            # set pit boundaries
            et.pit_escape_y = center_y  # top edge for escaping
            et.pit_bottom_y = center_y + 360  # bottom platform
            et.rising_out_of_pit = False

            # switch to pit screen
            game_state = "PIT"
            
            # set horizontal movement limits inside pit
            et.pit_left_limit = center_x + 192
            et.pit_right_limit = center_x + center_width - 192 - et.image.get_width()
        else:
            et.draw(screen)

    # forest2 screen:
    elif game_state == "FOREST2":
        draw_background(screen, SCREEN_WIDTH, SCREEN_HEIGHT, game_state)
        draw_center_area(screen, SCREEN_WIDTH, "FOREST2")
        et.handle_input(keys, space_pressed_once)
        et.draw(screen)

    # forest3 screen:
    elif game_state == "FOREST3":
        draw_background(screen, SCREEN_WIDTH, SCREEN_HEIGHT, game_state)
        draw_center_area(screen, SCREEN_WIDTH, "FOREST3")
        et.handle_input(keys, space_pressed_once)
        et.draw(screen)

    # forest4 screen:
    elif game_state == "FOREST4":
        draw_background(screen, SCREEN_WIDTH, SCREEN_HEIGHT, game_state)
        draw_center_area(screen, SCREEN_WIDTH, "FOREST4")
        et.handle_input(keys, space_pressed_once)
        et.draw(screen)

    # forest5 screen:
    elif game_state == "FOREST5":
        draw_background(screen, SCREEN_WIDTH, SCREEN_HEIGHT, game_state)
        draw_center_area(screen, SCREEN_WIDTH, "FOREST5")
        et.handle_input(keys, space_pressed_once)
        et.draw(screen)

    # building screen:
    elif game_state == "BUILDING":
        draw_background(screen, SCREEN_WIDTH, SCREEN_HEIGHT, game_state)
        draw_center_area(screen, SCREEN_WIDTH, "BUILDING")
        et.handle_input(keys, space_pressed_once)
        et.draw(screen)

    # pit screen  - E.T. can levitate to escape:
    elif game_state == "PIT":
        draw_background(screen, SCREEN_WIDTH, SCREEN_HEIGHT, "TITLE")  # TITLE to get black borders
        center_x, center_y, center_width, center_height = draw_center_area(screen, SCREEN_WIDTH, "PIT")
        screen.blit(pit_image, (center_x, center_y))
        result = et.handle_input(keys, space_pressed_once)
        if result == "ESCAPE_PIT":
            game_state = "FOREST2"
            et.in_pit = False
            et.rising_out_of_pit = False
        et.draw(screen)

    # house screen:
    elif game_state == "HOUSE":
        draw_background(screen, SCREEN_WIDTH, SCREEN_HEIGHT, game_state)
        draw_center_area(screen, SCREEN_WIDTH, "HOUSE")
        et.handle_input(keys, space_pressed_once)
        et.draw(screen)

    # update display and maintain framerate
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
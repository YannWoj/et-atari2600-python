# E.T. THE EXTRA-TERRESTRIAL (Python Remake)
# Original game        : Copyright 1982 Atari, Inc. (Atari 2600)
# Designer             : Howard Scott Warshaw
# Artist               : Jerome Domurat
# Python Remake Author : Yann Wojciechowski
# This is an unofficial remake created for educational and non-commercial purposes.

import pygame
from graphics import draw_background, draw_center_area
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

# game states:
# TITLE   : screen with ET's head (first screen)
# FOREST1 :
# FOREST2 :
# FOREST3 :
# FOREST4 :
# FOREST5 :
# BUILDING: screen with white columns and a house
# PIT     : screen with pit
# HOUSE   : screen with house on dark blue background (last screen)
game_state = "TITLE" # initial game state (start with title screen)

# music
pygame.mixer.init()
music_playing = False
pygame.mixer.music.load("assets/music/title_music.wav")
pygame.mixer.music.play(-1)  # -1 = infinite loop

# get E.t centered
et = ET((SCREEN_WIDTH - 48) // 2, (SCREEN_HEIGHT - 48) // 2)

# main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # get pressed keys
    keys = pygame.key.get_pressed()

    # handle game states and draw the correct screen content
    if game_state == "TITLE":
        # title screen: draw E.t logo and wait for space key to start the game
        draw_background(screen, SCREEN_WIDTH, SCREEN_HEIGHT, game_state)
        draw_center_area(screen, SCREEN_WIDTH, "TITLE")

        # play music only once when entering the title screen
        if not music_playing:
            pygame.mixer.music.load("assets/music/title_music.wav")
            pygame.mixer.music.play(-1)
            music_playing = True

        # switch to the forest screen when space is pressed and stop title music
        if keys[pygame.K_SPACE]:
            game_state = "FOREST1"
            pygame.mixer.music.stop()
            music_playing = False

    # forest1 screen:
    elif game_state == "FOREST1":
        draw_background(screen, SCREEN_WIDTH, SCREEN_HEIGHT, game_state)
        draw_center_area(screen, SCREEN_WIDTH, "FOREST1")
        et.handle_input(keys)
        et.draw(screen)

    # forest2 screen:
    elif game_state == "FOREST2":
        draw_background(screen, SCREEN_WIDTH, SCREEN_HEIGHT, game_state)
        draw_center_area(screen, SCREEN_WIDTH, "FOREST2")
        et.handle_input(keys)
        et.draw(screen)

    # forest3 screen:
    elif game_state == "FOREST3":
        draw_background(screen, SCREEN_WIDTH, SCREEN_HEIGHT, game_state)
        draw_center_area(screen, SCREEN_WIDTH, "FOREST3")
        et.handle_input(keys)
        et.draw(screen)

    # forest4 screen:
    elif game_state == "FOREST4":
        draw_background(screen, SCREEN_WIDTH, SCREEN_HEIGHT, game_state)
        draw_center_area(screen, SCREEN_WIDTH, "FOREST4")
        et.handle_input(keys)
        et.draw(screen)

    # forest5 screen:
    elif game_state == "FOREST5":
        draw_background(screen, SCREEN_WIDTH, SCREEN_HEIGHT, game_state)
        draw_center_area(screen, SCREEN_WIDTH, "FOREST5")
        et.handle_input(keys)
        et.draw(screen)

    # building screen:
    elif game_state == "BUILDING":
        draw_background(screen, SCREEN_WIDTH, SCREEN_HEIGHT, game_state)
        draw_center_area(screen, SCREEN_WIDTH, "BUILDING")
        et.handle_input(keys)
        et.draw(screen)

    # pit screen:
    elif game_state == "PIT":
        draw_background(screen, SCREEN_WIDTH, SCREEN_HEIGHT, game_state)
        draw_center_area(screen, SCREEN_WIDTH, "PIT")
        et.handle_input(keys)
        et.draw(screen)

    # house screen:
    elif game_state == "HOUSE":
        draw_background(screen, SCREEN_WIDTH, SCREEN_HEIGHT, game_state)
        draw_center_area(screen, SCREEN_WIDTH, "HOUSE")
        et.handle_input(keys)
        et.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
# E.T. THE EXTRA-TERRESTRIAL (Python Remake)
# Original game        ; Copyright 1982 Atari, Inc. (Atari 2600)
# Designer             ; Howard Scott Warshaw
# Artist               ; Jerome Domurat
# Python Remake Author ; Yann W.
# This is an unofficial remake created for educational and non-commercial purposes.

# main.py
import pygame
from graphics import draw_background, draw_center_area, LIGHT_BLUE2_HEIGHT
from player import ET
from spaceship import Spaceship
from counter import Counter
from game_state_manager import GameStateManager
from level_manager import LevelManager
from audio_manager import AudioManager

# constants
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 566
FPS = 60

# init
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("E.T. the Extra-Terrestrial (Atari 2600 Remake)")
clock = pygame.time.Clock()

# initialize managers
game_state_manager = GameStateManager(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
level_manager = LevelManager()
audio_manager = AudioManager()

# load instances
et = ET((SCREEN_WIDTH - 48) // 2, (SCREEN_HEIGHT - 48) // 2, 
        audio_manager.get_sound("et_walk"), 
        audio_manager.get_sound("et_run"), 
        audio_manager.get_sound("et_head_raise"))
spaceship = Spaceship((SCREEN_WIDTH - 96) // 2, 100)
counter = Counter()

# main loop
running = True
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

    # get current game state
    current_state = game_state_manager.get_current_state()

    # handle different game screens
    if current_state == "TITLE":
        # deactivate counter on title screen
        counter.deactivate()
        
        # render title screen
        game_state_manager.render_title_screen()

        # start music when entering title screen
        if not audio_manager.is_music_playing():
            audio_manager.play_music("title")

        # start game when space is pressed
        if keys[pygame.K_SPACE]:
            game_state_manager.change_state("FOREST1")
            level_manager.set_level("FOREST1")
            audio_manager.stop_music()

            # reset and activate counter for new game
            counter.reset()
            counter.activate()
            game_state_manager.set_game_over(False)

            # play spaceship sound
            audio_manager.play_sound("spaceship")
            
            # initialize the intro sequence with the spaceship
            game_state_manager.set_intro_active(True)
            center_x, center_y, center_width, center_height = draw_center_area(screen, SCREEN_WIDTH, "FOREST1")
            spaceship.reset_for_new_game(center_x + (center_width - 96) // 2, center_y)
            
            # initial position of e.t. in the ship
            et_x, et_y = spaceship.get_et_position()
            et.x = et_x
            et.y = et_y

    else:  # game states (forest1, forest2, etc.)
        # render the current game screen
        center_x, center_y, center_width, center_height = game_state_manager.render_game_screen(current_state, et, spaceship)
        
        # forest1 screen - handle intro sequence
        if current_state == "FOREST1" and game_state_manager.is_intro_active():
            # manage spaceship intro sequence
            spaceship.update(center_y)
            
            # if e.t. is still in spaceship
            if spaceship.is_et_in_spaceship():
                # e.t. follows spaceship
                et_x, et_y = spaceship.get_et_position()
                et.x = et_x
                et.y = et_y
                
                # e.t. can only look right/left during descent
                if keys[pygame.K_RIGHT]:
                    et.image = pygame.transform.flip(et.images["idle"], True, False)
                else:
                    et.image = et.images["idle"]  # look left by default
                    
            else:
                # e.t. has been dropped, wait for spaceship to disappear
                if not spaceship.is_visible():
                    game_state_manager.set_intro_active(False)
                    # e.t. becomes controllable only when the ship has completely disappeared
                    et.set_controllable(True)
                
                # e.t. can now be controlled normally
                if not game_state_manager.is_game_over():
                    result = et.handle_input(keys, space_pressed_once)
                    # handle counter decrements
                    if result == "STEP":
                        game_over = counter.decrement_step()
                        game_state_manager.set_game_over(game_over)
                    elif result == "HEAD_RAISE":
                        game_over = counter.decrement_head_raise()
                        game_state_manager.set_game_over(game_over)
                    elif result == "FALL_COMPLETE":
                        game_over = counter.decrement_fall()
                        game_state_manager.set_game_over(game_over)
            
            # draw spaceship
            spaceship.draw(screen)
            
        # pit screen - e.t. can levitate to escape
        elif current_state == "PIT":
            if not game_state_manager.is_game_over():
                result = et.handle_input(keys, space_pressed_once)
                # handle counter decrements
                if result == "STEP":
                    game_over = counter.decrement_step()
                    game_state_manager.set_game_over(game_over)
                elif result == "HEAD_RAISE":
                    game_over = counter.decrement_head_raise()
                    game_state_manager.set_game_over(game_over)
                elif result == "FALL_COMPLETE":
                    game_over = counter.decrement_fall()
                    game_state_manager.set_game_over(game_over)
                elif result == "ESCAPE_PIT":
                    # return to the level specified in level manager
                    escape_level = level_manager.get_next_level("escape")
                    if escape_level:
                        game_state_manager.change_state(escape_level)
                        level_manager.set_level(escape_level)
                        et.in_pit = False
                        et.rising_out_of_pit = False
                        # position e.t. at center of new level
                        et.x = center_x + (center_width - et.image.get_width()) // 2
                        et.y = center_y + (center_height - et.image.get_height()) // 2

        # handle all other game states (forest1 normal gameplay, forest2, forest3, forest4, forest5, building, house)
        else:
            if not game_state_manager.is_game_over():
                result = et.handle_input(keys, space_pressed_once)
                
                # handle counter decrements
                if result == "STEP":
                    game_over = counter.decrement_step()
                    game_state_manager.set_game_over(game_over)
                elif result == "HEAD_RAISE":
                    game_over = counter.decrement_head_raise()
                    game_state_manager.set_game_over(game_over)
                elif result == "FALL_COMPLETE":
                    game_over = counter.decrement_fall()
                    game_state_manager.set_game_over(game_over)

                # check if ET stepped on a pit
                if level_manager.has_pit_at_position(
                    et.x - center_x, et.y - center_y,
                    et.image.get_width(), et.image.get_height()
                ):
                    game_state_manager.change_state("PIT", et=et)
                    level_manager.set_level("PIT")
                    et.setup_pit_fall(center_x, center_y, center_width, center_height)
                    audio_manager.play_sound("et_fall")

                # general level transition system for other levels
                transition = level_manager.check_level_boundaries(
                    et.x, et.y, et.image.get_width(), et.image.get_height(),
                    center_x, center_y, center_width, center_height
                )
                    
                if transition:
                    if level_manager.change_level(transition):
                        new_level = level_manager.get_current_level()
                        game_state_manager.change_state(new_level)
                            
                        # position e.t. according to the direction he came from
                        opposite_direction = {
                            "right": "right", "left": "left", 
                            "up": "up", "down": "down"
                        }
                        spawn_direction = opposite_direction.get(transition, "center")
                        spawn_x, spawn_y = level_manager.get_spawn_position(
                            spawn_direction, center_x, center_y, center_width, center_height,
                            et.image.get_width(), et.image.get_height()
                        )
                        et.reset_for_level_transition(spawn_x, spawn_y)
        
        # always draw e.t.
        et.draw(screen, spaceship if (current_state == "FOREST1" and game_state_manager.is_intro_active()) else None)

    # draw counter (only appears in game screens, not title)
    counter.draw(screen, SCREEN_WIDTH, SCREEN_HEIGHT, LIGHT_BLUE2_HEIGHT)

    # handle game over
    if game_state_manager.is_game_over():
        # stop e.t. sounds
        audio_manager.stop_sound("et_walk")
        audio_manager.stop_sound("et_run")

    # update display and maintain framerate
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
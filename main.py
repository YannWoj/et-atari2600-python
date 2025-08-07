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
et.set_levitation_sound(audio_manager.get_sound("et_head_raise_levitating"))

spaceship = Spaceship((SCREEN_WIDTH - 96) // 2, 100)
counter = Counter()

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
                    escape_level = level_manager.get_pit_escape_level()
                    if escape_level:
                        game_state_manager.change_state(escape_level)
                        level_manager.set_level(escape_level)
                        et.in_pit = False
                        et.rising_out_of_pit = False
                        # position e.t. centered on the pit he fell from
                        center_x, center_y, center_width, center_height = draw_center_area(screen, SCREEN_WIDTH, escape_level)
                        pit_center_x, pit_center_y = level_manager.get_pit_center_position(center_x, center_y, et.image.get_width(), et.image.get_height())
                        et.x = pit_center_x
                        et.y = pit_center_y
                        # start escaped pit moving state
                        et.start_finish_head_raise()

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

                # check if ET escaped from pit collision and can finish head raise animation
                if et.escaped_pit_moving:
                    # get ET's current dimensions (height changes during animation)
                    et_rect_x = et.x - center_x
                    et_rect_y = et.y - center_y
                    et_width = et.image.get_width()
                    et_height = et.image.get_height()
                    
                    # check if ET's actual hitbox is completely clear of pit collision
                    # separate margins for each direction - adjust these values to fine-tune pit escape
                    margin_left = 0    # increase to need more clearance on left side
                    margin_right = 0   # increase to need more clearance on right side  
                    margin_top = 1     # increase to need more clearance above et
                    margin_bottom = 16 # increase to need more clearance below et (compensates for height changes)
                    
                    # detect which direction ET escaped from pit
                    escaped_upward = et.y < center_y + 180  
                    escaped_downward = et.y > center_y + 180
                    if level_manager.current_pit_bounds:
                        pit_x, pit_y, pit_width, pit_height = level_manager.current_pit_bounds
                        escaped_upward = (et_rect_y + et_height) <= pit_y + 1
                        escaped_downward = et_rect_y > (pit_y + pit_height)

                    if escaped_upward:
                        # for upward escape, we test from et's head
                        test_y = et_rect_y + et_height  
                        test_height = 1
                    elif escaped_downward:
                        # escaped by going down - test ET's head clearance  
                        test_y = et_rect_y
                        test_height = margin_bottom
                    else:
                        # escaped sideways - test full hitbox
                        test_y = et_rect_y - margin_top
                        test_height = et_height + margin_top + margin_bottom

                    expanded_hitbox = (
                        et_rect_x - margin_left,
                        test_y,
                        et_width + margin_left + margin_right,
                        test_height
                    )

                    # direct test instead of using has_pit_at_position
                    pit_collision = False
                    if level_manager.current_pit_bounds:
                        pit_x, pit_y, pit_width, pit_height = level_manager.current_pit_bounds
                        # test if expanded_hitbox overlaps with the pit
                        if (expanded_hitbox[0] < pit_x + pit_width and 
                            expanded_hitbox[0] + expanded_hitbox[2] > pit_x and 
                            expanded_hitbox[1] < pit_y + pit_height and 
                            expanded_hitbox[1] + expanded_hitbox[3] > pit_y):
                            pit_collision = True

                    all_clear = not pit_collision

                    print(f"expanded_hitbox: {expanded_hitbox}")
                    print(f"pit_collision: {pit_collision}")
                    
                    if all_clear:
                        # debug info to see exactly where et stops
                        print(f"=== ET ESCAPE DEBUG ===")
                        print(f"ET position: x={et.x}, y={et.y}")
                        print(f"ET relative to center: x={et.x - center_x}, y={et.y - center_y}")
                        print(f"ET image size: {et.image.get_width()}x{et.image.get_height()}")
                        print(f"ET bottom Y: {et.y + et.image.get_height()}")
                        print(f"ET bottom Y relative: {(et.y + et.image.get_height()) - center_y}")
                        print(f"Escaped upward: {escaped_upward}")
                        print(f"Current pit bounds: {level_manager.current_pit_bounds}")
                        if level_manager.current_pit_bounds:
                            pit_x, pit_y, pit_w, pit_h = level_manager.current_pit_bounds
                            print(f"Pit top Y: {pit_y}")
                            print(f"Distance between ET bottom and pit top: {((et.y + et.image.get_height()) - center_y) - pit_y}")
                        print("=======================")
                        # ET is completely clear of pit collision
                        et.escaped_pit_moving = False
                        et.finishing_head_raise = True
                        et.finish_frame = 4
                        et.finish_counter = 0
                        # stop levitation sound
                        et.levitation_sound_timer = 0
                
                else:
                    # check if ET stepped on a pit (only when NOT in escaped_pit_moving mode)
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
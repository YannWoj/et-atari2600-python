# player.py
import pygame

class ET:
    def __init__(self, x, y, walk_sound, run_sound, head_raise_sound):
        # load all sprite images for E.T.'s animations
        self.images = {
            # idle
            "idle": pygame.image.load("assets/images/e.t/idle/et_idle.png"),
            # walk
            "walk": [
                pygame.image.load("assets/images/e.t/walking/et_walking_0.png"),
                pygame.image.load("assets/images/e.t/walking/et_walking_1.png"),
                pygame.image.load("assets/images/e.t/walking/et_walking_2.png")
            ],
            # head raise
            "head_raise": [
                pygame.image.load("assets/images/e.t/head_raising/et_head_raise_0.png"),
                pygame.image.load("assets/images/e.t/head_raising/et_head_raise_1.png"),
                pygame.image.load("assets/images/e.t/head_raising/et_head_raise_2.png"),
                pygame.image.load("assets/images/e.t/head_raising/et_head_raise_3.png"),
                pygame.image.load("assets/images/e.t/head_raising/et_head_raise_4.png"),
                pygame.image.load("assets/images/e.t/head_raising/et_head_raise_5.png"),
                pygame.image.load("assets/images/e.t/head_raising/et_head_raise_6.png")
            ]
        }
        # initial position on screen
        self.x = x
        self.y = y
        
        # movement speeds - normal and boosted (when running)
        self.speed = 1.5
        self.boost_speed = 5.2
        
        # walking animation control
        self.walk_frame = 0
        self.walk_counter = 0
        self.walk_anim_speed = 3
        self.image = self.images["idle"]

        # sound effects
        self.walk_sound = walk_sound
        self.run_sound = run_sound

        # movement state
        self.moving = False
        self.is_running = False

        # visibility and playability control during the intro
        self.is_controllable = False  # e.t. is not playable until the spaceship has disappeared.

        # head raising (used for levitation)
        self.head_raise_active = False
        self.head_raise_frame = 0
        self.head_raise_counter = 0
        self.head_raise_sound = head_raise_sound
        self.head_raise_speed = 5 # animation speed
        self.head_raise_just_started = False  # track when head raise starts

        # pit falling
        self.is_falling_into_pit = False
        self.pit_target_y = 0
        self.pit_fall_speed = 6.65
        self.in_pit = False
        self.pit_left_limit = 0
        self.pit_right_limit = 0
        self.pit_bottom_y = 0

        # pit escaping
        self.rising_out_of_pit = False
        self.pit_escape_y = 0  # y limit to escape pit
        self.head_locked_image = self.images["head_raise"][3]  # frame used while rising
        self.ready_to_levitate = False  # becomes true when head_raise_3 is reached
        self.levitation_speed = 2 # control how fast e.t. goes up/down during levitation
        self.finishing_head_raise = False
        self.finish_frame = 4
        self.finish_counter = 0
        self.escaped_pit_moving = False  # new state: out of pit but still in head_raise_3, needs to move away from pit collision


        # levitation sound management
        self.levitation_sound_timer = 0
        self.levitation_sound_delay = 70  # 1 seconds at 60 fps
        self.levitation_sound = None  # will be set later

        # step tracking for counter
        self.previous_x = x
        self.previous_y = y
        self.step_threshold = 1.0  # minimum distance to count as a step

    def set_controllable(self, controllable):
        # defines whether e.t. can be controlled by the player
        self.is_controllable = controllable

    def set_levitation_sound(self, levitation_sound):
        """set the levitation sound"""
        self.levitation_sound = levitation_sound

    def start_finish_head_raise(self):
        """start the escaped pit moving state (stay in frame 3 until out of pit collision)"""
        self.escaped_pit_moving = True
        self.image = self.head_locked_image  # stay in head_raise_3

    def handle_input(self, keys, space_pressed_once):

        result = None  # return value to indicate what action occurred

        # if e.t. is not yet controllable, ignore all inputs
        if not self.is_controllable:
            # block all inputs when finishing head raise animation
            if self.finishing_head_raise:
                return result
            # allow only visual direction change during descent
            if keys[pygame.K_RIGHT]:
                self.image = pygame.transform.flip(self.images["idle"], True, False)
            else:
                self.image = self.images["idle"]  # look left by default
            return

        # block all movement when finishing head raise animation after pit escape
        if self.finishing_head_raise:
            self.walk_sound.stop()
            self.run_sound.stop() 
            self.moving = False
            
            self.finish_counter += 1
            if self.finish_counter >= self.head_raise_speed:
                self.finish_counter = 0
                if self.finish_frame <= 6:
                    self.image = self.images["head_raise"][self.finish_frame]
                    self.finish_frame += 1
                else:
                    self.image = self.images["idle"]
                    self.finishing_head_raise = False
            else:
                if self.finish_frame <= 6:
                    self.image = self.images["head_raise"][self.finish_frame]
                else:
                    self.image = self.images["idle"]
            return result

        # block all movement when head raise animation is playing (except in pit)
        if self.head_raise_active and not self.in_pit and not self.is_falling_into_pit:
            # check if head raise just started
            if self.head_raise_just_started:
                self.head_raise_just_started = False
                result = "HEAD_RAISE"

            # animate head raise frames with timing control
            self.head_raise_counter += 1
            if self.head_raise_counter >= self.head_raise_speed:
                self.head_raise_counter = 0
                self.head_raise_frame += 1
                
                # check if animation is complete
                if self.head_raise_frame >= len(self.images["head_raise"]):
                    self.head_raise_active = False
                    self.head_raise_frame = 0
                    self.image = self.images["idle"]
                else:
                    self.image = self.images["head_raise"][self.head_raise_frame]
            else:
                self.image = self.images["head_raise"][self.head_raise_frame]
            return result

        # handle falling into pit animation
        if self.is_falling_into_pit:
            self.walk_sound.stop()
            self.run_sound.stop()
            self.moving = False
            
            # enable head_raise during fall
            if space_pressed_once and not self.head_raise_active:
                self.head_raise_active = True
                self.head_raise_frame = 0
                self.head_raise_counter = 0
                self.head_raise_sound.play()
                return "HEAD_RAISE"
            
            # handle head_raise animation during fall
            if self.head_raise_active:
                self.head_raise_counter += 1
                if self.head_raise_counter >= self.head_raise_speed:
                    self.head_raise_counter = 0
                    self.head_raise_frame += 1
                    
                    # when we reach frame 3, then we stop the fall
                    if self.head_raise_frame == 3:
                        self.is_falling_into_pit = False
                        self.in_pit = True
                        self.rising_out_of_pit = True
                        self.head_raise_active = False
                        self.y -= 9 # # small visual jump when starting levitation
                        return result
                
                self.image = self.images["head_raise"][self.head_raise_frame]
                # keep falling during animation
                self.y += self.pit_fall_speed
            else:
                # normal fall
                self.image = self.images["idle"]
                self.y += self.pit_fall_speed

            # check if e.t. has reached the bottom of the pit
            if self.y >= self.pit_target_y:
                self.y = self.pit_target_y
                self.is_falling_into_pit = False
                self.in_pit = True
                result = "FALL_COMPLETE"

            # flip image to right only if right key is held
            if keys[pygame.K_RIGHT]:
                self.image = pygame.transform.flip(self.image, True, False)
            else:
                self.image = pygame.transform.flip(self.image, False, False)
            return result

        # handle levitation when trying to escape from pit
        if self.in_pit and self.rising_out_of_pit:
            self.image = self.head_locked_image  # always show head_raise_3

            # play levitation sound with delay
            self.levitation_sound_timer += 1
            if self.levitation_sound_timer >= self.levitation_sound_delay:
                self.levitation_sound_timer = 0
                if self.levitation_sound:
                    self.levitation_sound.play()

            # store position before levitation movement
            levitation_old_y = self.y

            # move up when up key is pressed (levitation)
            if keys[pygame.K_UP]:
                self.y -= self.levitation_speed
            # move down when down key is pressed (levitation)
            if keys[pygame.K_DOWN]:
                self.y += self.levitation_speed

            # check if levitation movement counts as a step
            distance_moved_levitation = abs(self.y - levitation_old_y)
            if distance_moved_levitation >= self.step_threshold - 0.5:
                result = "STEP"
            
            # flip image to right temporarily
            if keys[pygame.K_RIGHT]:
                self.image = pygame.transform.flip(self.head_locked_image, True, False)
            else:
                self.image = pygame.transform.flip(self.head_locked_image, False, False)

            # check if et reached the top of the pit (escaped the pit?)
            et_top_y = self.y - (self.image.get_height() - self.images["idle"].get_height())
            if et_top_y <= self.pit_escape_y:
                self.rising_out_of_pit = False
                self.image = self.images["idle"]
                return "ESCAPE_PIT"

            # check if et reached the bottom platform of the pit
            et_bottom_y = self.y + self.images["idle"].get_height()
            if et_bottom_y >= self.pit_bottom_y:
                self.rising_out_of_pit = False
                self.finishing_head_raise = True
                self.finish_frame = 4
                self.finish_counter = 0
                return result
            return result

        # pit movement and levitation setup
        if self.in_pit:
            current_speed = self.speed  # no run allowed in pit

            # start head raise animation (frames 0 to 3) if pressing space and not already levitating
            if (
                space_pressed_once and 
                not self.rising_out_of_pit and 
                not self.head_raise_active and 
                not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN])
            ):
                self.head_raise_active = True
                self.head_raise_frame = 0
                self.head_raise_counter = 0
                self.head_raise_just_started = True
                self.head_raise_sound.play()
                return "HEAD_RAISE"

        else:
            # normal movement speed (with boost when space is held)
            current_speed = self.boost_speed if keys[pygame.K_SPACE] else self.speed

        # adjust animation speed based on running state
        if not self.in_pit:
            self.walk_anim_speed = 2 if keys[pygame.K_SPACE] else 3
        else:
            self.walk_anim_speed = 3
            
        moving = False # adjust animation speed: faster when running

        # store previous position for step detection
        old_x, old_y = self.x, self.y

        # handle escaped pit moving state (ET can move but stays in head_raise_3)
        if self.escaped_pit_moving:
            # play levitation sound with delay (same as in pit)
            self.levitation_sound_timer += 1
            if self.levitation_sound_timer >= self.levitation_sound_delay:
                self.levitation_sound_timer = 0
                if self.levitation_sound:
                    self.levitation_sound.play()
            
            # ET can move normally but image stays locked to head_raise_3
            if keys[pygame.K_LEFT]:
                self.x -= current_speed
                moving = True
            if keys[pygame.K_RIGHT]:
                self.x += current_speed
                moving = True
            if keys[pygame.K_UP]:
                self.y -= current_speed
                moving = True
            if keys[pygame.K_DOWN]:
                self.y += current_speed
                moving = True
            
            # always keep head_raise_3 image
            self.image = self.head_locked_image
            if keys[pygame.K_RIGHT]:
                self.image = pygame.transform.flip(self.head_locked_image, True, False)
            else:
                self.image = pygame.transform.flip(self.head_locked_image, False, False)
            
            # check if moved enough to count as step
            distance_moved = ((self.x - old_x) ** 2 + (self.y - old_y) ** 2) ** 0.5
            if distance_moved >= self.step_threshold:
                if result is None:
                    result = "STEP"
            
            return result

        
        # trigger head raise animation if standing still and pressing space
        if space_pressed_once and not self.head_raise_active and not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
            self.head_raise_active = True
            self.head_raise_frame = 0
            self.head_raise_counter = 0
            self.head_raise_just_started = True
            self.head_raise_sound.play()
        
        # handle left/right movement
        if keys[pygame.K_LEFT]: # ⭠
            if self.in_pit:
                if self.x > self.pit_left_limit: # left limit in pit
                    self.x -= current_speed
                    moving = True
            else:
                self.x -= current_speed
                moving = True

        if keys[pygame.K_RIGHT]: # ⭢
            if self.in_pit:
                if self.x < self.pit_right_limit: # right limit in pit
                    self.x += current_speed
                    moving = True
            else:
                self.x += current_speed
                moving = True
                
        # handle up/down movement (only outside pit)
        if not self.in_pit:
            if keys[pygame.K_UP] and not self.in_pit:
                self.y -= current_speed
                moving = True
            if keys[pygame.K_DOWN] and not self.in_pit:
                self.y += current_speed
                moving = True
                
        # check if e.t. moved enough to count as a step (in the pit too)
        if self.in_pit and not self.head_raise_active and not self.rising_out_of_pit:
            distance_moved = ((self.x - old_x) ** 2 + (self.y - old_y) ** 2) ** 0.5
            if distance_moved >= self.step_threshold:
                if result is None:
                    result = "STEP"

        self.update_animation(moving, keys)

        # play head raise animation if it's currently active
        if self.head_raise_active:
            self.head_raise_counter += 1
            if self.head_raise_counter >= self.head_raise_speed:
                self.head_raise_counter = 0
                self.head_raise_frame += 1

                if self.in_pit:
                    # in pit: stop at frame 3 and start levitation
                    if self.head_raise_frame == 3:
                        self.head_raise_active = False
                        self.rising_out_of_pit = True
                        self.image = self.head_locked_image
                        self.y -= 9  # small visual jump when starting levitation
                    elif self.head_raise_frame < len(self.images["head_raise"]):
                        self.image = self.images["head_raise"][self.head_raise_frame]
                else:
                    # outside pit: play full animation then return to idle
                    if self.head_raise_frame >= len(self.images["head_raise"]):
                        self.head_raise_active = False
                        self.head_raise_frame = 0
                        self.image = self.images["idle"]
                    else:
                        self.image = self.images["head_raise"][self.head_raise_frame]
            else:
                # hold current frame while counter builds up
                self.image = self.images["head_raise"][self.head_raise_frame]
            return

        # finish head raise animation after landing from levitation (frames 4 to 6)
        if self.finishing_head_raise:
            # block all movement during finishing animation
            self.walk_sound.stop()
            self.run_sound.stop() 
            self.moving = False
            
            self.finish_counter += 1
            if self.finish_counter >= self.head_raise_speed:
                self.finish_counter = 0
                if self.finish_frame <= 6:
                    self.image = self.images["head_raise"][self.finish_frame]
                    self.finish_frame += 1
                else:
                    self.image = self.images["idle"]
                    self.finishing_head_raise = False
            else:
                # maintain current frame while counter progresses
                if self.finish_frame <= 6:
                    self.image = self.images["head_raise"][self.finish_frame]
                else:
                    self.image = self.images["idle"]
            return

        # handle movement sounds
        if self.in_pit:
            # in pit: only walking sounds, no running
            if moving:
                if not self.moving:
                    self.moving = True
                    self.walk_sound.play(-1)
                    self.is_running = False
            else:
                # outside pit: handle both walking and running sounds
                if self.moving:
                    self.walk_sound.stop()
                    self.moving = False
            return result
        else:
            if moving:
                if not self.moving:
                    self.moving = True
                    if keys[pygame.K_SPACE]:
                        self.run_sound.play(-1)
                        self.is_running = True
                    else:
                        self.walk_sound.play(-1)
                        self.is_running = False
                else:
                    # switch between walk and run sounds based on space key
                    if keys[pygame.K_SPACE] and not self.is_running:
                        self.walk_sound.stop()
                        self.run_sound.play(-1)
                        self.is_running = True
                    elif not keys[pygame.K_SPACE] and self.is_running:
                        self.run_sound.stop()
                        self.walk_sound.play(-1)
                        self.is_running = False
            else:
                # stop all sounds when not moving
                if self.moving:
                    self.moving = False
                    self.walk_sound.stop()
                    self.run_sound.stop()
                    
        # check if e.t. moved enough to count as a step
        if not self.in_pit and not self.head_raise_active and result is None:
            distance_moved = ((self.x - old_x) ** 2 + (self.y - old_y) ** 2) ** 0.5
            if distance_moved >= self.step_threshold:
                result = "STEP"

        return result

    def update_animation(self, moving, keys):
        # switch frames when e.t. is moving
        if moving:
            self.walk_counter += 1
            # advance to next frame when counter reaches animation speed
            if self.walk_counter >= self.walk_anim_speed:
                self.walk_counter = 0
                self.walk_frame = (self.walk_frame + 1) % len(self.images["walk"])
            self.image = self.images["walk"][self.walk_frame]
        else:
            # show idle image when not moving
            self.image = self.images["idle"]

        # flip image horizontally when moving right
        if keys[pygame.K_RIGHT]:
            self.image = pygame.transform.flip(self.image, True, False)
            
    def setup_pit_fall(self, center_x, center_y, center_width, center_height):
        """set up parameters for falling into the pit"""
        self.x = center_x + (center_width - self.image.get_width()) // 2
        self.y = center_y
        self.is_falling_into_pit = True
        self.pit_target_y = center_y + 360 - self.image.get_height()
        self.pit_escape_y = center_y
        self.pit_bottom_y = center_y + 360
        self.pit_left_limit = center_x + 192
        self.pit_right_limit = center_x + center_width - 192 - self.image.get_width()
        self.rising_out_of_pit = False

    def reset_for_level_transition(self, new_x, new_y):
        """reset E.T. for a level transition"""
        self.x = new_x
        self.y = new_y
        self.in_pit = False
        self.is_falling_into_pit = False
        self.rising_out_of_pit = False
        self.head_raise_active = False
        self.finishing_head_raise = False
        self.image = self.images["idle"]
        self.walk_sound.stop()
        self.run_sound.stop()
        self.moving = False

    def draw(self, screen, spaceship=None):
        # if e.t. is in the spaceship during intro, apply the same clipping
        if spaceship is not None and spaceship.is_et_in_spaceship():
            # visible zone starts at y = 71 (top of playable screen)
            visible_zone_top = 71
            
            # calculate e.t.'s drawing position
            idle_height = self.images["idle"].get_height()
            image_height = self.image.get_height()
            height_diff = image_height - idle_height
            draw_y = self.y - height_diff
            
            # if e.t. is completely above the visible zone
            if draw_y + image_height <= visible_zone_top:
                return  # draw nothing
            
            # if e.t. is partially or completely visible
            if draw_y < visible_zone_top:
                # top part cut - calculate which part to draw
                cut_top = visible_zone_top - draw_y
                visible_height = image_height - cut_top
                
                # create subsurface (visible part only)
                visible_part = self.image.subsurface(0, cut_top, self.image.get_width(), visible_height)
                screen.blit(visible_part, (self.x, visible_zone_top))
            else:
                # e.t. completely visible
                screen.blit(self.image, (self.x, draw_y))
        else:
            # normal e.t. display
            idle_height = self.images["idle"].get_height()
            image_height = self.image.get_height()
            height_diff = image_height - idle_height
            draw_y = self.y - height_diff
            screen.blit(self.image, (self.x, draw_y))
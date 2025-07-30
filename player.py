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

        # head raising (used for levitation)
        self.head_raise_active = False
        self.head_raise_frame = 0
        self.head_raise_counter = 0
        self.head_raise_sound = head_raise_sound
        self.head_raise_speed = 5 # animation speed

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
        self.ready_to_levitate = False  # becomes True when head_raise_3 is reached
        self.levitation_speed = 2 # control how fast E.T. goes up/down during levitation
        self.finishing_head_raise = False
        self.finish_frame = 4
        self.finish_counter = 0


    def handle_input(self, keys, space_pressed_once):
        # block all movement when head raise animation is playing (except in pit)
        if self.head_raise_active and not self.in_pit:
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
            return

        # handle falling into pit animation
        if self.is_falling_into_pit:
            self.walk_sound.stop()
            self.run_sound.stop()
            self.image = self.images["idle"]
            self.image = pygame.transform.flip(self.image, False, False)
            self.moving = False
            self.y += self.pit_fall_speed

            # check if E.T. has reached the bottom of the pit
            if self.y >= self.pit_target_y:
                self.y = self.pit_target_y
                self.is_falling_into_pit = False
                self.in_pit = True

            # flip image to right only if right key is held
            if keys[pygame.K_RIGHT]:
                self.image = pygame.transform.flip(self.image, True, False)
            else:
                self.image = pygame.transform.flip(self.image, False, False)
            return

        # handle levitation when trying to escape from pit
        if self.in_pit and self.rising_out_of_pit:
            self.image = self.head_locked_image  # always show head_raise_3

            # move up when up key is pressed (levitation)
            if keys[pygame.K_UP]:
                self.y -= self.levitation_speed
            # move down when down key is pressed (levitation)
            if keys[pygame.K_DOWN]:
                self.y += self.levitation_speed
            
            # flip image to right temporarily
            if keys[pygame.K_RIGHT]:
                self.image = pygame.transform.flip(self.head_locked_image, True, False)
            else:
                self.image = pygame.transform.flip(self.head_locked_image, False, False)

            # check if ET reached the top of the pit (escaped the pit?)
            et_top_y = self.y - (self.image.get_height() - self.images["idle"].get_height())
            if et_top_y <= self.pit_escape_y:
                self.rising_out_of_pit = False
                self.image = self.images["idle"]
                return "ESCAPE_PIT"

            # check if ET reached the bottom platform of the pit
            et_bottom_y = self.y + self.images["idle"].get_height()
            if et_bottom_y >= self.pit_bottom_y:
                self.rising_out_of_pit = False
                self.finishing_head_raise = True
                self.finish_frame = 4
                self.finish_counter = 0
                return
            return

        # pit movement and levitation setup
        if self.in_pit:
            current_speed = self.speed  # no run allowed in pit

            # start head raise animation (frames 0 to 3) if pressing SPACE and not already levitating
            if (
                space_pressed_once and 
                not self.rising_out_of_pit and 
                not self.head_raise_active and 
                not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN])
            ):
                self.head_raise_active = True
                self.head_raise_frame = 0
                self.head_raise_counter = 0
                self.head_raise_sound.play()
                return

            # if rising is in progress and head_raise_3.png was reached
            if self.rising_out_of_pit:
                self.image = self.head_locked_image

                # move up during levitation
                if keys[pygame.K_UP]:
                    self.y -= self.levitation_speed
                # move down but don't go below pit bottom
                if keys[pygame.K_DOWN]:
                    et_bottom_y = self.y
                    if et_bottom_y + self.levitation_speed <= self.pit_bottom_y:
                        self.y += self.levitation_speed

                # flip image based on direction
                if keys[pygame.K_RIGHT]:
                    self.image = pygame.transform.flip(self.head_locked_image, True, False)
                else:
                    self.image = pygame.transform.flip(self.head_locked_image, False, False)

                # escape if top of E.T. reaches top edge
                if self.y <= self.pit_escape_y:
                    self.rising_out_of_pit = False
                    return "ESCAPE_PIT"
                return

        else:
            # normal movement speed (with boost when space is held)
            current_speed = self.boost_speed if keys[pygame.K_SPACE] else self.speed

        # adjust animation speed based on running state
        if not self.in_pit:
            self.walk_anim_speed = 2 if keys[pygame.K_SPACE] else 3
        else:
            self.walk_anim_speed = 3
            
        moving = False # adjust animation speed: faster when running
        
        # trigger head raise animation if standing still and pressing SPACE
        if space_pressed_once and not self.head_raise_active and not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
            self.head_raise_active = True
            self.head_raise_frame = 0
            self.head_raise_counter = 0
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
            return
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
                    # switch between walk and run sounds based on SPACE key
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

    def update_animation(self, moving, keys):
        # switch frames when E.T. is moving
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

    def draw(self, screen):
        # draw E.T. positioned from his feet (bottom of idle sprite)
        idle_height = self.images["idle"].get_height()
        image_height = self.image.get_height()
        height_diff = image_height - idle_height
        draw_y = self.y - height_diff

        screen.blit(self.image, (self.x, draw_y))
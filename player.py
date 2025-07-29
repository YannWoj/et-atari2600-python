# player.py
import pygame

class ET:
    def __init__(self, x, y, walk_sound, run_sound):
        # load E.t images (idle and walking frames)
        self.images = {
            "idle": pygame.image.load("assets/images/e.t/idle/et_idle.png"),
            "walk": [
                pygame.image.load("assets/images/e.t/walking/et_walking_1.png"),
                pygame.image.load("assets/images/e.t/walking/et_walking_2.png"),
                pygame.image.load("assets/images/e.t/walking/et_walking_3.png")
            ],
            "head_raise": [
                pygame.image.load("assets/images/e.t/head_raisingo/et_head_raise_0.png"),
                pygame.image.load("assets/images/e.t/head_raisingo/et_head_raise_1.png"),
                pygame.image.load("assets/images/e.t/head_raisingo/et_head_raise_2.png"),
                pygame.image.load("assets/images/e.t/head_raisingo/et_head_raise_3.png"),
                pygame.image.load("assets/images/e.t/head_raisingo/et_head_raise_4.png"),
                pygame.image.load("assets/images/e.t/head_raisingo/et_head_raise_5.png"),
                pygame.image.load("assets/images/e.t/head_raisingo/et_head_raise_6.png")
            ]
        }
        # initial position
        self.x = x
        self.y = y
        # movement speeds
        self.speed = 1.5
        self.boost_speed = 5.2
        # animation control variables
        self.walk_frame = 0
        self.walk_counter = 0
        self.walk_anim_speed = 3
        self.image = self.images["idle"]

        # sounds
        self.walk_sound = walk_sound
        self.run_sound = run_sound
        self.moving = False

        self.is_running = False  # track previous running state

        # head raising
        self.head_raise_active = False
        self.head_raise_frame = 0
        self.head_raise_counter = 0
        self.head_raise_speed = 5 # animation speed


    def handle_input(self, keys, space_pressed_once):
        if self.head_raise_active:
            self.head_raise_counter += 1
            if self.head_raise_counter >= self.head_raise_speed:
                self.head_raise_counter = 0
                self.head_raise_frame += 1
                if self.head_raise_frame >= len(self.images["head_raise"]):
                    self.head_raise_active = False
                    self.head_raise_frame = 0
                else:
                    self.image = self.images["head_raise"][self.head_raise_frame]
            else:
                self.image = self.images["head_raise"][self.head_raise_frame]
            return
        
        current_speed = self.boost_speed if keys[pygame.K_SPACE] else self.speed # check boost with space key
        self.walk_anim_speed = 2 if keys[pygame.K_SPACE] else 3
        moving = False # adjust animation speed: faster when running
        # trigger head raise animation if standing still and pressing SPACE
        if space_pressed_once and not self.head_raise_active and not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
            self.head_raise_active = True
            self.head_raise_frame = 0
            self.head_raise_counter = 0
        # handle movement
        if keys[pygame.K_LEFT]: # ⭠
            self.x -= current_speed
            moving = True
        if keys[pygame.K_RIGHT]: # ⭢
            self.x += current_speed
            moving = True
        if keys[pygame.K_UP]: # ⭡
            self.y -= current_speed
            moving = True
        if keys[pygame.K_DOWN]: # ⭣
            self.y += current_speed
            moving = True
            
        self.update_animation(moving, keys)

        # play head raise animation if it's active
        if self.head_raise_active:
            self.head_raise_counter += 1
            # check if it's time to show the next frame
            if self.head_raise_counter >= self.head_raise_speed:
                self.head_raise_counter = 0
                self.head_raise_frame += 1
                # if the animation is finished, reset everything
                if self.head_raise_frame >= len(self.images["head_raise"]):
                    self.head_raise_active = False
                    self.head_raise_frame = 0
                else:
                    self.image = self.images["head_raise"][self.head_raise_frame]
            else:
                self.image = self.images["head_raise"][self.head_raise_frame]
            return

        # handle movement sounds
        if moving:
            if not self.moving:
                # first time moving
                self.moving = True
                if keys[pygame.K_SPACE]:
                    self.run_sound.play(-1)
                    self.is_running = True
                else:
                    self.walk_sound.play(-1)
                    self.is_running = False
            else:
                # already moving → check if running state changed
                if keys[pygame.K_SPACE] and not self.is_running:
                    self.walk_sound.stop()
                    self.run_sound.play(-1)
                    self.is_running = True
                # switched from running to walking
                elif not keys[pygame.K_SPACE] and self.is_running:
                    self.run_sound.stop()
                    self.walk_sound.play(-1)
                    self.is_running = False
        else:
            if self.moving:
                # stop all sounds when stopping
                self.moving = False
                self.walk_sound.stop()
                self.run_sound.stop()


    def update_animation(self, moving, keys):
        # switch frames when E.t is moving
        if moving:
            self.walk_counter += 1
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
        rect = self.image.get_rect()
        # adjust Y to keep the feet at the same position on screen
        y_offset = rect.height - self.images["idle"].get_height()
        draw_y = self.y - y_offset
        screen.blit(self.image, (self.x, draw_y))
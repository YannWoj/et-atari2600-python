# player.py
import pygame

class ET:
    def __init__(self, x, y, walk_sound, run_sound):
        # load ET images (idle and walking frames)
        self.images = {
            "idle": pygame.image.load("assets/images/e.t/idle/et_idle.png"),
            "walk": [
                pygame.image.load("assets/images/e.t/walking/et_walking_1.png"),
                pygame.image.load("assets/images/e.t/walking/et_walking_2.png"),
                pygame.image.load("assets/images/e.t/walking/et_walking_3.png")
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

    def handle_input(self, keys):
        current_speed = self.boost_speed if keys[pygame.K_SPACE] else self.speed # check boost with space key
        self.walk_anim_speed = 2 if keys[pygame.K_SPACE] else 3
        moving = False # adjust animation speed: faster when running
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
        # draw ET on the screen
        screen.blit(self.image, (self.x, self.y))
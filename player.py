import pygame

class ET:
    def __init__(self, x, y):
        # load ET images (idle and walking frames)
        self.images = {
            "idle": pygame.image.load("assets/images/e.t/idle/et_idle.png"),
            "walk": [
                pygame.image.load("assets/images/e.t/walking/et_walking_1.png"),
                pygame.image.load("assets/images/e.t/walking/et_walking_2.png"),
                # pygame.image.load("assets/images/e.t/walking/et_walking_3.png") # This image was in the initial game, but in my opinion, the game looks better without it.
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
        self.walk_anim_speed = 4.20
        self.image = self.images["idle"]

    def handle_input(self, keys):
        # check boost with space key
        current_speed = self.boost_speed if keys[pygame.K_SPACE] else self.speed
        moving = False
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
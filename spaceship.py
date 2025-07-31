# spaceship.py
import pygame

class Spaceship:
    def __init__(self, x, y):
        # load animation images
        self.images = [
            pygame.image.load(f"assets/images/spaceship/spaceship_{i}.png")
            for i in range(6)
        ]
        self.x = x
        self.y = y
        self.frame = 0
        self.counter = 0
        self.anim_speed = 6  # blink speed (for spaceship colors)
        self.image = self.images[0]
        
        # spaceship states
        self.state = "DESCENDING"  # DESCENDING, / ASCENDING / HIDDEN
        self.descent_speed = 2 # descent speed
        self.ascent_speed = 5.5 # ascent speed
        
        # starting position (off-screen, at the top)
        self.start_y = y - 150  # commence au-dessus de l'écran
        self.y = self.start_y
        
        # target position to drop E.T. (230px from the top of the playable screen for E.T.'s head)
        # E.T. is at (23, 26) in the spaceship, so we calculate where the spaceship should be
        self.target_y_for_drop = 0
        
        # to know if E.T. has been dropped
        self.et_dropped = False
        
    def set_drop_target(self, center_y):
        """calculates the target Y position of the spaceship to drop E.T. at the right place"""
        # target position for E.T.'s head: 230px from the top of the playable screen
        et_head_target_y = center_y + 230
        # E.T. is at (x: 23, y: 26) in the spaceship, so the spaceship should be at:
        self.target_y_for_drop = et_head_target_y - 26
        
    def get_et_position(self):
        # returns E.T.'s position when he's in the spaceship
        et_x = self.x + 23
        et_y = self.y + 26
        return et_x, et_y
        
    def update(self, center_y):
        """updates the spaceship according to its state"""
        # color animation
        self.counter += 1
        if self.counter >= self.anim_speed:
            self.counter = 0
            self.frame = (self.frame + 1) % len(self.images)
            self.image = self.images[self.frame]
        
        # movement logic according to state
        if self.state == "DESCENDING":
            if self.target_y_for_drop == 0:
                self.set_drop_target(center_y)
            
            self.y += self.descent_speed
            
            # check if we've reached the drop position
            if self.y >= self.target_y_for_drop:
                self.y = self.target_y_for_drop
                self.et_dropped = True
                self.state = "ASCENDING"
                
        elif self.state == "ASCENDING":
            self.y -= self.ascent_speed
            
            # disappears when it reaches the invisible zone (y <= -29)
            if self.y <= self.start_y:
                self.state = "HIDDEN"
    
    def is_et_in_spaceship(self):
        """returns True if E.T. is still in the spaceship"""
        return self.state == "DESCENDING"
    
    def is_visible(self):
        """returns True if the spaceship should be displayed"""
        return self.state != "HIDDEN"
    
    def reset_for_new_game(self, start_x, start_y):
        """resets the spaceship to its initial state for a new game"""
        self.x = start_x
        self.start_y = 71 - 100  # -29px from the top of the pygame window
        self.y = self.start_y
        self.state = "DESCENDING"
        self.et_dropped = False
        self.target_y_for_drop = 0
        self.frame = 0
        self.counter = 0

    # draws the spaceship with clipping - only the visible part is displayed
    def draw(self, screen):
        if self.is_visible():
            visible_zone_top = 71 # visible zone starts at y = 71 (top of the playable screen)
            
            # if the spaceship is completely above the visible zone
            if self.y + 100 <= visible_zone_top:  # bottom of spaceship above 71px
                return
            
            # if the spaceship is partially or completely visible
            if self.y < visible_zone_top:
                cut_top = visible_zone_top - self.y  # how many pixels to cut from the top
                visible_height = 100 - cut_top  # visible height of the spaceship
                
                # create a subsurface (visible part only)
                visible_part = self.image.subsurface(0, cut_top, 96, visible_height)
                screen.blit(visible_part, (self.x, visible_zone_top))
            else:
                # spaceship completely visible
                screen.blit(self.image, (self.x, self.y))
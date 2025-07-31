# counter.py
import pygame

class Counter:
    def __init__(self):
        # load all digit images (0-9)
        self.digit_images = {}
        for i in range(10):
            self.digit_images[i] = pygame.image.load(f"assets/images/counter/counter_{i}.png")
        
        # counter properties
        self.value = 9999  # starting value
        self.digit_width = 42  # width of each digit image
        self.digit_height = 22  # height of each digit image
        self.digit_spacing = 6  # spacing between digits
        
        # game state tracking
        self.is_active = False  # counter only appears in game screens (not title)
        
    def activate(self):
        # activate the counter when entering game mode
        self.is_active = True
    
    def deactivate(self):
        # deactivate the counter when returning to title
        self.is_active = False
        
    def reset(self):
        # reset counter to initial value for new game
        self.value = 9999
        
    def decrement(self, amount):
        # decrement counter by specified amount, ensuring it doesn't go below 0
        self.value = max(0, self.value - amount)
        return self.value == 0  # return True if game over (counter reached 0)
    
    def decrement_step(self):
        # decrement by 1 (for each step E.T. takes)
        return self.decrement(1)
    
    def decrement_head_raise(self):
        # decrement by 19 (for head raise action)
        return self.decrement(19)
        
    def decrement_fall(self):
        # decrement by 269 (for falling into pit)
        return self.decrement(269)
    
    def get_digits(self):
        # convert counter value to list of 4 digits
        # ensure value is between 0 and 9999
        clamped_value = max(0, min(9999, self.value))
        # convert to 4-digit string with leading zeros
        digits_str = f"{clamped_value:04d}"
        # convert each character to integer
        return [int(digit) for digit in digits_str]
    
    def get_total_width(self):
        # calculate total width needed to display all 4 digits with spacing
        # 4 digits + 3 spaces between them
        return (4 * self.digit_width) + (3 * self.digit_spacing)
    
    def draw(self, screen, screen_width, screen_height, light_blue2_height):
        # draw the counter in the light blue bar at bottom of screen
        if not self.is_active:
            return
            
        # get the 4 digits to display
        digits = self.get_digits()
        
        # calculate total width and starting x position for centering
        total_width = self.get_total_width()
        start_x = (screen_width - total_width) // 2
        
        # calculate y position (centered in light blue bar)
        y = screen_height - light_blue2_height + (light_blue2_height - self.digit_height) // 2
        
        # draw each digit with proper spacing
        current_x = start_x
        for digit in digits:
            screen.blit(self.digit_images[digit], (current_x, y))
            current_x += self.digit_width + self.digit_spacing
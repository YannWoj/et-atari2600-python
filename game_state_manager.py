# game_state_manager.py
import pygame
from graphics import draw_background, draw_center_area, LIGHT_BLUE2_HEIGHT

class GameStateManager:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_state = "TITLE"
        self.previous_state = None
        
        # load images
        self.images = self._load_images()
        
        # game flags
        self.intro_sequence_active = False
        self.game_over = False
        self.music_playing = False
        
    def _load_images(self):
        # loads all images
        return {
            # title screen images
            "et_head_title": pygame.image.load("assets/images/title/et_head_title.png"),
            "et_title": pygame.image.load("assets/images/title/et_title.png"),
            "copyright_title": pygame.image.load("assets/images/title/copyright_atari.png"),
            
            # game screen images
            "forest1": pygame.image.load("assets/images/forest/forest1.png"),
            "forest2": pygame.image.load("assets/images/forest/forest2.png"),
            "forest3": pygame.image.load("assets/images/forest/forest3.png"),
            "forest4": pygame.image.load("assets/images/forest/forest4.png"),
            "forest5": pygame.image.load("assets/images/forest/forest5.png"),
            "building": pygame.image.load("assets/images/building/building.png"),
            "house": pygame.image.load("assets/images/house/house.png"),
            "pit": pygame.image.load("assets/images/pit/pit.png"),
        }
    
    def change_state(self, new_state, **kwargs):
        # changes the game state with optional parameters
        self.previous_state = self.current_state
        self.current_state = new_state
        
        # specific actions when changing state
        if new_state == "TITLE":
            self.intro_sequence_active = False
            self.game_over = False
        elif new_state == "FOREST1" and self.previous_state == "TITLE":
            self.intro_sequence_active = True
        elif new_state == "PIT":
            # Configuration spécifique pour le pit
            et = kwargs.get('et')
            if et:
                center_x, center_y, center_width, center_height = draw_center_area(self.screen, self.screen_width, "PIT")
                et.setup_pit_fall(center_x, center_y, center_width, center_height)
    
    def get_current_state(self):
        return self.current_state
    
    def is_intro_active(self):
        return self.intro_sequence_active
    
    def set_intro_active(self, active):
        self.intro_sequence_active = active
    
    def is_game_over(self):
        return self.game_over
    
    def set_game_over(self, game_over):
        self.game_over = game_over
    
    def render_title_screen(self):
        """rendering game screens"""
        draw_background(self.screen, self.screen_width, self.screen_height, "TITLE")
        center_x, center_y, center_width, center_height = draw_center_area(self.screen, self.screen_width, "TITLE")
        
        # draw E.T. title logo
        et_title_rect = self.images["et_title"].get_rect(midtop=(
            center_x + center_width // 2 - 15,
            center_y + 53
        ))
        self.screen.blit(self.images["et_title"], et_title_rect)
        
        # draw E.T. head image
        et_head_title_rect = self.images["et_head_title"].get_rect(midbottom=(
            center_x + center_width // 2 - 4,
            center_y + center_height - 63
        ))
        self.screen.blit(self.images["et_head_title"], et_head_title_rect)
        
        # draw copyright notice
        copyright_rect = self.images["copyright_title"].get_rect(
            center=(self.screen_width // 2, self.screen_height - LIGHT_BLUE2_HEIGHT // 2)
        )
        self.screen.blit(self.images["copyright_title"], copyright_rect)
    
    def render_game_screen(self, state, et, spaceship=None):
        """rendering game screens"""
        # special case for pit: use title background to get black borders
        background_state = "TITLE" if state == "PIT" else state
        draw_background(self.screen, self.screen_width, self.screen_height, background_state)
        center_x, center_y, center_width, center_height = draw_center_area(self.screen, self.screen_width, state)
        
        # show level specific image
        image_key = state.lower()  # convert FOREST1 to forest1, etc.
        if image_key in self.images:
            self.screen.blit(self.images[image_key], (center_x, center_y))
        
        return center_x, center_y, center_width, center_height
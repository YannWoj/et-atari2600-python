# level_manager.py
import pygame

class LevelManager:
    def __init__(self):
        # game map definition based on the provided image and Atari testing
        self.level_map = {
            "FOREST1": {  # center of the map
                "connections": {
                    "right": "FOREST5",
                    "left": "FOREST3",
                    "up": "FOREST4",
                    "down": "FOREST2"
                },
                "has_pit": False,
                "pit_positions": [],
                "items": [],
                "enemies": []
            },
            "FOREST2": {
                "connections": {
                    "right": "FOREST5",
                    "left": "FOREST3", 
                    "up": "FOREST1",
                    "down": "BUILDING"
                },
                "has_pit": True,
                "pit_positions": [
                                    (96, 107, 192, 70), # x, y, w, h
                                    (480, 107, 192, 70),
                                    (96, 278, 168, 31),
                                    (504, 278, 168, 31)
                                 ],
                "items": [],
                "enemies": []
            },
            "FOREST3": {
                "connections": {
                    "right": "FOREST2",
                    "left": "FOREST4",
                    "up": "FOREST1",
                    "down": "BUILDING"
                },
                "has_pit": True,
                "pit_positions": [
                                    (72, 76, 240, 63), # x, y, w, h
                                    (456, 76, 240, 63),
                                    (72, 278, 240, 63),
                                    (456, 278, 240, 63)
                                 ],
                "items": [],
                "enemies": []
            },
            "FOREST4": {
                "connections": {
                    "right": "FOREST3",
                    "left": "FOREST5",
                    "up": "FOREST1",
                    "down": "BUILDING"
                },
                "has_pit": True,
                "pit_positions": [
                                    (96, 88, 120, 240), # x, y, w, h
                                    (552, 88, 120, 240),
                                    (312, 107, 144, 44),
                                    (312, 265, 144, 44)
                                 ],
                "items": [],
                "enemies": []
            },
            "FOREST5": {
                "connections": {
                    "right": "FOREST4",
                    "left": "FOREST2",
                    "up": "FOREST1",
                    "down": "BUILDING"
                },
                "has_pit": True,
                "pit_positions": [
                                    (0, 57, 120, 44), # x, y, w, h
                                    (264, 57, 240, 44),
                                    (648, 57, 120, 44),
                                    (96, 183, 192, 50),
                                    (480, 183, 192, 50),
                                    (0, 315, 120, 45),
                                    (264, 315, 240, 45),
                                    (648, 315, 120, 45)
                                 ],
                "items": [],
                "enemies": []
            },
            "BUILDING": {
                "connections": {
                    "right": "FOREST3",
                    "left": "FOREST5",
                    "up": "FOREST4",
                    "down": "FOREST2"
                },
                "has_pit": False,
                "pit_positions": [],
                "items": [],
                "enemies": []
            },
            "HOUSE": {
                "connections": {
                    "right": None,
                    "left": None,
                    "up": "FOREST5",
                    "down": None
                },
                "has_pit": False,
                "pit_positions": [],
                "items": [],
                "enemies": []
            },
            "PIT": {
                "connections": {
                    "escape": "FOREST2"  # when e.t. escapes from the pit
                },
                "has_pit": False,
                "pit_positions": [],
                "items": [],
                "enemies": []
            }
        }
        
        self.current_level = "FOREST1"
        # track which level ET fell from to return there
        self.pit_escape_level = None
        # track which pit ET fell into
        self.current_pit_bounds = None
    
    def get_current_level_data(self):
        """returns the current level data"""
        return self.level_map.get(self.current_level, {})
    
    def can_move_to(self, direction):
        """checks if we can move in a direction"""
        level_data = self.get_current_level_data()
        connections = level_data.get("connections", {})
        return connections.get(direction) is not None
    
    def get_next_level(self, direction):
        """returns the next level in a direction"""
        level_data = self.get_current_level_data()
        connections = level_data.get("connections", {})
        return connections.get(direction)
    
    def change_level(self, direction):
        """changes level in a direction"""
        next_level = self.get_next_level(direction)
        if next_level:
            self.current_level = next_level
            return True
        return False
    
    def set_level(self, level_name):
        """forces change to a specific level"""
        if level_name in self.level_map:
            self.current_level = level_name
            return True
        return False
    
    def get_current_level(self):
        return self.current_level
    
    def has_pit_at_position(self, x, y, et_width, et_height):
        level_data = self.get_current_level_data()
        pit_positions = level_data.get("pit_positions", [])
        
        for pit_x, pit_y, pit_width, pit_height in pit_positions:
            if (x < pit_x + pit_width and 
                x + et_width > pit_x and 
                y < pit_y + pit_height and 
                y + et_height > pit_y):
                # store the exact pit that was touched
                self.pit_escape_level = self.current_level
                self.current_pit_bounds = (pit_x, pit_y, pit_width, pit_height)
                return True
        return False

    def get_pit_center_position(self, center_x, center_y, et_width, et_height):
        """returns the center position of the pit ET fell into"""
        if not self.current_pit_bounds:
            return center_x + (768 - et_width) // 2, center_y + (360 - et_height) // 2
        
        pit_x, pit_y, pit_width, pit_height = self.current_pit_bounds
        # center ET on the pit
        centered_x = center_x + pit_x + (pit_width - et_width) // 2
        centered_y = center_y + pit_y + (pit_height - et_height) // 2
        return centered_x, centered_y
    
    def check_level_boundaries(self, et_x, et_y, et_width, et_height, center_x, center_y, center_width, center_height):
        """checks level boundaries and handles transitions"""
        transition = None
        
        # check borders and determine transition direction
        if et_x > center_x + center_width - et_width:  # right border
            if self.can_move_to("right"):
                transition = "right"
        elif et_x < center_x:  # left border
            if self.can_move_to("left"):
                transition = "left"
        elif et_y < center_y:  # top border
            if self.can_move_to("up"):
                transition = "up"
        elif et_y > center_y + center_height - et_height:  # bottom border
            if self.can_move_to("down"):
                transition = "down"
        
        return transition
    
    def get_spawn_position(self, from_direction, center_x, center_y, center_width, center_height, et_width, et_height):
        """returns the spawn position of E.T. based on the direction he comes from"""
        if from_direction == "right":  # comes from the right, spawn on the left
            return center_x + 10, center_y + center_height // 2
        elif from_direction == "left":  # comes from the left, spawn on the right
            return center_x + center_width - et_width - 10, center_y + center_height // 2
        elif from_direction == "up":  # comes from the top, spawn at the bottom
            return center_x + center_width // 2, center_y + center_height - et_height - 10
        elif from_direction == "down":  # comes from the bottom, spawn at the top
            return center_x + center_width // 2, center_y + 10
        else:  # default position (center)
            return center_x + (center_width - et_width) // 2, center_y + (center_height - et_height) // 2

    def get_pit_escape_level(self):
        """returns the level to escape to from pit"""
        return self.pit_escape_level
    
    def is_outside_pit(self, et_x, et_y, et_width, et_height, center_x, center_y):
        """checks if ET is outside the current pit bounds"""
        if not self.current_pit_bounds:
            return True
        
        pit_x, pit_y, pit_width, pit_height = self.current_pit_bounds
        # adjust pit coordinates relative to center
        abs_pit_x = center_x + pit_x
        abs_pit_y = center_y + pit_y
        
        # check if ET is completely outside pit bounds
        return (et_x + et_width <= abs_pit_x or 
                et_x >= abs_pit_x + pit_width or
                et_y + et_height <= abs_pit_y or
                et_y >= abs_pit_y + pit_height)
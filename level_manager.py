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
                "pit_positions": [(96, 107, 192, 70)], # x, y, w, h
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
                "has_pit": False,
                "pit_positions": [],
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
                "has_pit": False,
                "pit_positions": [],
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
                "has_pit": False,
                "pit_positions": [],
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
        """checks if ET is stepping on a pit"""
        level_data = self.get_current_level_data()
        pit_positions = level_data.get("pit_positions", [])
        
        for pit_x, pit_y, pit_width, pit_height in pit_positions:
            # check if ET's rectangle overlaps with pit rectangle
            if (x < pit_x + pit_width and 
                x + et_width > pit_x and 
                y < pit_y + pit_height and 
                y + et_height > pit_y):
                return True
        return False
    
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
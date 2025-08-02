# graphics.py
import pygame

# colors
PURPLE = (141, 18, 110)
PURPLE_HOUSE = (51, 26, 163)
BLUE = (0, 0, 138)
LIGHT_BLUE = (106, 174, 237)
LIGHT_BLUE2 = (90, 151, 221)
BROWN = (153, 87, 24)
YELLOW = (176, 188, 83)
DARK_GREEN = (0, 57, 0)
LIGHT_GREEN = (71, 115, 35)
BLACK = (0, 0, 0)
GREY = (170, 170, 170)

# rect heights
PURPLE_HEIGHT = 47
LIGHT_BLUE2_HEIGHT = 62
TITLE_TOP_BLACK_HEIGHT = 24
TITLE_BOTTOM_BLACK_HEIGHT = 22
GAME_TOP_BLACK_HEIGHT = 12
GAME_BOTTOM_BLACK_HEIGHT = 13
CENTER_WIDTH = 768
CENTER_HEIGHT = 410

def draw_background(screen, screen_width, screen_height, state):
    # set background color and black bar sizes depending on the current state
    if state == "TITLE":
        background_color = BLACK
        top_black = TITLE_TOP_BLACK_HEIGHT
        bottom_black = TITLE_BOTTOM_BLACK_HEIGHT
    elif state == "BUILDING":
        background_color = GREY
        top_black = GAME_TOP_BLACK_HEIGHT
        bottom_black = GAME_BOTTOM_BLACK_HEIGHT
    elif state == "HOUSE":
        background_color = PURPLE_HOUSE
        top_black = GAME_TOP_BLACK_HEIGHT
        bottom_black = GAME_BOTTOM_BLACK_HEIGHT
    else:
        background_color = DARK_GREEN
        top_black = GAME_TOP_BLACK_HEIGHT
        bottom_black = GAME_BOTTOM_BLACK_HEIGHT
        
    # fill screen with chosen background color
    screen.fill(background_color)

    # DRAW THE STATIC FRAME ELEMENTS
    # draw purple bar at the top
    pygame.draw.rect(screen, PURPLE, (0, 0, screen_width, PURPLE_HEIGHT))
    # draw light blue bar at the bottom
    pygame.draw.rect(screen, LIGHT_BLUE2, (0, screen_height - LIGHT_BLUE2_HEIGHT, screen_width, LIGHT_BLUE2_HEIGHT))
    # draw black bar under the purple
    pygame.draw.rect(screen, BLACK, (0, PURPLE_HEIGHT, screen_width, top_black))
    # draw black bar above the light blue
    pygame.draw.rect(screen, BLACK, (0, screen_height - LIGHT_BLUE2_HEIGHT - bottom_black, screen_width, bottom_black))

# draw the main play area
def draw_center_area(screen, screen_width, state):
    # compute horizontal and vertical position of the center area based on state
    center_x = (screen_width - CENTER_WIDTH) // 2

    # adjust vertical offset based on state to align the center area correctly
    if state == "TITLE":
        top_black = TITLE_TOP_BLACK_HEIGHT
        vertical_offset = 0
    else:
        top_black = GAME_TOP_BLACK_HEIGHT
        vertical_offset = 12

    center_y = PURPLE_HEIGHT + top_black + vertical_offset

    # choose color depending on the state
    if state == "TITLE":
        color = BLUE
    elif state == "FOREST1":
        color = LIGHT_GREEN
    elif state == "FOREST2":
        color = (40, 150, 40)
    elif state == "FOREST3":
        color = (50, 180, 50)
    elif state == "FOREST4":
        color = (20, 60, 20)
    elif state == "FOREST5":
        color = (25, 80, 25)
    elif state == "BUILDING":
        color = (60, 100, 200)
    elif state == "PIT":
        color = BLACK
    elif state == "HOUSE":
        color = (10, 10, 60)
    else:
        color = LIGHT_GREEN  # default color

    # draw the rectangle with the selected color
    pygame.draw.rect(screen, color, (center_x, center_y, CENTER_WIDTH, CENTER_HEIGHT))

    return (center_x, center_y, CENTER_WIDTH, CENTER_HEIGHT)
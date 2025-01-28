import pygame
import sys

pygame.init()

# Screen setup
res = (800, 600)
screen = pygame.display.set_mode(res)
pygame.display.set_caption("2 Teams with Different Passive Colors")

# Basic colors
COLOR_WHITE   = (255, 255, 255)
COLOR_LIGHT   = (170, 170, 170)
COLOR_DARK    = (100, 100, 100)
COLOR_ACTIVE  = pygame.Color("cornsilk1")
COLOR_BLACK   = (0, 0, 0)
BG_COLOR      = (25, 25, 25)

# Passive colors per team (Team 1 = 'crimson', Team 2 = 'green3')
TEAM_PASSIVE_COLORS = [
    pygame.Color("crimson"),  # Team 0
    pygame.Color("green3")    # Team 1
]

# Fonts
font_button = pygame.font.SysFont("Corbel", 35)
font_text   = pygame.font.SysFont("Corbel", 35)

# "Quit" button text
text_quit = font_button.render("Quit", True, COLOR_WHITE)

# Screen dimensions
width, height = screen.get_size()

# Number of teams and number of boxes per team
NUM_TEAMS = 2
NUM_BOXES_PER_TEAM = 10

# Create a 2D list of boxes
player_boxes = []
for team_index in range(NUM_TEAMS):
    boxes_for_this_team = []
    for i in range(NUM_BOXES_PER_TEAM):
        # Position each team's column differently
        # e.g., Team 0 is near x=20, Team 1 is near x=420
        x_pos = 20 + team_index * 400
        y_pos = 20 + 40 * i
        rect = pygame.Rect(x_pos, y_pos, 140, 35)
        boxes_for_this_team.append(rect)
    player_boxes.append(boxes_for_this_team)

# 2D lists for active flags and texts
active = [[False]*NUM_BOXES_PER_TEAM for _ in range(NUM_TEAMS)]
texts = [["" for _ in range(NUM_BOXES_PER_TEAM)] for _ in range(NUM_TEAMS)]

def get_max_text_width():
    """Returns the widest rendered text among all teams/boxes."""
    max_width = 0
    for team_index in range(NUM_TEAMS):
        for box_index in range(NUM_BOXES_PER_TEAM):
            text_width, _ = font_text.size(texts[team_index][box_index])
            if text_width > max_width:
                max_width = text_width
    return max_width

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check if a box was clicked
            for team_index in range(NUM_TEAMS):
                for box_index, box in enumerate(player_boxes[team_index]):
                    if box.collidepoint(mouse_pos):
                        # If you only want ONE box active in the entire UI:
                        active = [[False]*NUM_BOXES_PER_TEAM for _ in range(NUM_TEAMS)]
                        active[team_index][box_index] = True
                    # If you want each team to have its own active box 
                    # (independent of the others), replace the above lines with:
                    # active[team_index] = [False]*NUM_BOXES_PER_TEAM
                    # active[team_index][box_index] = True
            
            # Check if the 'quit' button was clicked
            if (width - 150 <= mouse_pos[0] <= width - 10) and (height - 50 <= mouse_pos[1] <= height - 10):
                pygame.quit()
                sys.exit()
        
        if event.type == pygame.KEYDOWN:
            # Update text for whichever box is active
            for team_index in range(NUM_TEAMS):
                for box_index in range(NUM_BOXES_PER_TEAM):
                    if active[team_index][box_index]:
                        if event.key == pygame.K_BACKSPACE:
                            texts[team_index][box_index] = texts[team_index][box_index][:-1]
                        else:
                            texts[team_index][box_index] += event.unicode
            
            # Press F4 to close (optional)
            if event.key == pygame.K_F4:
                pygame.quit()
                sys.exit()
    
    # Clear the screen
    screen.fill(BG_COLOR)

    # Draw the 'quit' button with hover effect
    mouse = pygame.mouse.get_pos()
    if (width - 150 <= mouse[0] <= width - 10) and (height - 50 <= mouse[1] <= height - 10):
        pygame.draw.rect(screen, COLOR_LIGHT, [width - 150, height - 50, 140, 40])
    else:
        pygame.draw.rect(screen, COLOR_DARK, [width - 150, height - 50, 140, 40])
    screen.blit(text_quit, (width - 110, height - 50))

    # Determine a common width for all boxes
    max_text_width = get_max_text_width()
    common_width   = max(100, max_text_width + 20)  # add some padding

    # Update and draw each team's boxes
    for team_index in range(NUM_TEAMS):
        for box_index, box in enumerate(player_boxes[team_index]):
            # Update the box's width to match the widest text
            box.w = common_width
            
            # Choose the color based on active state and team
            if active[team_index][box_index]:
                color = COLOR_ACTIVE
            else:
                # Use the passive color for this specific team
                color = TEAM_PASSIVE_COLORS[team_index]

            pygame.draw.rect(screen, color, box)

            # Render the text for this box
            text_surf = font_text.render(texts[team_index][box_index], True, COLOR_BLACK)
            text_w, text_h = text_surf.get_size()

            # Center the text in the box
            text_x = box.x + (box.w - text_w) // 2
            text_y = box.y + (box.h - text_h) // 2
            screen.blit(text_surf, (text_x, text_y))

    pygame.display.update()

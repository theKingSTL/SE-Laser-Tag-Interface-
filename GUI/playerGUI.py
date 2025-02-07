import pygame
import sys
import os
sys.path.append(os.path.abspath('../'))

# Now you can import from main.py
from main import getAspect

class TeamBoxUI:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()

        # Load background image
        self.bg_image = pygame.image.load('Photos/logo.jpg')  # Replace with your image path
        self.bg_width, self.bg_height = self.bg_image.get_size()

        # Apply aspect ratio and scale the image as required
        self.bg_x, self.bg_y, self.scaled_bg_image = getAspect(self.bg_image, self.screen)
        
        # Colors
        self.COLOR_WHITE   = (255, 255, 255)
        self.COLOR_LIGHT   = (170, 170, 170)
        self.COLOR_DARK    = (100, 100, 100)
        self.COLOR_ACTIVE  = pygame.Color("cornsilk1")
        self.COLOR_BLACK   = (0, 0, 0)
        self.BG_COLOR      = (0, 0, 0)

        self.TEAM_PASSIVE_COLORS = [
            pygame.Color("crimson"),  # Team 0
            pygame.Color("green3")    # Team 1
        ]

        # Fonts
        self.font_button = pygame.font.SysFont("Corbel", 35)
        self.font_text   = pygame.font.SysFont("Corbel", 35)

        # "Quit" button text
        self.text_quit = self.font_button.render("Quit", True, self.COLOR_WHITE)

        # Team & Box setup
        self.NUM_TEAMS = 2
        self.NUM_BOXES_PER_TEAM = 10
        self.player_boxes = self.create_boxes()
        self.active = [[False] * self.NUM_BOXES_PER_TEAM for _ in range(self.NUM_TEAMS)]
        self.texts = [["" for _ in range(self.NUM_BOXES_PER_TEAM)] for _ in range(self.NUM_TEAMS)]

    def create_boxes(self):
        """Creates a 2D list of rectangles for player boxes."""
        boxes = []
        for team_index in range(self.NUM_TEAMS):
            team_boxes = []
            for i in range(self.NUM_BOXES_PER_TEAM):
                x_pos = 20 + team_index * 400
                y_pos = 20 + 40 * i
                rect = pygame.Rect(x_pos, y_pos, 140, 35)
                team_boxes.append(rect)
            boxes.append(team_boxes)
        return boxes

    def get_max_text_width(self):
        """Returns the widest rendered text width among all teams/boxes."""        
        return max((self.font_text.size(text)[0] for team in self.texts for text in team), default=100) + 20

    def handle_event(self, event):
        """Handles user input events."""
        if event.type == pygame.QUIT:
            return "quit"
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            for team_index in range(self.NUM_TEAMS):
                for box_index, box in enumerate(self.player_boxes[team_index]):
                    if box.collidepoint(mouse_pos):
                        self.active = [[False] * self.NUM_BOXES_PER_TEAM for _ in range(self.NUM_TEAMS)]
                        self.active[team_index][box_index] = True
            
            if (self.width - 150 <= mouse_pos[0] <= self.width - 10) and (self.height - 50 <= mouse_pos[1] <= self.height - 10):
                return "quit"
        
        if event.type == pygame.KEYDOWN:
            for team_index in range(self.NUM_TEAMS):
                for box_index in range(self.NUM_BOXES_PER_TEAM):
                    if self.active[team_index][box_index]:
                        if event.key == pygame.K_BACKSPACE:
                            self.texts[team_index][box_index] = self.texts[team_index][box_index][:-1]
                        else:
                            self.texts[team_index][box_index] += event.unicode
            
            if event.key == pygame.K_F4:
                return "quit"

    def convert_to_grayscale(self, image):
        """Convert an image to grayscale."""
        # Create a copy of the image to avoid modifying the original one
        grayscale_image = image.copy()
        for x in range(grayscale_image.get_width()):
            for y in range(grayscale_image.get_height()):
                r, g, b, a = grayscale_image.get_at((x, y))
                # Convert the pixel to grayscale by averaging the RGB values
                gray = int(0.299 * r + 0.587 * g + 0.114 * b)
                grayscale_image.set_at((x, y), (gray, gray, gray, a))  # Keep alpha if exists
        return grayscale_image

    def draw(self):
        """Renders all UI elements on the screen."""
        # Create a grayscale version of the background image
        grayscale_bg = self.convert_to_grayscale(self.scaled_bg_image)
        
        # Blit the grayscale background image
        self.screen.blit(grayscale_bg, (self.bg_x, self.bg_y))
        
        mouse = pygame.mouse.get_pos()

        # Draw the quit button
        quit_rect = pygame.Rect(self.width - 150, self.height - 50, 140, 40)
        pygame.draw.rect(self.screen, self.COLOR_LIGHT if quit_rect.collidepoint(mouse) else self.COLOR_DARK, quit_rect)
        self.screen.blit(self.text_quit, (self.width - 110, self.height - 50))

        # Determine the common width for all text boxes
        common_width = self.get_max_text_width()

        for team_index in range(self.NUM_TEAMS):
            for box_index, box in enumerate(self.player_boxes[team_index]):
                box.w = common_width
                color = self.COLOR_ACTIVE if self.active[team_index][box_index] else self.TEAM_PASSIVE_COLORS[team_index]
                pygame.draw.rect(self.screen, color, box)

                text_surf = self.font_text.render(self.texts[team_index][box_index], True, self.COLOR_BLACK)
                text_x = box.x + (box.w - text_surf.get_width()) // 2
                text_y = box.y + (box.h - text_surf.get_height()) // 2
                self.screen.blit(text_surf, (text_x, text_y))

        pygame.display.update()

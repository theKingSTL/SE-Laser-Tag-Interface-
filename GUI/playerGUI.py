import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600  # Adjusted to fit all boxes
BOX_WIDTH, BOX_HEIGHT = 100, 40  # Smaller boxes
MARGIN = 10  # Space between boxes

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Team Entry")

# Font
font = pygame.font.Font(None, 24)

# Team Names
teams = {"Red Team": RED, "Green Team": GREEN}

def draw_text(surface, text, position, color=BLACK):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)

class EntryBox:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BOX_WIDTH, BOX_HEIGHT)
        self.text = ""
        self.active = False

    def draw(self, surface):
        pygame.draw.rect(surface, BLACK if self.active else GRAY, self.rect, 2)
        draw_text(surface, self.text, (self.rect.x + 5, self.rect.y + 10))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN and self.text:
                self.text = "CODE" + self.text  # Replaces ID with codename
                self.active = False  # Move focus to next box
                return True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
        return False

# Create entry boxes
def create_boxes():
    boxes = {team: [] for team in teams}
    for i, team in enumerate(teams):
        x_offset = 100 + (i * (SCREEN_WIDTH // 2))  # Separate teams left & right
        for j in range(15):  # 15 total, arranged 2 per row
            x = x_offset + (j % 2) * (BOX_WIDTH + MARGIN)
            y = 150 + (j // 2) * (BOX_HEIGHT + MARGIN)
            boxes[team].append(EntryBox(x, y))
    return boxes

boxes = create_boxes()

class TeamBoxUI:
    def __init__(self, screen, db):
        self.screen = screen
        self.db = db
        self.active_box = None

    def handleEvent(self, event):
        for team in boxes:
            for i, box in enumerate(boxes[team]):
                if box.handle_event(event):
                    if i + 1 < len(boxes[team]):
                        boxes[team][i + 1].active = True
        if event.type == pygame.QUIT:
            return "quit"
        return None

    def draw(self):
        self.screen.fill(WHITE)
        draw_text(self.screen, "Enter IDs. Press Enter to confirm.", (SCREEN_WIDTH//2 - 120, 50))
        for i, (team, color) in enumerate(teams.items()):
            x_offset = 100 + (i * (SCREEN_WIDTH // 2))
            draw_text(self.screen, team, (x_offset, 100), color)
            for box in boxes[team]:
                box.draw(self.screen)
        pygame.display.flip()
import pygame
import time

class scoreBoard:
    def __init__(self, screen, ids, names, nameConnect, Client, server):
        self.screen = screen
        self.ids = ids
        self.names = names
        self.nameConnect = nameConnect
        self.Client = Client
        self.server = server
        self.start_time = time.time()  # Start time
        self.duration = 6 * 60 + 30   # 6 minutes and 30 seconds
        self.scores = {"Red Team": 0, "Green Team": 0}  # Team scores
        self.font = pygame.font.Font(None, 36)  # Font for text
        self.neon_colors = {
            "pink": (255, 105, 180),
            "blue": (0, 255, 255),
            "green": (0, 255, 0),
            "red": (255, 0, 0)
        }
        self.padding = 20  # Space between elements

    def handleEvent(self, event):
        if event.type == pygame.QUIT:
            return "quit"
        return None

    def draw(self):
        self.screen.fill((0, 0, 0))  # Fill screen with black

        # Calculate elapsed time
        elapsed_time = time.time() - self.start_time
        remaining_time = max(0, self.duration - elapsed_time)

        # Stop the game if time is up
        if remaining_time <= 0:
            return "Done"

        screen_width, screen_height = self.screen.get_size()

        # Define section widths (each section takes 1/3 of the screen width)
        section_width = screen_width // 3

        # Draw Green Team on the right
        green_team_rect = pygame.Rect(2 * section_width + self.padding, self.padding, section_width - 2 * self.padding, screen_height - 2 * self.padding)
        self.draw_team_section(green_team_rect, "Green Team", self.neon_colors["green"])

        # Draw Scoreboard in the middle
        scoreboard_rect = pygame.Rect(section_width + self.padding, self.padding, section_width - 2 * self.padding, screen_height * 2 // 3 - 2 * self.padding)
        self.draw_scoreboard(scoreboard_rect)

        # Draw Timer at the bottom of the middle section
        timer_rect = pygame.Rect(section_width + self.padding, screen_height * 2 // 3 + self.padding, section_width - 2 * self.padding, screen_height // 3 - 2 * self.padding)
        self.draw_timer(timer_rect, remaining_time)

        # Draw Red Team on the left
        red_team_rect = pygame.Rect(self.padding, self.padding, section_width - 2 * self.padding, screen_height - 2 * self.padding)
        self.draw_team_section(red_team_rect, "Red Team", self.neon_colors["red"])

        pygame.display.flip()  # Update display

    def draw_team_section(self, rect, team_name, color):
        pygame.draw.rect(self.screen, color, rect, 2)  # Draw border
        team_font = pygame.font.Font(None, 48)
        team_text = team_font.render(team_name, True, color)
        self.screen.blit(team_text, (rect.x + 10, rect.y + 10))

        # TODO: Check to make sure scores are updating correctly
        # TODO: Check that each name has player_id and vice versa
        y_offset = rect.y + 60
        for player_id, names in zip(self.ids, self.names):
            # for red team
            if (color[0] == 255):
                    player_name = self.font.render(names[0], True, color)
                    self.screen.blit(player_name, (rect.x + 20, y_offset))
                    y_offset += 30
            
            # for green team
            if (color[0] == 0):
                    player_name = self.font.render(names[1], True, color)
                    self.screen.blit(player_name, (rect.x + 20, y_offset))
                    y_offset += 30

    def draw_scoreboard(self, rect):
        pygame.draw.rect(self.screen, self.neon_colors["blue"], rect, 2)
        action_font = pygame.font.Font(None, 36)
        action_text = action_font.render("Game Actions", True, self.neon_colors["blue"])
        self.screen.blit(action_text, (rect.x + 10, rect.y + 10))

        # Example game event
        event_example = action_font.render("Player 1 hit Player 2!", True, self.neon_colors["pink"])
        self.screen.blit(event_example, (rect.x + 20, rect.y + 60))

    def draw_timer(self, rect, remaining_time):
        pygame.draw.rect(self.screen, self.neon_colors["pink"], rect, 2)
        timer_font = pygame.font.Font(None, 48)
        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)
        timer_text = timer_font.render(f"Time Left: {minutes:02}:{seconds:02}", True, self.neon_colors["pink"])
        self.screen.blit(timer_text, (rect.x + 20, rect.y + 20))

    def updateScore(self, team, points):
        if team in self.scores:
            self.scores[team] += points

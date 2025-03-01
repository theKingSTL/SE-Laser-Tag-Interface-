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
        self.start_time = time.time()  # Record the start time
        self.duration = 6 * 60 + 30   # 6 minutes for the time to play plus the 30 for warning 
        self.scores = {"Red Team": 0, "Green Team": 0}  # Initialize scores for two teams
        self.font = pygame.font.Font(None, 36)  # Font for rendering text
        self.neon_colors = {
            "pink": (255, 105, 180),
            "blue": (0, 255, 255),
            "green": (0, 255, 0),
            "red": (255, 0, 0)
        }
        self.padding = 20

    def handleEvent(self, event):
        if event.type == pygame.QUIT:
            return "quit"
        # Handle other events (e.g., score updates) here if needed
        return None

    def draw(self):
        # Clear the screen
        self.screen.fill((0, 0, 0))  # Fill with black

        # Calculate elapsed time
        elapsed_time = time.time() - self.start_time
        remaining_time = max(0, self.duration - elapsed_time)

        # Stop the game if time is up
        if remaining_time <= 0:
            return "Done"

        # Get screen dimensions
        screen_width, screen_height = self.screen.get_size()

        # Draw the top 1/3 for player names and scores
        self.draw_player_section(screen_width, screen_height)

        # Draw the bottom 1/2 for current game actions
        self.draw_game_actions(screen_width, screen_height)

        # Draw the remaining time in the bottom remaining part
        self.draw_timer(screen_width, screen_height, remaining_time)

        # Update the display
        pygame.display.flip()

    def draw_player_section(self, screen_width, screen_height):
        # Calculate the top section dimensions
        top_section_height = screen_height // 3
        section_width = screen_width // 2

        # Draw Red Team
        red_team_rect = pygame.Rect(self.padding, self.padding, section_width - 2 * self.padding, top_section_height - 2 * self.padding)
        self.draw_team_section(red_team_rect, "Red Team", self.neon_colors["red"])

        # Draw Green Team
        green_team_rect = pygame.Rect(section_width + self.padding, self.padding, section_width - 2 * self.padding, top_section_height - 2 * self.padding)
        self.draw_team_section(green_team_rect, "Green Team", self.neon_colors["green"])

    def draw_team_section(self, rect, team_name, color):
        pygame.draw.rect(self.screen, color, rect, 2)  # Draw border
        team_font = pygame.font.Font(None, 48)
        team_text = team_font.render(team_name, True, color)
        self.screen.blit(team_text, (rect.x + 10, rect.y + 10))

        # Draw player names and scores
        y_offset = rect.y + 60
        for player_id, name in zip(self.ids, self.names):
            player_text = self.font.render(f"{name}: {self.scores[team_name]}", True, color)
            self.screen.blit(player_text, (rect.x + 20, y_offset))
            y_offset += 30

    def draw_game_actions(self, screen_width, screen_height):
        # Calculate the bottom section dimensions
        bottom_section_height = screen_height // 2
        bottom_section_rect = pygame.Rect(self.padding, screen_height // 3 + self.padding, screen_width - 2 * self.padding, bottom_section_height - 2 * self.padding)

        # Draw the game actions section
        pygame.draw.rect(self.screen, self.neon_colors["blue"], bottom_section_rect, 2)
        action_font = pygame.font.Font(None, 36)
        action_text = action_font.render("Current Game Actions", True, self.neon_colors["blue"])
        self.screen.blit(action_text, (bottom_section_rect.x + 10, bottom_section_rect.y + 10))

        # Example action text
        action_example = action_font.render("Player 1 scored a goal!", True, self.neon_colors["pink"])
        self.screen.blit(action_example, (bottom_section_rect.x + 20, bottom_section_rect.y + 60))

    def draw_timer(self, screen_width, screen_height, remaining_time):
        # Calculate the timer section dimensions
        timer_section_height = screen_height - (screen_height // 3 + screen_height // 2)
        timer_section_rect = pygame.Rect(self.padding, screen_height // 3 + screen_height // 2 + self.padding, screen_width - 2 * self.padding, timer_section_height - 2 * self.padding)

        # Draw the timer section
        pygame.draw.rect(self.screen, self.neon_colors["pink"], timer_section_rect, 2)
        timer_font = pygame.font.Font(None, 48)
        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)
        timer_text = timer_font.render(f"Time Left: {minutes:02}:{seconds:02}", True, self.neon_colors["pink"])
        self.screen.blit(timer_text, (timer_section_rect.x + 20, timer_section_rect.y + 20))

    def updateScore(self, team, points):
        if team in self.scores:
            self.scores[team] += points
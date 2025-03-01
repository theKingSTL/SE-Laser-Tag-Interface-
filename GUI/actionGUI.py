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
        self.duration = 6 * 60   # 6 minutes in seconds
        self.scores = {"Team A": 0, "Team B": 0}  # Initialize scores for two teams
        self.font = pygame.font.Font(None, 36)  # Font for rendering text

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
            return "time_up"

        # Render the scores
        score_text = self.font.render(f"Team A: {self.scores['Team A']}  Team B: {self.scores['Team B']}", True, (255, 255, 255))
        self.screen.blit(score_text, (50, 50))

        # Render the timer
        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)
        timer_text = self.font.render(f"Time Left: {minutes:02}:{seconds:02}", True, (255, 255, 255))
        self.screen.blit(timer_text, (50, 100))

        # Render player names and IDs
        y_offset = 150
        for player_id, name in zip(self.ids, self.names):
            player_text = self.font.render(f"Player {player_id}: {name}", True, (255, 255, 255))
            self.screen.blit(player_text, (50, y_offset))
            y_offset += 30

        # Update the display
        pygame.display.flip()

    def updateScore(self, team, points):
        if team in self.scores:
            self.scores[team] += points
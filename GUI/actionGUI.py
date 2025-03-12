
import pygame
import time

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0  # Initialize score to zero

class scoreBoard:
    def __init__(self, screen, ids, names, nameConnectID, idConnectEquip, Client, server):
        self.screen = screen
        self.ids = ids
        self.names = names  # List of player names for Red Team and Green Team
        self.nameConnect = nameConnectID
        self.idConnectEquip = idConnectEquip
        self.Client = Client
        self.server = server
        self.start_time = time.time()  # Start time
        self.duration = 6 * 60  # 6 minutes
        self.scores = {"Red Team": 0, "Green Team": 0}  # Team scores
        self.font = pygame.font.Font(None, 36)  # Font for text
        self.neon_colors = {
            "pink": (255, 105, 180),
            "blue": (0, 255, 255),
            "green": (0, 255, 0),
            "red": (255, 0, 0),
            "white": (255, 255, 255)
        }
        self.padding = 20  # Space between elements

        #Filter out the empty names
        self.redNamesFilt = list(filter(lambda item: item != "", self.names[0]))
        self.greenNamesFilt = list(filter(lambda item: item != "", self.names[1]))

        # Initialize players as objects from self.names
        self.redPlayers = [Player(name) for name in self.redNamesFilt]  # Red Team
        self.greenPlayers = [Player(name) for name in self.greenNamesFilt]  # Green Team

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

        # Draw Red Team on the left with neon transparent red
        red_surface = pygame.Surface((section_width, screen_height), pygame.SRCALPHA)
        red_surface.fill((255, 0, 0, 50))  # Neon transparent red
        self.screen.blit(red_surface, (0, 0))
        self.drawTeamSection(0, "Red Team", self.neon_colors["white"], self.redPlayers)

        # Draw Green Team on the right with neon transparent green
        green_surface = pygame.Surface((section_width, screen_height), pygame.SRCALPHA)
        green_surface.fill((0, 255, 0, 50))  # Neon transparent green
        self.screen.blit(green_surface, (2 * section_width, 0))
        self.drawTeamSection(2 * section_width, "Green Team", self.neon_colors["white"], self.greenPlayers)

        # Draw middle section (black)
        middle_surface = pygame.Surface((section_width, screen_height))
        middle_surface.fill((0, 0, 0))  # Black
        self.screen.blit(middle_surface, (section_width, 0))

        # Draw Timer at the bottom 1/6 of the middle section
        timer_rect = pygame.Rect(section_width, screen_height * 5 // 6, section_width, screen_height // 6)
        self.draw_timer(timer_rect, remaining_time)

        pygame.display.flip()  # Update display

    def drawTeamSection(self, x_offset, team_name, color, players):
        team_font = pygame.font.Font(None, 64)  # Bigger font for team name

        # Center the team name text
        team_text = team_font.render(team_name, True, color)
        text_rect = team_text.get_rect(center=(x_offset + (self.screen.get_width() // 3) // 2, 60))  # Move team name down

        # Draw the team name
        self.screen.blit(team_text, text_rect)

        # Only draw player names and scores if there are players
        if players:
            # Sort players by score in descending order
            sorted_players = sorted(players, key=lambda player: player.score, reverse=True)

            # Draw player names and scores
            y_offset = 120  # More space between team name and player section
            for player in sorted_players:
                # Player name on the left
                player_name = self.font.render(player.name, True, color)
                self.screen.blit(player_name, (x_offset + 20, y_offset))

                # Player score on the right
                player_score = self.font.render(str(player.score), True, color)
                score_x = x_offset + (self.screen.get_width() // 3) - player_score.get_width() - 20
                self.screen.blit(player_score, (score_x, y_offset))

                y_offset += 40  # More space between player names

        # Draw team score at the bottom of the column (always displayed)
        team_score_font = pygame.font.Font(None, 48)
        team_score = self.scores[team_name]
        team_score_text = team_score_font.render(f"Score: {team_score}", True, color)
        team_score_rect = team_score_text.get_rect(center=(x_offset + (self.screen.get_width() // 3) // 2, self.screen.get_height() - 60))
        self.screen.blit(team_score_text, team_score_rect)

    def draw_timer(self, rect, remaining_time):
        timer_font = pygame.font.Font(None, 64)
        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)
        timer_text = timer_font.render(f"{minutes:02}:{seconds:02}", True, (255, 255, 255))  # White text
        text_rect = timer_text.get_rect(center=(rect.x + rect.width // 2, rect.y + rect.height // 2))
        self.screen.blit(timer_text, text_rect)

    def updateScore(self, team, player_index, points):
        if team == "Red Team":
            self.red_players[player_index].score += points
            self.scores["Red Team"] += points
        elif team == "Green Team":
            self.green_players[player_index].score += points
            self.scores["Green Team"] += points

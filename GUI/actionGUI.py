
import pygame
import time

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0  # Initialize score to zero

class Message:
    def __init__(self,type,team1,team2, name1, name2):
        self.type = type # True or false for base hit or hit 
        self.team1 = team1
        self.team2 = team2
        self.name1 = name1
        self.name2 = name2


class Message:
    def __init__(self,type,team1,team2, name1, name2):
        self.type = type # True or false for base hit or hit 
        self.team1 = team1
        self.team2 = team2
        self.name1 = name1
        self.name2 = name2


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

        # Draw text
        for i in range(len(self.readList)):
            y_location = screen_height * 5 // 6-i*32-25
            if((y_location) == 0):
                break
            
            img = self.fontText.render(self.readList[i], True, 'WHITE')
            self.screen.blit(img, (section_width+30, y_location))

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

    def updateScore(self, team, playerIndex, points):
        if team == "red":
            self.redPlayers[playerIndex].score += points
            self.scores["Red Team"] += points
        elif team == "green":
            self.greenPlayers[playerIndex].score += points
            self.scores["Green Team"] += points
    
    def fixMessagesScore(self):   
        for message in self.readList:  # Assuming `self.readList` contains messages like "11:12"
            try:
                # Split the message into two integers
                player1_id, player2_id = map(int, message.split(":"))

                # Find Player 1 (Shooter)
                player1 = next((p for p in self.redPlayers + self.greenPlayers if p.equipId == player1_id), None)

                # Find Player 2 (Target)
                player2 = next((p for p in self.redPlayers + self.greenPlayers if p.equipId == player2_id), None)

                # If either player is missing, continue
                if not player1 or not player2:
                    print(f"Warning: Could not find players for IDs {player1_id}, {player2_id}")
                    continue

                # Determine teams and names
                player1_name, player1_team = player1.name, player1.team
                player2_name, player2_team = player2.name, player2.team
                # Identify if this is a base hit (53 or 43)
                if player2_id in (53, 43):  
                    if not player1.hitBase:  # Check if player has hit the base before
                        if player1_team == "green" and player2_id == 53:
                            message = Message(True,player1_team,player2_team, player1_name, player2_name)
                            self.readList.append(message)
                            player1.name = "[B] " + player1.name  # Mark as base hit
                            player1.hitBase = True
                            self.updateScore(player1_team, player1_id, 100)
                        elif player1_team == "red" and player2_id == 43:
                            message = Message(True,player1_team,player2_team, player1_name, player2_name)
                            self.readList.append(message)
                            player1.name = "[B] " + player1.name  # Mark as base hit
                            player1.hitBase = True
                            self.updateScore(player1_team, player1_id, 100)
                        else:
                            print("error in base hits ")
                
                if player1_team == player2_team:
                    self.client.sendClientMessage(str(player1_id))
                    self.updateScore(player1_team, player1_id, -10)
                    message = Message(False,player1_team,player2_team, player1_name, player2_name)
                    self.readList.append(message)
                elif player1_team != player2_team:
                    message = Message(False,player1_team,player2_team, player1_name, player2_name)
                    self.readList.append(message)
                    self.client.sendClientMessage(str(player2_id))   
                    self.updateScore(player1_team, player1_id, 10)

            except ValueError:
                print(f"Invalid message format: {message}")

        #loop the array split into two values seperated by :
        #Find player with equipment ID first 
        # is the second string a 53 or 43 if so check which team player one is on add a [B] to Name and check if been base before 
        #Find playe with second hit 
        #Are they on same team 
            #if yes -10 transmit first 
            #if no +10 tramsit second 
        #print message to screen 
        
    
    def assignIDS(self):
        for player in self.redPlayers:
            player_id = self.nameConnect[player.name]  # Get the player's ID
            player.equipId = self.idConnectEquip[player_id]  # Assign the equipment ID

        # Assign IDs for Green Team
        for player in self.greenPlayers:
            player_id = self.nameConnect[player.name]
            player.equipId = self.idConnectEquip[player_id]


# TO DO 
# make winning team flash 

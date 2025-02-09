import pygame
import sys
import os
import psycopg2

# Add parent directory to system path for main.py import
sys.path.append(os.path.abspath('../'))
from main import getAspect

class TeamBoxUI:
    def __init__(self, screen, database):
        # Initialize screen and dimensions
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.database = database  # Store database connection
        
        # Load background image and adjust its aspect ratio
        self.bgImage = pygame.image.load('Photos/logo.jpg')
        self.bgX, self.bgY, self.scaledBgImage = getAspect(self.bgImage, self.screen)
        
        # Draw grayscale background once
        grayscaleBg = self.convertToGrayscale(self.scaledBgImage)
        self.screen.blit(grayscaleBg, (self.bgX, self.bgY))

        # Define colors
        self.colorWhite = (255, 255, 255)
        self.colorBlack = (0, 0, 0)
        self.colorActive = pygame.Color("cornsilk1")
        self.teamColors = [pygame.Color("red"), pygame.Color("green3")]

        # Define fonts
        self.fontTitle = pygame.font.SysFont("Corbel", 45, bold=True)
        self.fontButton = pygame.font.SysFont("Corbel", 35)
        self.fontText = pygame.font.SysFont("Corbel", 30)

        # Render labels
        self.labels = [
            self.fontTitle.render("Red Team", True, self.colorWhite),
            self.fontTitle.render("Green Team", True, self.colorWhite)
        ]
        self.instructions = self.fontText.render("Insert ID in the team box below", True, self.colorWhite)

        # Quit button
        self.textQuit = self.fontButton.render("Quit", True, self.colorWhite)

        # Define team box structure
        self.numTeams = 2
        self.numBoxesPerTeam = 15
        self.activeBoxes = [0, 0]  # Tracks number of active boxes per team
        self.playerBoxes = self.createBoxes()

        # Track active input boxes
        self.active = [[False] * self.numBoxesPerTeam for _ in range(self.numTeams)]
        
        # Store entered IDs & corresponding player names
        self.ids = [["" for _ in range(self.numBoxesPerTeam)] for _ in range(self.numTeams)]
        self.names = [["" for _ in range(self.numBoxesPerTeam)] for _ in range(self.numTeams)]

    def createBoxes(self):
        """Create input boxes, but only show one per team initially."""
        boxes = []
        spacing_x = self.width // 3  # Divide screen into three sections
        for teamIndex in range(self.numTeams):
            teamBoxes = []
            for i in range(self.numBoxesPerTeam):
                xPos = spacing_x * (teamIndex + 1) - 70  # Center boxes in each column
                yPos = 200 + 50 * i  # Stack boxes vertically
                rect = pygame.Rect(xPos, yPos, 140, 40)
                teamBoxes.append(rect)
            boxes.append(teamBoxes)
        return boxes

    def fetchPlayerName(self, player_id):
        """Retrieve player name from database using player ID."""
        try:
            conn = self.database.connect()  
            cursor = conn.cursor()
            cursor.execute("SELECT codename FROM players WHERE id = %s", (player_id,))
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else "Unknown Player"
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return "Error"

    def handleEvent(self, event):
        """Handle user input (mouse clicks and keyboard input)."""
        if event.type == pygame.QUIT:
            return "quit"

        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            
            # Check if quit button was clicked
            if (self.width - 150 <= mousePos[0] <= self.width - 10) and (self.height - 50 <= mousePos[1] <= self.height - 10):
                return "quit"

            # Check if text box was clicked
            for teamIndex in range(self.numTeams):
                for boxIndex in range(self.activeBoxes[teamIndex] + 1):
                    if self.playerBoxes[teamIndex][boxIndex].collidepoint(mousePos):
                        self.active = [[False] * self.numBoxesPerTeam for _ in range(self.numTeams)]
                        self.active[teamIndex][boxIndex] = True

        if event.type == pygame.KEYDOWN:
            for teamIndex in range(self.numTeams):
                for boxIndex in range(self.activeBoxes[teamIndex] + 1):
                    if self.active[teamIndex][boxIndex]:
                        if event.key == pygame.K_BACKSPACE:
                            self.ids[teamIndex][boxIndex] = self.ids[teamIndex][boxIndex][:-1]
                        elif event.key == pygame.K_RETURN:
                            # Fetch name from database and open a new box if limit isn't reached
                            player_id = self.ids[teamIndex][boxIndex]
                            self.names[teamIndex][boxIndex] = self.fetchPlayerName(player_id)
                            if self.activeBoxes[teamIndex] < self.numBoxesPerTeam - 1:
                                self.activeBoxes[teamIndex] += 1
                        else:
                            self.ids[teamIndex][boxIndex] += event.unicode

    def convertToGrayscale(self, image):
        """Convert image to grayscale."""
        grayscaleImage = image.copy()
        for x in range(grayscaleImage.get_width()):
            for y in range(grayscaleImage.get_height()):
                r, g, b, a = grayscaleImage.get_at((x, y))
                gray = int(0.299 * r + 0.587 * g + 0.114 * b)
                grayscaleImage.set_at((x, y), (gray, gray, gray, a))
        return grayscaleImage

    def draw(self):
        """Draw all UI elements."""
        mouse = pygame.mouse.get_pos()

        # Draw quit button
        quitRect = pygame.Rect(self.width - 150, self.height - 50, 140, 40)
        pygame.draw.rect(self.screen, (170, 170, 170) if quitRect.collidepoint(mouse) else (100, 100, 100), quitRect)
        self.screen.blit(self.textQuit, (self.width - 110, self.height - 50))

        # Draw team labels
        spacing_x = self.width // 3
        for i, label in enumerate(self.labels):
            self.screen.blit(label, (spacing_x * (i + 1) - label.get_width() // 2, 50))
            self.screen.blit(self.instructions, (spacing_x * (i + 1) - self.instructions.get_width() // 2, 120))

        # Draw input boxes
        for teamIndex in range(self.numTeams):
            for boxIndex in range(self.activeBoxes[teamIndex] + 1):
                box = self.playerBoxes[teamIndex][boxIndex]
                pygame.draw.rect(self.screen, self.colorActive if self.active[teamIndex][boxIndex] else self.teamColors[teamIndex], box)

                # Render input text
                text = self.ids[teamIndex][boxIndex]
                textSurf = self.fontText.render(text, True, self.colorBlack)
                self.screen.blit(textSurf, (box.x + 10, box.y + 5))

                # Render player name
                name = self.names[teamIndex][boxIndex]
                nameSurf = self.fontText.render(name, True, self.colorWhite)
                self.screen.blit(nameSurf, (box.x + 160, box.y + 5))

        pygame.display.update()

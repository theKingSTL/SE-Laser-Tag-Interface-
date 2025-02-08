import pygame
import sys
import os

# Add the parent directory to the system path to allow imports from main.py
sys.path.append(os.path.abspath('../'))
from main import getAspect

class TeamBoxUI:
    def __init__(self, screen):
        # Initialize screen and dimensions
        self.screen = screen
        self.width, self.height = screen.get_size()
        
        # Load background image and adjust its aspect ratio
        self.bgImage = pygame.image.load('Photos/logo.jpg')
        self.bgWidth, self.bgHeight = self.bgImage.get_size()
        self.bgX, self.bgY, self.scaledBgImage = getAspect(self.bgImage, self.screen)
        
        #draw the background so it only draws once
        grayscaleBg = self.convertToGrayscale(self.scaledBgImage)
        self.screen.blit(grayscaleBg, (self.bgX, self.bgY))

        # Define colors for UI elements
        self.colorWhite = (255, 255, 255)
        self.colorLight = (170, 170, 170)
        self.colorDark = (100, 100, 100)
        self.colorActive = pygame.Color("cornsilk1")
        self.colorBlack = (0, 0, 0)
        self.bgColor = (0, 0, 0)

        # Colors for passive team boxes
        self.teamPassiveColors = [
            pygame.Color("crimson"),
            pygame.Color("green3")
        ]

        # Define fonts for buttons and text
        self.fontButton = pygame.font.SysFont("Corbel", 35)
        self.fontText = pygame.font.SysFont("Corbel", 35)

        # Render quit button text
        self.textQuit = self.fontButton.render("Quit", True, self.colorWhite)

        # Define team and box structure
        self.numTeams = 2
        self.numBoxesPerTeam = 15
        self.playerBoxes = self.createBoxes()
        
        # Track which boxes are active (selected for input)
        self.active = [[False] * self.numBoxesPerTeam for _ in range(self.numTeams)]
        
        # Store text input for each box
        self.texts = [["" for _ in range(self.numBoxesPerTeam)] for _ in range(self.numTeams)]

    def createBoxes(self):
        """Create text input boxes for each team."""
        boxes = []
        for teamIndex in range(self.numTeams):
            teamBoxes = []
            for i in range(self.numBoxesPerTeam):
                xPos = 20 + teamIndex * 400  # Position boxes per team
                yPos = 20 + 40 * i  # Stack boxes vertically
                rect = pygame.Rect(xPos, yPos, 140, 35)
                teamBoxes.append(rect)
            boxes.append(teamBoxes)
        return boxes

    def getMaxTextWidth(self):
        """Calculate the maximum text width among all boxes for uniform sizing."""
        return max((self.fontText.size(text)[0] for team in self.texts for text in team), default=100) + 20

    def handleEvent(self, event):
        """Handle user input events including mouse clicks and keyboard input."""
        if event.type == pygame.QUIT:
            return "quit"
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            
            # Check if a text box was clicked
            for teamIndex in range(self.numTeams):
                for boxIndex, box in enumerate(self.playerBoxes[teamIndex]):
                    if box.collidepoint(mousePos):
                        # Reset active states and set the clicked box as active
                        self.active = [[False] * self.numBoxesPerTeam for _ in range(self.numTeams)]
                        self.active[teamIndex][boxIndex] = True
            
            # Check if the quit button was clicked
            if (self.width - 150 <= mousePos[0] <= self.width - 10) and (self.height - 50 <= mousePos[1] <= self.height - 10):
                return "quit"
        
        if event.type == pygame.KEYDOWN:
            # Handle text input for the active text box
            for teamIndex in range(self.numTeams):
                for boxIndex in range(self.numBoxesPerTeam):
                    if self.active[teamIndex][boxIndex]:
                        if event.key == pygame.K_BACKSPACE:
                            self.texts[teamIndex][boxIndex] = self.texts[teamIndex][boxIndex][:-1]  # Remove last character
                        else:
                            self.texts[teamIndex][boxIndex] += event.unicode  # Append typed character
            
            # Allow quitting with F4 key
            if event.key == pygame.K_F4:
                return "quit"

    def convertToGrayscale(self, image):
        """Convert an image to grayscale by applying a luminance filter."""
        grayscaleImage = image.copy()
        for x in range(grayscaleImage.get_width()):
            for y in range(grayscaleImage.get_height()):
                r, g, b, a = grayscaleImage.get_at((x, y))
                gray = int(0.299 * r + 0.587 * g + 0.114 * b)  # Convert to grayscale
                grayscaleImage.set_at((x, y), (gray, gray, gray, a))
        return grayscaleImage

    def draw(self):
        """Draw all UI elements on the screen."""
        
        mouse = pygame.mouse.get_pos()
        
        # Draw the quit button
        quitRect = pygame.Rect(self.width - 150, self.height - 50, 140, 40)
        pygame.draw.rect(self.screen, self.colorLight if quitRect.collidepoint(mouse) else self.colorDark, quitRect)
        self.screen.blit(self.textQuit, (self.width - 110, self.height - 50))
        
        # Ensure all text boxes have the same width
        commonWidth = self.getMaxTextWidth()
        
        # Draw text input boxes and their contents
        for teamIndex in range(self.numTeams):
            for boxIndex, box in enumerate(self.playerBoxes[teamIndex]):
                box.w = commonWidth  # Set width based on max text width
                
                # Highlight active box, otherwise use team color
                color = self.colorActive if self.active[teamIndex][boxIndex] else self.teamPassiveColors[teamIndex]
                pygame.draw.rect(self.screen, color, box)

                # Render and center text inside the box
                textSurf = self.fontText.render(self.texts[teamIndex][boxIndex], True, self.colorBlack)
                textX = box.x + (box.w - textSurf.get_width()) // 2
                textY = box.y + (box.h - textSurf.get_height()) // 2
                self.screen.blit(textSurf, (textX, textY))
        
        pygame.display.update()

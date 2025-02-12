import pygame
import sys
import os
import psycopg2

#adding parent directory to path so the getAspect method can be used from main 
sys.path.append(os.path.abspath('../'))
from main import getAspect

#class for player selection UI 
class TeamBoxUI:
    def __init__(self, screen, database):
        #take parameters and make screen and database 
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.database = database  
        #background image being set to same as splash screen with getAspect
        self.bgImage = pygame.image.load('Photos/logo2.jpg')
        self.bgX, self.bgY, self.scaledBgImage = getAspect(self.bgImage, self.screen)
        #now set background to black and white and draw
        grayscaleBg = self.convertToGrayscale(self.scaledBgImage)
        self.screen.blit(grayscaleBg, (self.bgX, self.bgY))
        #make a couple colors do we need them as members of class?
        self.colorWhite = (255, 255, 255)
        self.colorBlack = (0, 0, 0)
        self.colorActive = pygame.Color("cornsilk1")
        self.teamColors = [pygame.Color("red"), pygame.Color("green3")]
        #fonts to use 
        self.fontTitle = pygame.font.SysFont("Corbel", 80, bold=False)
        self.fontButton = pygame.font.SysFont("Corbel", 35)
        self.fontText = pygame.font.SysFont("Corbel", 40)

        #create the top labels - green and red team 
        self.labels = [
            #render (name, anti-aliasing, color)
            self.fontTitle.render("Red Team", True, self.teamColors[0]),
            self.fontTitle.render("Green Team", True, self.teamColors[1])
        ]
        
        #the instruction to be set below labels 
        self.instructions = self.fontText.render("Type Player IDs into their respective team boxes below. (IDs are 6 digits)", True, self.colorWhite)

        #quit button (name, anti-aliasing, color)
        self.quit = self.fontButton.render("Quit", True, self.colorWhite)
        #button for clearn and change address 
        self.clear = self.fontButton.render("Clear Game", True, self.colorWhite)
        self.textQuit = self.fontButton.render("Change Address", True, self.colorWhite)

        #creates params for the boxs for teams 
        self.numTeams = 2
        self.numBoxesPerTeam = 15
        #used to track how many active boxes for display
        #this starts if with one in use for some reason 
        #self.activeBoxes = [0, 0]
        self.playerBoxes = self.createBoxes() #will return the player boxes - two lists of 15 boxs 

        #a list of a list of bools - init to all False no active boxes 
        # in our case its two lists full of 15 bools for which boxes are active for display reasons 
        #self.active = [[False] * self.numBoxesPerTeam for _ in range(self.numTeams)]
        
        #same idea as above for the ids and names enter empty strings 
        self.ids = [["" for _ in range(self.numBoxesPerTeam)] for _ in range(self.numTeams)]
        self.names = [["" for _ in range(self.numBoxesPerTeam)] for _ in range(self.numTeams)]

    #will return a list of pygame rects 
    def createBoxes(self):
        boxes = []  
        for teamIndex in range(self.numTeams):
            teamBoxes = []
            yInc = 0
            for i in range(self.numBoxesPerTeam):
                if i%2 == 0:
                    xInc= 100
                    yInc = yInc + 56.65
                else:
                    xInc = 315
                
                xPos =  (teamIndex*640) + xInc
                yPos = 160 + yInc
                rect = pygame.Rect(xPos, yPos, 185, 40)
                teamBoxes.append(rect)
            boxes.append(teamBoxes)
        return boxes

    #will look for player id in database then return either none flag or codename 
    def fetchPlayerName(self, player_id):
        try:
            conn = self.database.connect()  
            cursor = conn.cursor()
            cursor.execute("SELECT codename FROM players WHERE id = %s", (player_id,))
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else None
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return "Error"

    def handleEvent(self, event):
        if event.type == pygame.QUIT:
            return "quit"

        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            
            # Check if quit button was clicked
            if (self.width - 150 <= mousePos[0] <= self.width - 10) and (self.height - 50 <= mousePos[1] <= self.height - 10):
                return "quit"
            
            # Check if text box was clicked
            for teamIndex in range(self.numTeams):
                for boxIndex, box in enumerate(self.playerBoxes[teamIndex]):
                    if box.collidepoint(mousePos):
                        self.focusedBox = (teamIndex, boxIndex)
                        return

        if event.type == pygame.KEYDOWN and hasattr(self, 'focusedBox'):
            teamIndex, boxIndex = self.focusedBox
            
            if event.key == pygame.K_BACKSPACE:
                self.ids[teamIndex][boxIndex] = self.ids[teamIndex][boxIndex][:-1]
            elif event.key == pygame.K_RETURN:
                player_id = self.ids[teamIndex][boxIndex]
                self.names[teamIndex][boxIndex] = self.fetchPlayerName(player_id)
                self.focusedBox = None  # Remove focus after pressing enter
            else:
                self.ids[teamIndex][boxIndex] += event.unicode

    #converts the image to grey scale 
    def convertToGrayscale(self, image):
        grayscaleImage = image.copy()
        
        for x in range(grayscaleImage.get_width()):
            for y in range(grayscaleImage.get_height()):
                r, g, b, a = grayscaleImage.get_at((x, y))
                
                # Convert to grayscale
                gray = int(0.299 * r + 0.587 * g + 0.114 * b)
                
                # Reduce brightness by multiplying (e.g., 0.7 for a dimmed effect)
                dimFactor = 0.7  # Adjust this between 0.5 - 0.9 for different dim levels
                gray = int(gray * dimFactor)
                
                # Set pixel with new dimmed grayscale value
                grayscaleImage.set_at((x, y), (gray, gray, gray, a))

        return grayscaleImage

    def draw(self):
        mouse = pygame.mouse.get_pos()

        # Draw quit button
        quitRect = pygame.Rect(890, self.height - 100, 100, 50)
        pygame.draw.rect(self.screen, 'cornsilk4', quitRect)
        quit_text_rect = self.quit.get_rect(center=quitRect.center)
        self.screen.blit(self.quit, quit_text_rect)

        # Draw reset button
        resetRect = pygame.Rect(self.width/2 - 110, self.height - 100, 175, 50)
        pygame.draw.rect(self.screen, 'cornsilk4', resetRect)
        reset_text_rect = self.clear.get_rect(center=resetRect.center)
        self.screen.blit(self.clear, reset_text_rect)

        # Draw change network button
        changeRect = pygame.Rect(180, self.height - 100, 250, 50)
        pygame.draw.rect(self.screen, 'cornsilk4', changeRect)
        change_text_rect = self.textQuit.get_rect(center=changeRect.center)
        self.screen.blit(self.textQuit, change_text_rect)

        # Assuming self.fontTitle is already set up like this:
        # self.fontTitle = pygame.font.Font(None, 48)  # Adjust font size as needed
        # Spacing and positioning
        spacingX = 640
        textColor = (255, 255, 255)  # White text for general readability

        # Calculate the position to center the text for each team
        redTeamText = self.labels[0]  # Red Team text
        greenTeamText = self.labels[1]  # Green Team text

        # Get the rects for each text to center them
        redTeamRect = redTeamText.get_rect(center=(300, 70))  # Adjusted y position by 40 pixels
        greenTeamRect = greenTeamText.get_rect(center=(300 + 640, 70))  # Adjusted y position by 40 pixels

        # Draw the team names with proper positioning
        self.screen.blit(redTeamText, redTeamRect)
        self.screen.blit(greenTeamText, greenTeamRect)

        # Instructions rendering
        instructionsFont = pygame.font.Font(None, 36)  # Smaller font for instructions
        instructionsText = self.instructions
        # Adjust y position of instructions to 150 (down 40 pixels)
        instructionsRect = instructionsText.get_rect(center=(self.width // 2, 150))
        self.screen.blit(instructionsText, instructionsRect)



        # Draw input boxes
        for teamIndex in range(self.numTeams):
            for boxIndex in range(self.numBoxesPerTeam):
                box = self.playerBoxes[teamIndex][boxIndex]
                pygame.draw.rect(self.screen, self.teamColors[teamIndex], box)

                # Render input text
                text = self.ids[teamIndex][boxIndex]
                textSurf = self.fontText.render(text, True, self.colorBlack)
                self.screen.blit(textSurf, (box.x + 10, box.y + 5))

                # Render player name
                name = self.names[teamIndex][boxIndex]
                nameSurf = self.fontText.render(name, True, self.colorWhite)
                self.screen.blit(nameSurf, (box.x + 10, box.y + 5))

        pygame.display.update()
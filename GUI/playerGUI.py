import pygame
import sys
import os
import psycopg2
import time 
import ipaddress

server_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Server"))

# Add the Server directory to sys.path
sys.path.append(server_dir)

# Now you can import the module from the Server director
from .updClient import *
from .updServer import *
#adding parent directory to path so the getAspect method can be used from main 

def isValidIp(ip):
    try:
        ipaddress.ip_address(ip)  # This will raise ValueError if the IP is invalid
        return True
    except ValueError:
        return False 

def getAspect(image, screen):
    img_width, img_height = image.get_size()
    
    # Screen dimensions
    screen_width, screen_height = screen.get_size()

    # Calculate the best fit while maintaining aspect ratio
    img_ratio = img_width / img_height
    screen_ratio = screen_width / screen_height

    if img_ratio > screen_ratio:
        # Image is wider than screen, scale based on width
        new_width = screen_width
        new_height = int(screen_width / img_ratio)
    else:
        # Image is taller than screen, scale based on height
        new_height = screen_height
        new_width = int(screen_height * img_ratio)
    
    # Scale the image while keeping aspect ratio
    scaledImage = pygame.transform.scale(image, (new_width, new_height))

    # Calculate position to center the image
    xPos = (screen_width - new_width) // 2
    yPos = (screen_height - new_height) // 2

    return xPos, yPos, scaledImage

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
        self.grayscaleBg = self.convertToGrayscale(self.scaledBgImage)
        self.screen.blit(self.grayscaleBg, (self.bgX, self.bgY))
        #make a couple colors do we need them as members of class?
        self.colorWhite = (255, 255, 255)
        self.colorBlack = (0, 0, 0)
        self.colorActive = pygame.Color("cornsilk1")
        self.teamColors = [pygame.Color("red"), pygame.Color("green3")]
        #fonts to use 
        self.fontTitle = pygame.font.SysFont("Corbel", 80, bold=False)
        self.fontButton = pygame.font.SysFont("Corbel", 35)
        self.fontText = pygame.font.SysFont("Corbel", 40)
        self.fontID = pygame.font.SysFont("Courier", 30, True)  
        self.fontUsername = pygame.font.SysFont("Courier", 25, True)  

        #create the top labels - green and red team 
        self.labels = [
            #render (name, anti-aliasing, color)
            self.fontTitle.render("Red Team", True, self.teamColors[0]),
            self.fontTitle.render("Green Team", True, self.teamColors[1])
        ]
        
        #the instruction to be set below labels 
        self.instructions = self.fontText.render("Type Player IDs into their respective team boxes below. (IDs are 6 digits)", True, self.colorWhite)

        #used for the box cursor 
        self.focusedBox = None  # Track the focused box
        self.cursorVisible = False  # Track cursor visibility
        self.lastCursorToggle = time.time()  # Track the last time the cursor toggled
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
        #will create the list for equipment id and id relation
        self.data: dict[int, int] = {}
        #connect id to name 
        self.nameConnect: dict[str,int] = {}

        #client UDP socket  
        self.Client = ClientSocket()
        self.server = ServerSocket()
        #start that thing 
        self.server.startServer()
    #will return a list of pygame rects 
    def createBoxes(self):
        boxes = []  
        for teamIndex in range(self.numTeams):
            teamBoxes = []
            yInc = 0
            for i in range(self.numBoxesPerTeam):
                if i%2 == 0:
                    xInc= 75
                    yInc = yInc + 56.65
                else:
                    xInc = 315
                
                xPos =  (teamIndex*640) + xInc
                yPos = 160 + yInc
                rect = pygame.Rect(xPos, yPos, 210, 40)
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
        
            #if id doesnt exist need to pop up box and state enter new id 
    def handleEvent(self, event):
        if event.type == pygame.QUIT:
            return "quit"

        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()

            # Check if quit button was clicked
            quitRect = pygame.Rect(890, self.height - 100, 100, 50)
            if quitRect.collidepoint(mousePos):
                self.server.stopServer()
                return "quit"  # Quit the application

            # Check if clear game button was clicked
            clearRect = pygame.Rect(self.width / 2 - 110, self.height - 100, 175, 100)
            if clearRect.collidepoint(mousePos):
                # Clear all IDs and usernames
                self.ids = [["" for _ in range(self.numBoxesPerTeam)] for _ in range(self.numTeams)]
                self.names = [["" for _ in range(self.numBoxesPerTeam)] for _ in range(self.numTeams)]
                self.nameConnect.clear()
                self.data.clear()
                self.focusedBox = None  # Remove focus from any box
                return

            # Check if change address button was clicked
            changeRect = pygame.Rect(180, self.height - 100, 250, 50)
            if changeRect.collidepoint(mousePos):
                new_ip = self.createNewIP()  # Call without player_id
                self.server.change_network(new_ip)
                self.Client.changeNetwork(new_ip)
                print(f"New server IP: {new_ip}")  # Debugging output
                return

            # Check if text box was clicked
            for teamIndex in range(self.numTeams):
                for boxIndex, box in enumerate(self.playerBoxes[teamIndex]):
                    if box.collidepoint(mousePos):
                        # If the box already has a name, clear it
                        if self.names[teamIndex][boxIndex]:
                            val = self.nameConnect[self.names[teamIndex][boxIndex]]
                            del self.nameConnect[self.names[teamIndex][boxIndex]]
                            del self.data[val]
                            self.ids[teamIndex][boxIndex] = ""
                            self.names[teamIndex][boxIndex] = ""
                        self.focusedBox = (teamIndex, boxIndex)
                        return  # Stop checking once a box is focused

        # Ensure event is a key press and a box is selected
        if event.type == pygame.KEYDOWN and self.focusedBox is not None:
            teamIndex, boxIndex = self.focusedBox

            if event.key == pygame.K_BACKSPACE:
                self.ids[teamIndex][boxIndex] = self.ids[teamIndex][boxIndex][:-1]
            elif event.key == pygame.K_RETURN:
                player_id = self.ids[teamIndex][boxIndex]
                if len(player_id) != 6 or not player_id.isdigit():
                    # Display error message for invalid ID format
                    self.showErrorMessage("ID must be exactly 6 digits.", "top")
                else:
                    userName = self.fetchPlayerName(player_id)
                    if userName is None:
                        userName, equipID = self.createNewUsername(player_id)
                    else:
                        equipID = self.createEquipmentID()
                    self.names[teamIndex][boxIndex] = userName
                    self.Client.sendClientMessage(str(equipID))
                    self.data[self.ids[teamIndex][boxIndex]] = equipID
                    self.nameConnect[userName] = self.ids[teamIndex][boxIndex]
                    self.ids[teamIndex][boxIndex] = ""  # Clear the ID box

                    # Automatically focus the next box in the same team
                    nextBoxIndex = boxIndex + 1
                    while nextBoxIndex < self.numBoxesPerTeam:
                        if not self.names[teamIndex][nextBoxIndex]:  # Check if the box is empty
                            self.focusedBox = (teamIndex, nextBoxIndex)  # Move focus to the next empty box
                            break
                        nextBoxIndex += 1
                    else:
                        self.focusedBox = None  # No more empty boxes in this team
            elif event.key == pygame.K_F5:
                # Clear all IDs and usernames
                self.ids = [["" for _ in range(self.numBoxesPerTeam)] for _ in range(self.numTeams)]
                self.names = [["" for _ in range(self.numBoxesPerTeam)] for _ in range(self.numTeams)]
                self.nameConnect.clear()
                self.data.clear()
                self.focusedBox = None  # Remove focus from any box
            else:
                # Allow limit to 6 characters
                if len(self.ids[teamIndex][boxIndex]) < 6:
                    self.ids[teamIndex][boxIndex] += event.unicode


    def showErrorMessage(self, message, location):
        if location == "top":
            x=self.width // 2.05
            y=self.height - 610
        else: 
            x = self.width // 2
            y = self.height // 2 + 50
        errorSurface = self.fontText.render(message, True, (255, 0, 0))  # Red text
        errorRect = errorSurface.get_rect(center=(x,y))
        
        # Draw error message
        self.screen.blit(errorSurface, errorRect)
        pygame.display.update()

        # Wait for user input (click or key press) to remove the message
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:  # User clicked or typed
                    running = False
                    
                    # Redraw only the part of the screen where the error message was
                    self.redrawAffectedArea(errorRect)
                    pygame.display.update()

    def redrawAffectedArea(self, rect):
        # Replace with how you normally draw your game screen
        background = pygame.Surface((rect.width, rect.height))
        background.fill((0, 0, 0))  # Assuming a black background; change if needed
        self.screen.blit(background, rect.topleft)

        pygame.display.update(rect)  # Update only that region

    def createNewUsername(self, player_id):
        # Save the current screen state (background and UI elements)
        saved_screen = self.screen.copy()

        # Define the input box for the pop-up
        inputBox = pygame.Rect(self.width // 2 - 150, self.height // 2 - 25, 300, 50)
        inputText = ""
        inputActive = True
        cursorVisible = True  # Tracks cursor visibility
        lastCursorToggle = time.time()  # Tracks the last time the cursor was toggled

        while inputActive:
            currentTime = time.time()

            # Toggle cursor visibility every 500ms
            if currentTime - lastCursorToggle > 0.5:
                cursorVisible = not cursorVisible
                lastCursorToggle = currentTime

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Validate input before proceeding
                        inputTextStripped = inputText.strip()  # Remove leading/trailing spaces

                        # Check if input is empty or only spaces
                        if len(inputTextStripped) == 0:
                            self.showErrorMessage("Username cannot be empty or only spaces. Please retype.", "bottom")
                            inputText = ""  # Clear the input box
                            continue  # Skip the rest and force retype

                        # Check if username already exists in the database
                        conn = self.database.connect()
                        cursor = conn.cursor()
                        cursor.execute("SELECT 1 FROM players WHERE codename = %s", (inputTextStripped,))
                        existingUser = cursor.fetchone()
                        conn.close()

                        if existingUser:
                            self.showErrorMessage("Username already exists. Please choose a different one.", "bottom")
                            inputText = ""  # Clear the input box
                            continue  # Skip the rest and force retype

                        # If input is valid, exit the loop
                        inputActive = False

                    elif event.key == pygame.K_BACKSPACE:
                        inputText = inputText[:-1]  # Remove the last character
                    else:
                        if len(inputText) < 13:  # Limit username to 13 characters
                            inputText += event.unicode  # Add the typed character

                elif event.type == pygame.QUIT:
                    self.screen.blit(saved_screen, (0, 0))
                    pygame.display.update()
                    return "", None  # Default username if the user closes the window

            # Draw the pop-up background (Photos/logo2.jpg)
            self.screen.blit(self.grayscaleBg, (self.bgX, self.bgY))

            # Draw a semi-transparent overlay (optional, to dim the background further)
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))  # Black with 128 alpha for slight dimming
            self.screen.blit(overlay, (0, 0))

            # Draw the input box
            pygame.draw.rect(self.screen, (255, 255, 255), inputBox, border_radius=10)  # White rounded box
            pygame.draw.rect(self.screen, (0, 0, 0), inputBox, 2, border_radius=10)  # Black outline

            # Render the instruction text
            textSurface = self.fontText.render(f"Enter new username for new ID: {player_id} (13 chars max):", True, (255, 255, 255))
            textRect = textSurface.get_rect(center=(self.width // 2, self.height // 2 - 50))
            self.screen.blit(textSurface, textRect)

            # Render the input text inside the box
            inputSurface = self.fontText.render(inputText, True, (0, 0, 0))
            self.screen.blit(inputSurface, (inputBox.x + 5, inputBox.y + 7.5))

            # Draw the cursor if it's visible
            if cursorVisible:
                cursorX = inputBox.x + 10 + inputSurface.get_width()  # Position cursor at the end of the text
                pygame.draw.line(self.screen, (0, 0, 0), (cursorX, inputBox.y + 5), (cursorX, inputBox.y + inputBox.height - 5))

            pygame.display.update()  # Refresh the screen

        # Restore the original screen state (remove the pop-up)
        equipID = self.createEquipmentID()
        self.screen.blit(saved_screen, (0, 0))
        pygame.display.update()

        # Add the new username and ID to the database (if input is provided)
        inputTextStripped = inputText.strip()  # Ensure no leading/trailing spaces
        if inputTextStripped:
            try:
                conn = self.database.connect()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO players (id, codename) VALUES (%s, %s)", (player_id, inputTextStripped))
                conn.commit()
                conn.close()
            except psycopg2.Error as e:
                print(f"Database error: {e}")
                return "", None  # Default username if database insertion fails
            return inputTextStripped, equipID
        else:
            return "", None  # Default username if no input is provided

    def createNewIP(self):
        saved_screen = self.screen.copy()
        inputBox = pygame.Rect(self.width // 2 - 150, self.height // 2 - 25, 300, 50)
        inputText = ""
        inputActive = True
        cursorVisible = True
        lastCursorToggle = time.time()

        # Error message variables
        showError = False
        showError2 = False
        showInvalidIPError = False  # New error for invalid IP
        errorStartTime = 0  # Tracks when the error message was first displayed

        while inputActive:
            currentTime = time.time()
            if currentTime - lastCursorToggle > 0.5:
                cursorVisible = not cursorVisible
                lastCursorToggle = currentTime

            mousePos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if len(inputText) <= 18 and len(inputText) >= 1:  # Validate input length
                            if isValidIp(inputText):  # Validate the IP address
                                inputActive = False
                            else:
                                # Show error message for invalid IP
                                showInvalidIPError = True
                                errorStartTime = currentTime
                                inputText = ""  # Clear the input for a new attempt
                        elif len(inputText) <= 1:
                            showError2 = True
                            errorStartTime = currentTime
                        else:
                            # Show error message if input exceeds 18 characters
                            showError = True
                            errorStartTime = currentTime
                    elif event.key == pygame.K_BACKSPACE:
                        inputText = inputText[:-1]
                        showError = False  # Hide error message when user starts typing
                        showInvalidIPError = False  # Hide invalid IP error as well
                    else:
                        if len(inputText) < 18:  # Limit input to 18 characters
                            inputText += event.unicode
                        else:
                            # Show error message if input exceeds 18 characters
                            showError = True
                            errorStartTime = currentTime
                elif event.type == pygame.QUIT:
                    self.screen.blit(saved_screen, (0, 0))
                    pygame.display.update()
                    return "127.0.0.1"  # Default IP on quit
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    changeRect = pygame.Rect(180, self.height - 100, 250, 50)
                    if changeRect.collidepoint(mousePos):
                        return self.createNewIP()

            # Draw the pop-up background
            self.screen.blit(self.grayscaleBg, (self.bgX, self.bgY))
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            self.screen.blit(overlay, (0, 0))

            # Draw the input box
            pygame.draw.rect(self.screen, (255, 255, 255), inputBox, border_radius=10)
            pygame.draw.rect(self.screen, (0, 0, 0), inputBox, 2, border_radius=10)

            # Render the instruction text
            textSurface = self.fontText.render("Enter new IP for server (18 chars max):", True, (255, 255, 255))
            textRect = textSurface.get_rect(center=(self.width // 2, self.height // 2 - 50))
            self.screen.blit(textSurface, textRect)

            # Render the input text inside the box
            inputSurface = self.fontText.render(inputText, True, (0, 0, 0))
            self.screen.blit(inputSurface, (inputBox.x + 5, inputBox.y + 7.5))

            # Draw the cursor if it's visible
            if cursorVisible:
                cursorX = inputBox.x + 10 + inputSurface.get_width()
                pygame.draw.line(self.screen, (0, 0, 0), (cursorX, inputBox.y + 5), (cursorX, inputBox.y + inputBox.height - 5))

            # Display error message if input exceeds 18 characters and within the 3-second window
            if showError and (currentTime - errorStartTime <= 3):
                errorSurface = self.fontText.render("Error: IP must be 18 characters or less.", True, (255, 0, 0))
                errorRect = errorSurface.get_rect(center=(self.width // 2, self.height // 2 + 50))
                self.screen.blit(errorSurface, errorRect)
            else:
                showError = False  # Hide error message after 3 seconds

            # Display error message if input is too short and within the 3-second window
            if showError2 and (currentTime - errorStartTime <= 3):
                errorSurface = self.fontText.render("Error: IP must be at least 1 character.", True, (255, 0, 0))
                errorRect = errorSurface.get_rect(center=(self.width // 2, self.height // 2 + 50))
                self.screen.blit(errorSurface, errorRect)
            else:
                showError2 = False  # Hide error message after 3 seconds

            # Display error message if IP is invalid and within the 3-second window
            if showInvalidIPError and (currentTime - errorStartTime <= 3):
                errorSurface = self.fontText.render("Error: Invalid IP address. Please enter a valid IP.", True, (255, 0, 0))
                errorRect = errorSurface.get_rect(center=(self.width // 2, self.height // 2 + 50))
                self.screen.blit(errorSurface, errorRect)
            else:
                showInvalidIPError = False  # Hide error message after 3 seconds

            pygame.display.update()

        # Restore the original screen state (remove the pop-up)
        self.screen.blit(saved_screen, (0, 0))
        pygame.display.update()

        # Return the valid IP or a default value
        return inputText if inputText else "New_IP"
    def createEquipmentID(self):
        # Save the current screen state (background and UI elements)
        saved_screen = self.screen.copy()

        # Define the input box for the pop-up
        inputBox = pygame.Rect(self.width // 2 - 150, self.height // 2 - 25, 300, 50)
        inputText = ""
        inputActive = True
        lastCursorToggle = time.time()  # Tracks the last time the cursor was toggled

        # Error message variables
        showError = False
        errorStartTime = 0  # Tracks when the error message was first displayed

        while inputActive:
            currentTime = time.time()
            cursorVisible = int(currentTime * 2) % 2 == 0  # Toggle cursor every 500ms

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Validate input when Enter is pressed
                        if len(inputText) == 2 and inputText.isdigit():  # Check for exactly 7 digits
                            inputActive = False  # Exit input loop if valid
                        else:
                            # Show error message and reset input
                            showError = True
                            errorStartTime = currentTime  # Start the error message timer
                            inputText = ""  # Clear input for retry
                    elif event.key == pygame.K_BACKSPACE:
                        inputText = inputText[:-1]  # Remove the last character
                        showError = False  # Hide error message when user starts typing
                    else:
                        # Allow only numeric input and limit to 7 characters
                        if len(inputText) < 2:
                            inputText += event.unicode  # Add the typed character
                            showError = False  # Hide error message when user starts typing
                elif event.type == pygame.QUIT:
                    self.screen.blit(saved_screen, (0, 0))
                    pygame.display.update()
                    return None

            # Draw the pop-up background (Photos/logo2.jpg)
            self.screen.blit(self.grayscaleBg, (self.bgX, self.bgY))

            # Draw a semi-transparent overlay (optional, to dim the background further)
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))  # Black with 128 alpha for slight dimming
            self.screen.blit(overlay, (0, 0))

            # Draw the input box
            pygame.draw.rect(self.screen, (255, 255, 255), inputBox, border_radius=10)  # White rounded box
            pygame.draw.rect(self.screen, (0, 0, 0), inputBox, 2, border_radius=10)  # Black outline

            # Render the instruction text
            textSurface = self.fontText.render("Enter Equipment ID (2 digits):", True, (255, 255, 255))
            textRect = textSurface.get_rect(center=(self.width // 2, self.height // 2 - 50))
            self.screen.blit(textSurface, textRect)

            # Render the input text inside the box
            inputSurface = self.fontText.render(inputText, True, (0, 0, 0))
            self.screen.blit(inputSurface, (inputBox.x + 5, inputBox.y + 7.5))

            # Draw the cursor if it's visible
            if cursorVisible:
                cursorX = inputBox.x + 10 + inputSurface.get_width()  # Position cursor at the end of the text
                pygame.draw.line(self.screen, (0, 0, 0), (cursorX, inputBox.y + 5), (cursorX, inputBox.y + inputBox.height - 5))

            # Display error message if input is invalid and within the 3-second window
            if showError and (currentTime - errorStartTime <= 3):
                errorSurface = self.fontText.render("Error: Please enter exactly 2 digits.", True, (255, 0, 0))
                errorRect = errorSurface.get_rect(center=(self.width // 2, self.height // 2 + 50))
                self.screen.blit(errorSurface, errorRect)
            else:
                showError = False  # Hide error message after 3 seconds

            pygame.display.update()  # Refresh the screen

        # Restore the original screen state (remove the pop-up)
        self.screen.blit(saved_screen, (0, 0))
        pygame.display.update()

        # Return the valid equipment ID
        return inputText
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

        # Draw quit button with hover effect
        quitRect = pygame.Rect(890, self.height - 100, 100, 50)
        if quitRect.collidepoint(mouse):
            pygame.draw.rect(self.screen, 'cornsilk3', quitRect)  # Lighter color when hovered
        else:
            pygame.draw.rect(self.screen, 'cornsilk4', quitRect)
        quit_text_rect = self.quit.get_rect(center=quitRect.center)
        self.screen.blit(self.quit, quit_text_rect)

        # Draw reset button with hover effect
        resetRect = pygame.Rect(self.width / 2 - 110, self.height - 100, 175, 100)
        if resetRect.collidepoint(mouse):
            pygame.draw.rect(self.screen, 'cornsilk3', resetRect)  # Lighter color when hovered
        else:
            pygame.draw.rect(self.screen, 'cornsilk4', resetRect)

        # Render the main text ("Clear Game") and center it in the top half of the button
        clear_text = self.fontButton.render("Clear Game", True, (255,255,255))  # Black text
        clear_text_rect = clear_text.get_rect(center=(resetRect.centerx, resetRect.centery - resetRect.height // 4))  # Top half
        self.screen.blit(clear_text, clear_text_rect)

        # Render the secondary text ("[F5]") and center it in the bottom half of the button
        f5_text = self.fontButton.render("[F5]", True, (255, 255, 255))  # Black text
        f5_text_rect = f5_text.get_rect(center=(resetRect.centerx, resetRect.centery + resetRect.height // 4))  # Bottom half
        self.screen.blit(f5_text, f5_text_rect)
        self.screen.blit(f5_text, f5_text_rect)

        # Draw change network button with hover effect
        changeRect = pygame.Rect(180, self.height - 100, 250, 50)
        if changeRect.collidepoint(mouse):
            pygame.draw.rect(self.screen, 'cornsilk3', changeRect)  # Lighter color when hovered
        else:
            pygame.draw.rect(self.screen, 'cornsilk4', changeRect)
        change_text_rect = self.textQuit.get_rect(center=changeRect.center)
        self.screen.blit(self.textQuit, change_text_rect)

        # Assuming self.fontTitle is already set up like this:
        # self.fontTitle = pygame.font.Font(None, 48)  # Adjust font size as needed
        # Spacing and positioning

        # Calculate the position to center the text for each team
        redTeamText = self.labels[0]  # Red Team text
        greenTeamText = self.labels[1]  # Green Team text

        # Get the rects for each text to center them
        redTeamRect = redTeamText.get_rect(center=(300, 70))  # Adjusted y position by 40 pixels
        greenTeamRect = greenTeamText.get_rect(center=(300 + 640, 70))  # Adjusted y position by 40 pixels

        # Draw the team names with proper positioning
        self.screen.blit(redTeamText, redTeamRect)
        self.screen.blit(greenTeamText, greenTeamRect)

        # Adjust y position of instructions to 150 (down 40 pixels)
        instructionsRect = self.instructions.get_rect(center=(self.width // 2, 150))
        self.screen.blit(self.instructions, instructionsRect)

        # Draw input boxes
        for teamIndex in range(self.numTeams):
            for boxIndex in range(self.numBoxesPerTeam):
                box = self.playerBoxes[teamIndex][boxIndex]
                pygame.draw.rect(self.screen, self.teamColors[teamIndex], box)

                # Render input text
                text = self.ids[teamIndex][boxIndex]
                textSurf = self.fontID.render(text, True, self.colorWhite)
                self.screen.blit(textSurf, (box.x + 5, box.y + 5))

                # Render player name
                name = self.names[teamIndex][boxIndex]
                nameSurf = self.fontUsername.render(name, True, self.colorWhite)
                self.screen.blit(nameSurf,(box.x + 5, box.y + 7.5))

        #draw cursor in the focused box
        if hasattr(self, 'focusedBox') and self.focusedBox is not None:
            teamIndex, boxIndex = self.focusedBox
            box = self.playerBoxes[teamIndex][boxIndex]

            # Toggle cursor visibility every 500ms
            if time.time() - self.lastCursorToggle > 0.5:
                self.cursorVisible = not self.cursorVisible
                self.lastCursorToggle = time.time()

            if self.cursorVisible:
                # Calculate cursor position (end of the text)
                text = self.ids[teamIndex][boxIndex]
                textSurf = self.fontID.render(text, True, self.colorBlack)
                cursorX = box.x + 10 + textSurf.get_width()  # Position cursor at the end of the text
                pygame.draw.line(self.screen, self.colorBlack, (cursorX, box.y + 5), (cursorX, box.y + box.height - 5))

        pygame.display.update()
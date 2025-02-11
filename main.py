import pygame
import sys
import time
from GUI.playerGUI import *  # Ensure playerGUI.py is properly structured as a module
from Server.database import *  # If needed for player data

# Initialize Pygame
pygame.init()

# Create the game screen (800x600)
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Photon-System")

# Connect to the database
db = PlayerDatabase()
# db.connect()

# # Test DB connection
# players = db.get_players()
# print(players)

#refit image 
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

#will run the Player GUI 
def playerGUIrun(screen, db):
    clock = pygame.time.Clock()
    ui = TeamBoxUI(screen, db)

    running = True
    while running:
        for event in pygame.event.get():
            action = ui.handleEvent(event)
            if action == "quit":
                running = False

        ui.draw()
        clock.tick(30)

    pygame.quit()

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Set window size
    pygame.display.set_caption("Game Start")
    
    image = pygame.image.load("Photos/logo.jpg")  # Change to your image path
    x, y, scaledImage = getAspect(image, screen)

    # Fill screen with black
    screen.fill((0, 0, 0))

    # Draw the image centered
    screen.blit(scaledImage, (x, y))
    pygame.display.flip()
    
    time.sleep(3)  # Show image for 3 seconds
    
    # Run the player entry screen
    playerGUIrun(screen, db)

if __name__ == "__main__":
    main()  # Start the program

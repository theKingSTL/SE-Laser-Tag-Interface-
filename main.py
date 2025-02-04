import pygame
import sys
import GUI.playerGUI
from Server.database import *

#start pygame 
pygame.init()

# create our screen for the game (800x600)
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Photon-System")

#create DB 
db = PlayerDatabase()
db.connect()
#db.add_player(id,name) for later in main 
#test DB
players = db.get_players()
print(players)


# Manage Screens
def main():
    print("")
    # clock = pygame.time.Clock()
    # current_screen = MenuScreen(screen)  # Start with the Menu Screen

    # while True:
    #     next_screen = current_screen.run()  # Run the current screen

    #     if next_screen == "game":
    #         current_screen = GameScreen(screen)
    #     elif next_screen == "settings":
    #         current_screen = SettingsScreen(screen)
    #     elif next_screen == "menu":
    #         current_screen = MenuScreen(screen)
    #     elif next_screen == "quit":
    #         pygame.quit()
    #         sys.exit()

    #     clock.tick(60)  # Limit to 60 FPS

if __name__ == "__main__":
    main()


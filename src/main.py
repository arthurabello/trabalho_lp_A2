"""
Main entry point for the Warbound game.
"""

import sys
import pygame
from classes.menu.core.menu_manager import MenuManager
from classes.game.core.game_manager import GameManager

class WarBound:
    """Main game application class."""
    
    def __init__(self):
        """Initialize the game application."""
        try:
            pygame.init()
            if pygame.get_error():
                raise RuntimeError("Failed to initialize Pygame")
            
            self.screen = pygame.display.set_mode((1800, 1000), pygame.RESIZABLE)
            pygame.display.set_caption("Warbound")
            
        except Exception as e:
            print(f"Failed to initialize game: {str(e)}")
            sys.exit(1)

    def run(self):
        """Main application loop."""
        try:
            # Run menu
            menu = MenuManager(self.screen)
            menu_result = menu.run()
            
            # Start game if menu returns valid configuration
            if menu_result and menu_result.get('start_game'):
                game = GameManager(
                    player1_general=menu_result.get('player1_general'),
                    player2_general=menu_result.get('player2_general'),
                    map_choice=menu_result.get('map_choice', 1)
                )
                game.run()
                
        except Exception as e:
            print(f"Error running game: {str(e)}")
        finally:
            pygame.quit()

def main():
    """Entry point of the application."""
    app = WarBound()
    app.run()

if __name__ == "__main__":
    main()
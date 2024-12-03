"""
This module runs the game using everythig that was buit in other files
"""
import pygame
from classes.menu.menu import Menu
from classes.game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((1800, 1000), pygame.RESIZABLE)
    pygame.display.set_caption("Warbound")
    
    menu = Menu(screen)
    menu_result = menu.run()
    
    if menu_result and menu_result.get('start_game'):
        game = Game(
            player1_general=menu_result.get('player1_general'),
            player2_general=menu_result.get('player2_general'),
            map_choice=menu_result.get('map_choice', 1)
        )
        game.run()
    
    pygame.quit()

if __name__ == "__main__":
    main()
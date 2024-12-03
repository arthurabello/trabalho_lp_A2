"""
Core menu manager responsible for orchestrating menu functionality.
"""

import pygame
import os
from ..rendering.menu_renderer import MenuRenderer
from ..input.menu_input import MenuInputHandler
from .menu_state import MenuState
from ..tutorial.tutorial_manager import TutorialManager
from ...game.core.game_manager import GameManager

class MenuManager:
    def __init__(self, screen):
        """Initialize menu system."""
        self.screen = screen
        self.setup_systems()

    def setup_systems(self):
        """Initialize all menu subsystems."""
        try:
            pygame.mixer.init()
            self.background_music = pygame.mixer.Sound(os.path.join('..', 'assets', 'sounds', 'music', 'menu_music.ogg'))
            self.background_music.set_volume(0.5)
            self.background_music.play(-1) 
        except Exception as e:
            print(f"Failed to load music: {str(e)}")
            
        self.state = MenuState()
        self.renderer = MenuRenderer(self.screen, self)
        self.input_handler = MenuInputHandler(self)
        self.tutorial = TutorialManager(self.screen)

    def run(self):
        """Main menu loop."""
        while self.state.running:
            self.renderer.render()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state.running = False
                    return None
                    
                if self.tutorial.active:
                    result = self.tutorial.handle_event(event)
                    if result == 'menu':
                        self.tutorial.active = False
                else:
                    self.input_handler.handle_event(event)
                    
            if self.state.should_start_game:
                return {
                    'start_game': True,
                    'player1_general': self.state.player1_general,
                    'player2_general': self.state.player2_general,
                    'map_choice': self.state.map_choice
                }

        return None

    def start_game(self):
        """Prepare to start the game."""
        if self.state.map_choice and self.state.player1_general and self.state.player2_general:
            self.state.should_start_game = True

    def start_tutorial(self):
        """Activate tutorial mode."""
        self.tutorial.active = True
        self.tutorial.current_page = 0

    def toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        self.renderer.toggle_fullscreen()

    def change_state(self, new_state):
        """Change menu state."""
        self.state.current = new_state
        if new_state == "map_select":
            screen_width, screen_height = self.screen.get_size()
            self.renderer.setup_map_buttons(screen_width, screen_height)
        elif new_state == "general_selection":
            self.state.reset_general_selection()
        return new_state
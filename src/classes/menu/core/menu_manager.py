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
        self.state = MenuState()
        self.tutorial = TutorialManager(self.screen)  
        self.renderer = MenuRenderer(self.screen, self)
        self.input_handler = MenuInputHandler(self)
        
        try:
            pygame.mixer.init()
            pygame.mixer.set_num_channels(8) 
            
            self.background_music = pygame.mixer.Sound(os.path.join('..', 'assets', 'sounds', 'music', 'menu_music.ogg'))
            
            if self.state.music_enabled:
                self.background_music.set_volume(self.state.music_volume)
            else:
                self.background_music.set_volume(0)

            self.background_music_channel = pygame.mixer.Channel(7)
            self.background_music_channel.play(self.background_music, loops=-1)
            
        except Exception as e:
            print(f"Failed to load music: {str(e)}")
            
    def update_sound_state(self):
        """Update sound system state based on menu settings."""
        if hasattr(self, 'background_music_channel'):    
            if self.state.music_enabled:
                self.background_music_channel.set_volume(self.state.music_volume)
            else:
                self.background_music_channel.set_volume(0)

    def run(self):
        """Main menu loop."""
        while self.state.running:
            self.handle_events()
            self.update()
            self.render()
            
            if self.state.should_start_game:
                return {
                    'start_game': True,
                    'player1_general': self.state.player1_general,
                    'player2_general': self.state.player2_general,
                    'map_choice': self.state.map_choice
                }

        return None

    def handle_events(self):
        """Handle all events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state.running = False
                return
                
            if self.tutorial.active:
                result = self.tutorial.handle_event(event)
                if result == 'menu':
                    self.tutorial.active = False
            else:
                self.input_handler.handle_event(event)

    def update(self):
        """Update game state."""
        pass 

    def render(self):
        """Render current frame."""
        if self.tutorial.active:
            self.tutorial.draw()
        else:
            self.renderer.render()
            
        pygame.display.flip()

    def start_tutorial(self):
        """Activate tutorial mode."""
        self.tutorial.active = True
        self.tutorial.current_page = 0

    def start_game(self):
        """Prepare to start the game."""
        if self.state.player1_general and self.state.player2_general:
            self.state.should_start_game = True

    def toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        self.renderer.toggle_fullscreen()

    def change_state(self, new_state):
        """Change menu state."""
        self.state.current = new_state

        if new_state == "general_selection":
            self.state.reset_general_selection()
        elif new_state == "game":
            self.start_game()
        elif new_state == "quit":
            pygame.quit()
        return new_state
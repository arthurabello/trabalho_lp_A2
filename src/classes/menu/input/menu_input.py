"""
Handles input for the menu system.
"""

import pygame
from ..core.menu_state import MenuState

class MenuInputHandler:
    def __init__(self, menu_manager):
        """Initialize menu input handler."""
        self.menu_manager = menu_manager
        self.state = menu_manager.state

    def handle_event(self, event):
        """Process menu events."""
        if self.state.current == "main":
            self._handle_main_menu_event(event)
        elif self.state.current == "options":
            self._handle_options_event(event)
        elif self.state.current == "general_selection":
            self._handle_general_selection_event(event)

    def _handle_main_menu_event(self, event):
        """Handle main menu events."""
        for button in self.menu_manager.renderer.main_menu_buttons.values():
            if button.handle_event(event):
                break

    def _handle_options_event(self, event):
        """Handle options menu events."""
        for element in self.menu_manager.renderer.options_elements.values():
            if element.handle_event(event):
                break

    def _handle_general_selection_event(self, event):
        """Handle general selection events."""
        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        screen_width = self.menu_manager.screen.get_width()
        screen_height = self.menu_manager.screen.get_height()
        button_width = 200
        button_height = 40
        button_y = screen_height - button_height - 20

        cancel_button = pygame.Rect(20, button_y, button_width, button_height)
        if cancel_button.collidepoint(event.pos):
            if self.state.current_selecting_player == 1:
                self.state.player1_general = None
            else:
                self.state.player2_general = None
            return

        nav_button = pygame.Rect(
            screen_width - button_width - 20, 
            button_y, 
            button_width, 
            button_height
        )
        if nav_button.collidepoint(event.pos):
            if self.state.current_selecting_player == 1 and self.state.player1_general:
                self.state.current_selecting_player = 2
            elif self.state.current_selecting_player == 2:
                self.state.current_selecting_player = 1
            return

        if self.state.player1_general and self.state.player2_general:
            proceed_button = pygame.Rect(
                (screen_width - button_width) // 2,
                button_y,
                button_width,
                button_height
            )
            if proceed_button.collidepoint(event.pos):
                self.menu_manager.change_state("game")
                self.menu_manager.proceed = True
                return

        self._handle_general_card_selection(event.pos)

    def _handle_general_card_selection(self, pos):
        """Handle clicking on general cards."""
        for card in self.menu_manager.renderer.general_cards:
            if card.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': pos})):
                if self.state.current_selecting_player == 1:
                    if card.general_id != self.state.player2_general:
                        self.state.player1_general = card.general_id
                else:
                    if card.general_id != self.state.player1_general:
                        self.state.player2_general = card.general_id
                break

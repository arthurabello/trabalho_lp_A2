"""
Complete menu renderer implementation.
"""

import pygame
import os
from .components import Button, ToggleButton, Slider, GeneralCard

class MenuRenderer:
    def __init__(self, screen, menu_manager):
        """Initialize menu renderer."""
        self.screen = screen
        self.menu_manager = menu_manager
        self.state = menu_manager.state
        self.setup_resources()
        self.general_cards = []
        self.setup_ui_elements()

    def setup_main_menu_buttons(self, screen_width, screen_height):
        """Setup main menu buttons."""
        button_width, button_height = 200, 50
        button_spacing = 20
        start_y = screen_height // 2 - (button_height + button_spacing) * 2
        
        self.main_menu_buttons = {
            "play": Button(
                (screen_width - button_width) // 2,
                start_y,
                button_width,
                button_height,
                "Play",
                lambda: self.menu_manager.change_state("general_selection")
            ),
            "options": Button(
                (screen_width - button_width) // 2,
                start_y + button_height + button_spacing,
                button_width,
                button_height,
                "Options",
                lambda: self.menu_manager.change_state("options")
            ),
            "tutorial": Button(
                (screen_width - button_width) // 2,
                start_y + (button_height + button_spacing) * 2,
                button_width,
                button_height,
                "Tutorial",
                self.menu_manager.start_tutorial
            ),
            "quit": Button(
                (screen_width - button_width) // 2,
                start_y + (button_height + button_spacing) * 3,
                button_width,
                button_height,
                "Quit",
                lambda: self.menu_manager.change_state("quit")
            )
        }

    def setup_resources(self):
        """Setup visual resources."""
        self.load_images()
        self.setup_fonts()
        
    def load_images(self):
        """Load menu images and sprites."""
        self.menu_image = pygame.image.load(os.path.join("..", "assets", "images", "menu_image.png"))
        self.menu_image = self._scale_image_to_screen()
        
        self.general_sprites = {
            'alexander': pygame.image.load("../assets/images/menu_generals/alexander_menu.png"),
            'edward': pygame.image.load("../assets/images/menu_generals/edward_menu.png"),
            'charlemagne': pygame.image.load("../assets/images/menu_generals/charlemagne_menu.png"),
            'harald': pygame.image.load("../assets/images/menu_generals/harald_menu.png"),
            'julius': pygame.image.load("../assets/images/menu_generals/julius_menu.png"),
            'leonidas': pygame.image.load("../assets/images/menu_generals/leonidas_menu.png")
        }

    def setup_fonts(self):
        """Initialize fonts."""
        self.fonts = {
            'title': pygame.font.Font(None, 100),
            'normal': pygame.font.Font(None, 74),
            'small': pygame.font.Font(None, 36),
            'mini': pygame.font.Font(None, 20)
        }

    def setup_ui_elements(self):
        """Setup UI components."""
        screen_width, screen_height = self.screen.get_size()
        self.setup_main_menu_buttons(screen_width, screen_height)
        self.setup_options_elements(screen_width, screen_height)
        self.setup_map_buttons(screen_width, screen_height)
        self.setup_general_cards()


    def setup_options_elements(self, screen_width, screen_height):
        """Setup options menu elements."""
        panel_width, panel_height = 400, 450
        panel_x = (screen_width - panel_width) // 2
        panel_y = (screen_height - panel_height) // 2
        
        self.options_panel = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        
        toggle_size = 40
        slider_width = 250
        slider_height = 8
        element_start_y = panel_y + 80
        
        self.options_elements = {
            "sound_toggle": ToggleButton(
                panel_x + 30,
                element_start_y + 70,
                toggle_size,
                self.state.sound_enabled,
                self.state.toggle_sound
            ),
            "sound_slider": Slider(
                panel_x + 30 + toggle_size + 20,
                element_start_y + 70 + (toggle_size - slider_height) // 2,
                slider_width,
                slider_height,
                self.state.sound_volume,
                self.state.set_sound_volume
            ),
            "music_toggle": ToggleButton(
                panel_x + 30,
                element_start_y + 150,
                toggle_size,
                self.state.music_enabled,
                self.state.toggle_music
            ),
            "music_slider": Slider(
                panel_x + 30 + toggle_size + 20,
                element_start_y + 150 + (toggle_size - slider_height) // 2,
                slider_width,
                slider_height,
                self.state.music_volume,
                self.state.set_music_volume
            ),
            "back": Button(
                panel_x + (panel_width - 150) // 2,
                panel_y + panel_height - 80,
                150,
                50,
                "Back",
                lambda: self.menu_manager.change_state("main")  # Fixed line
            )
        }

    def setup_map_buttons(self, screen_width, screen_height):
        """Setup map selection buttons."""
        button_width, button_height = 250, 100
        button_spacing = 50
        
        self.map_buttons = {
            "map1": Button(
                (screen_width - button_width) // 2,
                screen_height // 2 - button_height - button_spacing // 2,
                button_width,
                button_height,
                "Map 1",
                lambda: setattr(self.state, 'map_choice', 1)
            ),
            "map2": Button(
                (screen_width - button_width) // 2,
                screen_height // 2 + button_spacing // 2,
                button_width,
                button_height,
                "Map 2",
                lambda: setattr(self.state, 'map_choice', 2)
            )
        }

    def setup_general_cards(self):
        """Setup general selection cards."""
        self.general_cards = []
        screen_width = self.screen.get_width()
        card_width = min(screen_width // 3.5, 280)
        card_height = int(card_width * 1.4)
        spacing = 25
        start_x = (screen_width - (card_width * 3 + spacing * 2)) // 2
        start_y = 150  
        
        for i, (general_id, info) in enumerate(self.state.generals.items()):
            col = i % 3
            row = i // 3
            x = start_x + col * (card_width + spacing)
            y = start_y + row * (card_height + spacing)
            
            selected = (
                (self.state.current_selecting_player == 1 and self.state.player1_general == general_id) or
                (self.state.current_selecting_player == 2 and self.state.player2_general == general_id)
            )
            
            card = GeneralCard(
                general_id=general_id,
                info=info,
                x=x,
                y=y,
                width=card_width,
                height=card_height,
                fonts=self.fonts,
                sprite=self.general_sprites[general_id],
                selected=selected
            )
            self.general_cards.append(card)

    def render(self):
        """Main render method."""
        self.screen.blit(self.menu_image, (0, 0))
        if self.state.current == "main":
            self._draw_main_menu()
        elif self.state.current == "options":
            self._draw_options_menu()
        elif self.state.current == "general_selection":
            self._draw_general_selection()
        elif self.state.current == "map_select":
            self._draw_map_selection()
        elif self.menu_manager.tutorial.active:
            self.menu_manager.tutorial.draw()

        pygame.display.flip()

    def _draw_main_menu(self):
        """Draw main menu screen."""
        title = self.fonts['title'].render("WARBOUND", True, (255, 215, 0))
        title_rect = title.get_rect(centerx=self.screen.get_rect().centerx, top=50)
        
        shadow = self.fonts['title'].render("WARBOUND", True, (0, 0, 0))
        shadow_rect = title_rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        
        self.screen.blit(shadow, shadow_rect)
        self.screen.blit(title, title_rect)
        
        for button in self.main_menu_buttons.values():
            button.draw(self.screen)

    def _draw_options_menu(self):
        """Draw options menu screen."""
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        pygame.draw.rect(self.screen, (30, 30, 33), self.options_panel, border_radius=15)
        pygame.draw.rect(self.screen, (255, 255, 255), self.options_panel, 2, border_radius=15)
        
        title = self.fonts['normal'].render("Options", True, (255, 215, 0))
        title_rect = title.get_rect(centerx=self.options_panel.centerx, top=self.options_panel.top + 20)
        self.screen.blit(title, title_rect)
        
        sfx_label = self.fonts['small'].render("Sound Effects", True, (200, 200, 200))
        music_label = self.fonts['small'].render("Background Music", True, (200, 200, 200))
        self.screen.blit(sfx_label, (self.options_panel.x + 30, self.options_panel.y + 120))
        self.screen.blit(music_label, (self.options_panel.x + 30, self.options_panel.y + 200))
        
        for element in self.options_elements.values():
            element.draw(self.screen)



    def _draw_map_selection(self):
        """Draw map selection screen."""
        title = self.fonts['title'].render("Select a Map", True, (255, 215, 0))
        title_rect = title.get_rect(centerx=self.screen.get_rect().centerx, top=50)
        
        shadow = self.fonts['title'].render("Select a Map", True, (0, 0, 0))
        shadow_rect = title_rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        
        self.screen.blit(shadow, shadow_rect)
        self.screen.blit(title, title_rect)
        
        for button in self.map_buttons.values():
            button.draw(self.screen)

    def _scale_image_to_screen(self):
        """Scale background image to fit screen."""
        screen_width, screen_height = self.screen.get_size()
        image_width, image_height = self.menu_image.get_size()
        
        width_scale = screen_width / image_width
        height_scale = screen_height / image_height
        scale = min(width_scale, height_scale)
        
        new_width = int(image_width * scale)
        new_height = int(image_height * scale)
        
        scaled_image = pygame.transform.smoothscale(self.menu_image, (new_width, new_height))
        
        final_surface = pygame.Surface((screen_width, screen_height))
        final_surface.fill((0, 0, 0))
        
        x_offset = (screen_width - new_width) // 2
        y_offset = (screen_height - new_height) // 2
        
        final_surface.blit(scaled_image, (x_offset, y_offset))
        
        return final_surface
    


    def _draw_general_selection(self):
        """
        Draws the general selection screen with properly formatted cards and layout.
        """
        screen_width, screen_height = self.screen.get_size()
        
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        title = self.fonts['title'].render("Select Your General", True, (255, 215, 0))
        title_rect = title.get_rect(centerx=screen_width//2, top=20)
        self.screen.blit(title, title_rect)
        
        player_text = self.fonts['normal'].render(f"Player {self.state.current_selecting_player}'s Selection", 
                                                True, (255, 255, 255))
        player_rect = player_text.get_rect(centerx=screen_width//2, top=title_rect.bottom + 10)
        self.screen.blit(player_text, player_rect)
        
        card_width = min(screen_width // 3.5, 280)  
        card_height = int(card_width * 1.4)  
        spacing = 25  

        start_x = (screen_width - (card_width * 3 + spacing * 2)) // 2
        start_y = player_rect.bottom + 15

        self.general_cards = []

        row_count = 2
        col_count = 3

        for i, (general_id, general_info) in enumerate(self.state.generals.items()):
            row = i // col_count 
            col = i % col_count  
            
            x = start_x + col * (card_width + spacing)
            y = start_y + row * (card_height + spacing)
            
            selected = (
                (self.state.current_selecting_player == 1 and self.state.player1_general == general_id) or
                (self.state.current_selecting_player == 2 and self.state.player2_general == general_id)
            )
            
            card = GeneralCard(
                general_id=general_id,
                info=general_info,
                x=x,
                y=y,
                width=card_width,
                height=card_height,
                fonts=self.fonts,
                sprite=self.general_sprites[general_id],
                selected=selected
            )
            self.general_cards.append(card)
            card.draw(self.screen)
        
        self._draw_general_selection_buttons()

    def _draw_general_selection_buttons(self):
        """
        Draws the navigation buttons for the general selection screen.
        """
        screen_width, screen_height = self.screen.get_size()
        button_width = 200
        button_height = 40
        button_y = screen_height - button_height - 10

        cancel_button = pygame.Rect(20, button_y, button_width, button_height)
        pygame.draw.rect(self.screen, (180, 30, 30), cancel_button, border_radius=10)
        cancel_text = self.fonts['small'].render("Cancel Selection", True, (255, 255, 255))
        cancel_rect = cancel_text.get_rect(center=cancel_button.center)
        self.screen.blit(cancel_text, cancel_rect)

        nav_text = "Next Player" if self.state.current_selecting_player == 1 else "Previous Player"
        nav_button = pygame.Rect(
            screen_width - button_width - 20, 
            button_y, 
            button_width, 
            button_height
        )
        pygame.draw.rect(self.screen, (30, 180, 30), nav_button, border_radius=10)
        nav_text_surf = self.fonts['small'].render(nav_text, True, (255, 255, 255))
        nav_rect = nav_text_surf.get_rect(center=nav_button.center)
        self.screen.blit(nav_text_surf, nav_rect)

        if self.state.player1_general and self.state.player2_general:
            proceed_button = pygame.Rect(
                (screen_width - button_width) // 2,
                button_y,
                button_width,
                button_height
            )
            pygame.draw.rect(self.screen, (30, 30, 180), proceed_button, border_radius=10)
            proceed_text = self.fonts['small'].render("Proceed", True, (255, 255, 255))
            proceed_rect = proceed_text.get_rect(center=proceed_button.center)
            self.screen.blit(proceed_text, proceed_rect)

    def handle_general_selection(self, pos):
        """
        Handles mouse clicks in the general selection screen.
        
        Args:
            pos (tuple): Mouse position (x, y)
        """
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        button_width = 200
        button_height = 40
        button_y = screen_height - button_height - 20

        cancel_button = pygame.Rect(20, button_y, button_width, button_height)
        if cancel_button.collidepoint(pos):
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
        if nav_button.collidepoint(pos):
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
            if proceed_button.collidepoint(pos):
                self.state = "map_select"
                return

        for card in self.general_cards:
            if card.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': pos})):
                if self.state.current_selecting_player == 1: 
                    if card.general_id != self.state.player2_general:
                        self.state.player1_general = card.general_id
                else:
                    if card.general_id != self.state.player1_general:
                        self.state.player2_general = card.general_id
                break
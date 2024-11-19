"""
This module handles the main menu and its functionalities using a modular approach
"""

import pygame
import os
from .tutorial import Tutorial

class Button:
    def __init__(self, x, y, width, height, text, callback, border_radius=10, fontsize=36):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.border_radius = border_radius
        self.font = pygame.font.Font(None, fontsize)
        
        self.color_default = (45, 45, 48)
        self.color_hover = (70, 70, 75)
        self.color_text = (255, 255, 255)
        self.color_current = self.color_default

    def draw(self, screen):
        pygame.draw.rect(screen, self.color_current, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(screen, self.color_text, self.rect, 2, border_radius=self.border_radius)
        
        text_surface = self.font.render(self.text.capitalize(), True, self.color_text)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()
                return True
        elif event.type == pygame.MOUSEMOTION:
            self.color_current = self.color_hover if self.rect.collidepoint(event.pos) else self.color_default
        return False

class ToggleButton:
    def __init__(self, x, y, size, initial_state, callback):
        self.rect = pygame.Rect(x, y, size, size)
        self.callback = callback
        self.state = initial_state
        self.font = pygame.font.Font(None, 24)
        
        self.colors = {
            'enabled': (76, 175, 80),
            'disabled': (244, 67, 54),
            'text': (255, 255, 255)
        }

    def draw(self, screen):
        color = self.colors['enabled'] if self.state else self.colors['disabled']
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        
        text = "ON" if self.state else "OFF"
        text_surface = self.font.render(text, True, self.colors['text'])
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.state = not self.state
            self.callback(self.state)
            return True
        return False

class Slider:
    def __init__(self, x, y, width, height, initial_value, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.callback = callback
        self.value = initial_value
        self.dragging = False
        
        self.colors = {
            'background': (70, 70, 75),
            'fill': (76, 175, 80),
            'handle': (120, 120, 125)
        }

    def draw(self, screen):
        pygame.draw.rect(screen, self.colors['background'], self.rect, border_radius=4)
        
        fill_rect = self.rect.copy()
        fill_rect.width *= self.value
        pygame.draw.rect(screen, self.colors['fill'], fill_rect, border_radius=4)

        handle_pos = self.rect.x + (self.rect.width * self.value)
        handle_rect = pygame.Rect(handle_pos - 8, self.rect.y - 6, 16, 20)
        pygame.draw.rect(screen, self.colors['handle'], handle_rect, border_radius=5)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            relative_x = (event.pos[0] - self.rect.x) / self.rect.width
            self.value = max(0, min(1, relative_x))
            self.callback(self.value)
            return True
        return False

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.state = "main"
        self.setup_resources()
        self.setup_audio()
        self.setup_ui_elements()
        self.tutorial = Tutorial(self.screen)
        
    def setup_resources(self):
        self.original_menu_image = pygame.image.load(os.path.join("..", "assets", "images", "menu_image.png"))
        self.menu_image = self._scale_image_to_screen()
        
        self.fonts = {
            'title': pygame.font.Font(None, 100),
            'normal': pygame.font.Font(None, 74),
            'small': pygame.font.Font(None, 36),
            'mini': pygame.font.Font(None, 24)
        }

    def setup_audio(self):
        self.music_enabled = True
        self.sound_enabled = True
        self.music_volume = 0.7
        self.sound_volume = 0.7
        
        pygame.mixer.music.load(os.path.join("..", "assets", "sounds", "music", "menu_music.ogg"))
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(-1)

    def setup_ui_elements(self):
        screen_width, screen_height = self.screen.get_size()
        
        button_width, button_height = 200, 50
        button_spacing = 20
        start_y = screen_height // 2 - (button_height + button_spacing) * 2
        
        self.main_buttons = {
            "play": Button(
                (screen_width - button_width) // 2,
                start_y,
                button_width,
                button_height,
                "Play",
                lambda: self.change_state("map_select")
            ),
            "options": Button(
                (screen_width - button_width) // 2,
                start_y + button_height + button_spacing,
                button_width,
                button_height,
                "Options",
                lambda: self.change_state("options")
            ),
            "tutorial": Button(
                (screen_width - button_width) // 2,
                start_y + (button_height + button_spacing) * 2,
                button_width,
                button_height,
                "Tutorial",
                self.start_tutorial
            ),
            "quit": Button(
                (screen_width - button_width) // 2,
                start_y + (button_height + button_spacing) * 3,
                button_width,
                button_height,
                "Quit",
                lambda: self.change_state("quit")
            )
        }
        
        self.setup_options_elements()
        self.setup_map_buttons()

    def setup_options_elements(self):
        screen_width, screen_height = self.screen.get_size()
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
                self.sound_enabled,
                self.toggle_sound
            ),
            "sound_slider": Slider(
                panel_x + 30 + toggle_size + 20,
                element_start_y + 70 + (toggle_size - slider_height) // 2,
                slider_width,
                slider_height,
                self.sound_volume,
                self.set_sound_volume
            ),
            "music_toggle": ToggleButton(
                panel_x + 30,
                element_start_y + 150,
                toggle_size,
                self.music_enabled,
                self.toggle_music
            ),
            "music_slider": Slider(
                panel_x + 30 + toggle_size + 20,
                element_start_y + 150 + (toggle_size - slider_height) // 2,
                slider_width,
                slider_height,
                self.music_volume,
                self.set_music_volume
            ),
            "back": Button(
                panel_x + (panel_width - 150) // 2,
                panel_y + panel_height - 80,
                150,
                50,
                "Back",
                lambda: self.change_state("main")
            )
        }

    def setup_map_buttons(self):
        screen_width, screen_height = self.screen.get_size()
        button_width, button_height = 250, 100
        button_spacing = 50
        
        self.map_buttons = {
            "map1": Button(
                (screen_width - button_width) // 2,
                screen_height // 2 - button_height - button_spacing // 2,
                button_width,
                button_height,
                "Map 1",
                lambda: self.change_state("game_map1")
            ),
            "map2": Button(
                (screen_width - button_width) // 2,
                screen_height // 2 + button_spacing // 2,
                button_width,
                button_height,
                "Map 2",
                lambda: self.change_state("game_map2")
            )
        }

    def toggle_sound(self, enabled):
        self.sound_enabled = enabled

    def toggle_music(self, enabled):
        self.music_enabled = enabled
        if enabled:
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()

    def set_sound_volume(self, volume):
        self.sound_volume = volume

    def set_music_volume(self, volume):
        self.music_volume = volume
        pygame.mixer.music.set_volume(volume)

    def start_tutorial(self):
        self.tutorial.active = True
        self.tutorial.current_page = 0

    def change_state(self, new_state):
        self.state = new_state
        if new_state == "map_select":
            self.setup_map_buttons()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
                
            if self.tutorial.active:
                result = self.tutorial.handle_event(event)
                if result == 'menu':
                    self.tutorial.active = False
                    return self.state
                    
            elif self.state == "main":
                for button in self.main_buttons.values():
                    if button.handle_event(event):
                        break
            elif self.state == "options":
                for element in self.options_elements.values():
                    if element.handle_event(event):
                        break
            elif self.state == "map_select":
                for button in self.map_buttons.values():
                    if button.handle_event(event):
                        break
                        
        return self.state
    
    def _scale_image_to_screen(self):

        """
        Scales the menu image to fit the screen size
        """

        screen_width, screen_height = self.screen.get_size()
        image_width, image_height = self.original_menu_image.get_size()
        
        width_scale = screen_width / image_width
        height_scale = screen_height / image_height
        
        scale = min(width_scale, height_scale)
        
        new_width = int(image_width * scale)
        new_height = int(image_height * scale)
        
        scaled_image = pygame.transform.smoothscale(self.original_menu_image, (new_width, new_height))
        
        final_surface = pygame.Surface((screen_width, screen_height))
        final_surface.fill((0, 0, 0)) 
        
        x_offset = (screen_width - new_width) // 2
        y_offset = (screen_height - new_height) // 2
        
        final_surface.blit(scaled_image, (x_offset, y_offset))
        
        return final_surface

    def draw(self):
        self.screen.blit(self.menu_image, (0, 0))
        
        if self.state == "main":
            self._draw_main_menu()
        elif self.state == "options":
            self._draw_options_menu()
        elif self.state == "map_select":
            self._draw_map_selection()
            
        if self.tutorial.active:
            self.tutorial.draw()
            
        pygame.display.flip()

    def _draw_main_menu(self):

        title = self.fonts['title'].render("WARBOUND", True, (255, 215, 0))
        title_rect = title.get_rect(centerx=self.screen.get_rect().centerx, top=50)
        
        shadow = self.fonts['title'].render("WARBOUND", True, (0, 0, 0))
        shadow_rect = title_rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        self.screen.blit(shadow, shadow_rect)
        self.screen.blit(title, title_rect)
        
        for button in self.main_buttons.values():
            button.draw(self.screen)

    def _draw_options_menu(self):

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

    def change_state(self, new_state):
        """
        Changes the current menu state and handles necessary updates
        """
        self.state = new_state
        if new_state == "map_select":
            self.setup_map_buttons() 
        return new_state

    def _draw_map_selection(self):
        """
        Draws the map selection screen
        """
        title = self.fonts['title'].render("Select a Map", True, (255, 215, 0))
        title_rect = title.get_rect(centerx=self.screen.get_rect().centerx, top=50)
        
        shadow = self.fonts['title'].render("Select a Map", True, (0, 0, 0))
        shadow_rect = title_rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        self.screen.blit(shadow, shadow_rect)
        self.screen.blit(title, title_rect)
        
        if hasattr(self, 'map_buttons'):
            for button in self.map_buttons.values():
                button.draw(self.screen)
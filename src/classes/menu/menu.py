"""
This module handles the main menu and its functionalities
"""

import pygame
import os
from .tutorial import Tutorial

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.state = "main"  
        
        self.original_menu_image = pygame.image.load(os.path.join("..", "assets", "images", "menu_image.png"))
        self.menu_image = self._scale_image_to_screen()
        
        self.music_enabled = True
        self.sound_enabled = True
        self.music_volume = 0.7
        self.sound_volume = 0.7
        
        pygame.mixer.music.load(os.path.join("..", "assets", "sounds", "music", "menu_music.ogg"))
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(-1)  
        
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)  
        self.mini_font = pygame.font.Font(None, 24)   
        self._init_buttons()
        self.tutorial = Tutorial(self.screen)

        self.COLORS = {
            'button_bg': (45, 45, 48),
            'button_hover': (60, 60, 65),
            'button_text': (255, 255, 255),
            'slider_bg': (70, 70, 75),
            'slider_handle': (120, 120, 125),
            'enabled': (76, 175, 80),
            'disabled': (244, 67, 54),
            'title': (255, 215, 0),
            'text': (200, 200, 200)
        }

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
    
    def handle_resize(self):
        
        """
        Handles the resize event
        """

        self.menu_image = self._scale_image_to_screen()
        self._init_buttons() 
        
    def _init_buttons(self):
        
        """
        Initializes the buttons
        """

        screen_width, screen_height = self.screen.get_size()
        button_width = 200
        button_height = 50
        button_spacing = 20
        start_y = screen_height // 2 - (button_height + button_spacing) * 2
        
        self.main_buttons = {
            "play": pygame.Rect((screen_width - button_width) // 2, start_y, button_width, button_height),
            "options": pygame.Rect((screen_width - button_width) // 2, start_y + button_height + button_spacing, button_width, button_height),
            "tutorial": pygame.Rect((screen_width - button_width) // 2, start_y + (button_height + button_spacing) * 2, button_width, button_height),
            "quit": pygame.Rect((screen_width - button_width) // 2, start_y + (button_height + button_spacing) * 3, button_width, button_height)
        }
        
        options_panel_width = 400
        options_panel_height = 450
        panel_x = (screen_width - options_panel_width) // 2
        panel_y = (screen_height - options_panel_height) // 2
        
        self.options_panel = pygame.Rect(panel_x, panel_y, options_panel_width, options_panel_height)
        
        element_spacing = 60
        element_start_y = panel_y + 80
        toggle_size = 40
        slider_width = 250
        slider_height = 8
        label_offset = 70  

        self.options_elements = {
            "sfx_label": pygame.Rect(panel_x + 30, element_start_y, 200, 30),
            "sound_toggle": pygame.Rect(panel_x + 30, element_start_y + label_offset, toggle_size, toggle_size),
            "sound_slider": pygame.Rect(panel_x + 30 + toggle_size + 20, 
                                    element_start_y + label_offset + (toggle_size - slider_height) // 2,
                                    slider_width, slider_height),
            
            "music_label": pygame.Rect(panel_x + 30, element_start_y + element_spacing, 200, 30),
            "music_toggle": pygame.Rect(panel_x + 30, element_start_y + element_spacing + label_offset, toggle_size, toggle_size),
            "music_slider": pygame.Rect(panel_x + 30 + toggle_size + 20,
                                    element_start_y + element_spacing + label_offset + (toggle_size - slider_height) // 2,
                                    slider_width, slider_height),
            
            "back": pygame.Rect(panel_x + (options_panel_width - 150) // 2,
                            panel_y + options_panel_height - 80,
                            150, 50)
        }

    def handle_events(self):

        """
        Handles the main events of the menu
        """
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
              
            if self.tutorial.active:
                result = self.tutorial.handle_event(event)
                if result == 'menu':
                    self.tutorial.active = False
                    return self.state
                     
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if self.state == "main":
                    return self._handle_main_menu_click(mouse_pos)
                elif self.state == "options":
                    return self._handle_options_menu_click(mouse_pos)
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging = None
        
        return self.state
    
    def _handle_main_menu_click(self, mouse_pos):

        """
        Handles the main menu click
        """

        for button_name, button_rect in self.main_buttons.items():
            if button_rect.collidepoint(mouse_pos):
                if button_name == "quit":
                    return "quit"
                elif button_name == "play":
                    return "game"
                elif button_name == "options":
                    self.state = "options"
                elif button_name == "tutorial":
                    self.tutorial.active = True
                    self.tutorial.current_page = 0  #first page

        return self.state
    
    def _handle_options_menu_click(self, mouse_pos):
        
        """
        Handles the options menu click
        """

        if self.options_elements["back"].collidepoint(mouse_pos):
            self.state = "main"
            return "main"
            
        for element_name, element_rect in self.options_elements.items():
            if element_rect.collidepoint(mouse_pos):
                if element_name == "sound_toggle":
                    self.sound_enabled = not self.sound_enabled
                    return self.state
                elif element_name == "music_toggle":
                    self.music_enabled = not self.music_enabled
                    if self.music_enabled:
                        pygame.mixer.music.play(-1)
                    else:
                        pygame.mixer.music.stop()
                    return self.state
                
        for slider_name, volume_name in [("sound_slider", "sound_volume"), ("music_slider", "music_volume")]:
            slider_rect = self.options_elements[slider_name]
            if slider_rect.collidepoint(mouse_pos):
                relative_x = (mouse_pos[0] - slider_rect.x) / slider_rect.width
                volume = max(0, min(1, relative_x))
                setattr(self, volume_name, volume)
                if volume_name == "music_volume":
                    pygame.mixer.music.set_volume(volume)
                
        return self.state
                
    
    def draw(self):

        """
        Draws the menu
        """

        self.screen.blit(self.menu_image, (0, 0))
        
        if self.state == "main":
            self._draw_main_menu()
        elif self.state == "options":
            self._draw_options_menu()
            
        if self.tutorial.active:
            self.tutorial.draw()
            
        pygame.display.flip()
    
    def _draw_main_menu(self):
        
        """
        Draws the main menu title and buttons
        """

        title_font = pygame.font.Font(None, 100) 
        title = title_font.render("WARBOUND", True, (255, 215, 0))  #this color is changeable
        title_rect = title.get_rect()
        title_rect.centerx = self.screen.get_rect().centerx
        title_rect.top = 50  
        
        shadow_offset = 3
        title_shadow = title_font.render("WARBOUND", True, (0, 0, 0))
        shadow_rect = title_rect.copy()
        shadow_rect.x += shadow_offset
        shadow_rect.y += shadow_offset
        self.screen.blit(title_shadow, shadow_rect)
        self.screen.blit(title, title_rect)

        for button_name, button_rect in self.main_buttons.items():
            mouse_pos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_pos):
                color = (70, 70, 75) 
            else:
                color = (45, 45, 48)  
            
            pygame.draw.rect(self.screen, color, button_rect, border_radius=10)
            pygame.draw.rect(self.screen, self.COLORS['button_text'], button_rect, 2, border_radius=10)
            
            text = self.small_font.render(button_name.capitalize(), True, self.COLORS['button_text'])
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)
        
    def _draw_options_menu(self):
        
        """
        Draws the options menu
        """

        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        pygame.draw.rect(self.screen, (30, 30, 33), self.options_panel, border_radius=15)
        pygame.draw.rect(self.screen, self.COLORS['button_text'], self.options_panel, 2, border_radius=15)
        
        title = self.font.render("Options", True, self.COLORS['title'])
        title_rect = title.get_rect(centerx=self.options_panel.centerx, top=self.options_panel.top + 20)
        self.screen.blit(title, title_rect)
        
        sfx_label = self.small_font.render("Sound Effects", True, self.COLORS['text'])
        self.screen.blit(sfx_label, self.options_elements["sfx_label"])
        
        music_label = self.small_font.render("Background Music", True, self.COLORS['text'])
        self.screen.blit(music_label, self.options_elements["music_label"])
        
        for toggle_name in ["sound_toggle", "music_toggle"]:
            enabled = getattr(self, toggle_name.replace("_toggle", "_enabled"))
            color = self.COLORS['enabled'] if enabled else self.COLORS['disabled']
            rect = self.options_elements[toggle_name]
            pygame.draw.rect(self.screen, color, rect, border_radius=8)
            text = "ON" if enabled else "OFF"
            text_surf = self.small_font.render(text, True, self.COLORS['button_text'])
            text_rect = text_surf.get_rect(center=rect.center)
            self.screen.blit(text_surf, text_rect)
        
        for slider_name, volume_name in [("sound_slider", "sound_volume"), ("music_slider", "music_volume")]:

            slider_rect = self.options_elements[slider_name]
            pygame.draw.rect(self.screen, self.COLORS['slider_bg'], slider_rect, border_radius=4)
            volume = getattr(self, volume_name)
            fill_rect = slider_rect.copy()
            fill_rect.width *= volume
            pygame.draw.rect(self.screen, self.COLORS['enabled'], fill_rect, border_radius=4)
            handle_pos = slider_rect.x + (slider_rect.width * volume)
            handle_rect = pygame.Rect(handle_pos - 8, slider_rect.y - 6, 16, 20)
            pygame.draw.rect(self.screen, self.COLORS['slider_handle'], handle_rect, border_radius=5)
        
        mouse_pos = pygame.mouse.get_pos()
        back_rect = self.options_elements["back"]
        
        if back_rect.collidepoint(mouse_pos):
            color = (70, 70, 75)  
        else:
            color = (45, 45, 48) 
            
        pygame.draw.rect(self.screen, color, back_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.COLORS['button_text'], back_rect, 2, border_radius=10)
        
        back_text = self.small_font.render("Back", True, self.COLORS['button_text'])
        back_rect = back_text.get_rect(center=self.options_elements["back"].center)
        self.screen.blit(back_text, back_rect)
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
        
        """
        Draws the button on the screen
        """

        pygame.draw.rect(screen, self.color_current, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(screen, self.color_text, self.rect, 2, border_radius=self.border_radius)
        
        text_surface = self.font.render(self.text.capitalize(), True, self.color_text)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        
        """
        Handles events for the button
        """

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
        
        """
        Draws the toggle button on the screen
        """

        color = self.colors['enabled'] if self.state else self.colors['disabled']
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        
        text = "ON" if self.state else "OFF"
        text_surface = self.font.render(text, True, self.colors['text'])
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        
        """
        Handles events for the toggle button
        """

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
        
        """
        Draws the slider on the screen
        """

        pygame.draw.rect(screen, self.colors['background'], self.rect, border_radius=4)
        
        fill_rect = self.rect.copy()
        fill_rect.width *= self.value
        pygame.draw.rect(screen, self.colors['fill'], fill_rect, border_radius=4)

        handle_pos = self.rect.x + (self.rect.width * self.value)
        handle_rect = pygame.Rect(handle_pos - 8, self.rect.y - 6, 16, 20)
        pygame.draw.rect(screen, self.colors['handle'], handle_rect, border_radius=5)

    def handle_event(self, event):
        
        """
        Handles events for the slider
        """

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
        self.player1_general = None
        self.player2_general = None
        self.current_selecting_player = 1
        self.map_choice = None
        self.running = True

        self.general_sprites = {
            'alexander': pygame.image.load("../assets/images/menu_generals/alexander_menu.png"),
            'edward': pygame.image.load("../assets/images/menu_generals/edward_menu.png"),
            'charlemagne': pygame.image.load("../assets/images/menu_generals/charlemagne_menu.png"),
            'harald': pygame.image.load("../assets/images/menu_generals/harald_menu.png"),
            'julius': pygame.image.load("../assets/images/menu_generals/julius_menu.png"),
            'leonidas': pygame.image.load("../assets/images/menu_generals/leonidas_menu.png")
        }
        
        self.generals = {
            'alexander': {
                'name': 'Alexander the Great of Macedon',
                'bonus': [
                    'Hypaspists: +10% Defense (Passive)',
                    'Hypaspists: +20% Strength in Phalanx',
                    'Hypaspists: +30% Strength w/Alexander'
                ]
            },
            'edward': {
                'name': 'Edward the Elder of Wessex',
                'bonus': [
                    'Archers: +5% Strength (Passive)',
                    'Man-at-arms: +25% Strength w/Edward',
                    'Archers: +25% Str, +5% Def, +1 Move w/Edward'
                ]
            },
            'charlemagne': {
                'name': 'Charlemagne of The Franks',
                'bonus': [
                    'Heavy Cavalry: +5% Defense (Passive)',
                    'Heavy Cavalry: +35% Strength, +1 Move w/Charlemagne'
                ]
            },
            'harald': {
                'name': 'Harald Hardrada of Norway',
                'bonus': [
                    'Vikings: +12% Defense (Passive)',
                    'Vikings: +40% Strength w/Harald',
                    'Archers: +5% Strength (Passive)'
                ]
            },
            'julius': {
                'name': 'Julius Caesar of Rome',
                'bonus': [
                    'Legions: +10% Defense (Passive)',
                    'Light Cav: +5% Strength (Passive)',
                    'Legions: +25% Str, +1 Move w/Julius'
                ]
            },
            'leonidas': {
                'name': 'Leonidas I of Sparta',
                'bonus': [
                    'Hoplites: +20% Defense (Passive)',
                    'Hoplites: +25% Str, +1 Move w/Leonidas'
                ]
            }
        }

    def run(self):
        """
        Runs the menu and returns the game configuration when ready
        """
        while self.running:
            self.draw()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return None
                    
                if self.tutorial.active:
                    result = self.tutorial.handle_event(event)
                    if result == 'menu':
                        self.tutorial.active = False
                        
                elif self.state == "main":
                    for button in self.main_buttons.values():
                        if button.handle_event(event):
                            break
                            
                elif self.state == "general_selection":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.handle_general_selection(event.pos)
                        
                elif self.state == "map_select":
                    for button in self.map_buttons.values():
                        if button.handle_event(event):
                            if self.map_choice and self.player1_general and self.player2_general:
                                return {
                                    'start_game': True,
                                    'player1_general': self.player1_general,
                                    'player2_general': self.player2_general,
                                    'map_choice': self.map_choice
                                }
                            break
                            
                elif self.state == "options":
                    for element in self.options_elements.values():
                        if element.handle_event(event):
                            break
        
        return None

    def handle_map_selection(self, map_number):
        self.map_choice = map_number
        if self.player1_general and self.player2_general:
            self.running = False
    
    def draw_general_selection(self):
        
        """
        Function to draw the general selection screen.

        How it works:
            1. It clears the screen.
            2. It renders the title "Select Your General" in the center of the screen.
            3. It renders the player's selection text in the center of the screen.
            4. It defines the width and height of the cards and spacing between them.
            5. It calculates the starting position of the cards.
            6. It calls the draw_wave_separator function to draw the wave separator.
            7. It iterates over the generals and their information.
            8. It renders the general name and bonus information.
            9. It blits the rendered text onto the screen.
            10. It blits the general images onto the screen.
            11. It blits the wave separator onto the screen.
            12. It blits the "Back" button onto the screen.
            13. It blits the "Next" button onto the screen.
            14. It blits the "Done" button onto the screen.
            15. It updates the display.
        """

        screen_width, screen_height = self.screen.get_size()
        self.screen.fill((20, 20, 25))
        title = self.fonts['title'].render("Select Your General", True, (255, 215, 0))
        title_rect = title.get_rect(centerx=screen_width//2, top=20) 
        self.screen.blit(title, title_rect)
        
        player_text = self.fonts['normal'].render(f"Player {self.current_selecting_player}'s Selection", 
                                                True, (255, 255, 255))
        player_rect = player_text.get_rect(centerx=screen_width//2, top=title_rect.bottom + 10)  
        self.screen.blit(player_text, player_rect)
        
        card_width = min(screen_width // 3.5, 280)  
        card_height = int(card_width * 1.4)  
        spacing = 25  
        start_x = (screen_width - (card_width * 3 + spacing * 2)) // 2
        start_y = player_rect.bottom + 15  
        
        def draw_wave_separator(surface, x, y, width):
            
            """
            Auxiliary Function to draw a wave separator (merely aesthetic).

            Args:
                surface (pygame.Surface): The surface to draw on
                x (int): X-coordinate of the separator
                y (int): Y-coordinate of the separator
                width (int): Width of the separator
            """

            points = []
            wave_height = 2  
            segments = 12 
            for i in range(segments + 1):
                segment_x = x + (width * i / segments)
                segment_y = y + (wave_height * (-1 if i % 2 == 0 else 1))
                points.append((segment_x, segment_y))
                
            if len(points) > 1:
                pygame.draw.lines(surface, (100, 100, 100), False, points, 1)
        
        def wrap_text(text, font, max_width):
            
            """
            Auxiliary Function to wrap text into multiple lines based on a maximum width.

            Args:
                text (str): The text to wrap.
                font (pygame.font.Font): The font to use for the text.
                max_width (int): The maximum width of each line.

            Returns:
                list: A list of wrapped lines of text.
            """

            words = text.split()
            lines = []
            current_line = []
                
            for word in words:
                current_line.append(word)
                test_surface = font.render(' '.join(current_line), True, (255, 255, 255))
                if test_surface.get_width() > max_width:
                    current_line.pop()
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]
            if current_line:
                lines.append(' '.join(current_line))
            return lines


        for i, (general_id, general_info) in enumerate(self.generals.items()):
            col = i % 3
            row = i // 3
            x = start_x + col * (card_width + spacing)
            y = start_y + row * (card_height + spacing)
            
            card_surface = pygame.Surface((card_width, card_height))
            card_surface.fill((40, 40, 45))
            
            portrait_size = int(card_width * 0.7)  
            portrait_x = (card_width - portrait_size) // 2
            portrait_rect = pygame.Rect(portrait_x, 15, portrait_size, portrait_size) 
            pygame.draw.rect(card_surface, (30, 30, 35), portrait_rect)
            
            if self.general_sprites[general_id]:
                portrait = pygame.transform.scale(self.general_sprites[general_id], 
                                            (portrait_size, portrait_size))
                card_surface.blit(portrait, (portrait_x, 20))
            
            text_start_y = portrait_rect.bottom + 15  
            
            words = general_info['name'].split()
            name_lines = []
            current_line = []
            
            for word in words:
                current_line.append(word)
                test_surface = self.fonts['small'].render(' '.join(current_line), True, (255, 215, 0))
                if test_surface.get_width() > card_width - 20:
                    current_line.pop()
                    if current_line:
                        name_lines.append(' '.join(current_line))
                    current_line = [word]
            if current_line:
                name_lines.append(' '.join(current_line))
            
            for idx, line in enumerate(name_lines):
                name_surface = self.fonts['small'].render(line, True, (255, 215, 0))
                name_rect = name_surface.get_rect(centerx=card_width//2, 
                                                top=text_start_y + idx * 25)
                card_surface.blit(name_surface, name_rect)
            

            effect_y = text_start_y + len(name_lines) * 22 + 15
            max_effect_width = card_width - 40

            for idx, bonus in enumerate(general_info['bonus']):
                if idx > 0:
                    draw_wave_separator(card_surface, 20, effect_y - 8, card_width - 40)
                
                color = (150, 255, 150) if '(Passive)' in bonus else (255, 255, 150)
                wrapped_lines = wrap_text(bonus, self.fonts['mini'], max_effect_width)
                
                for line in wrapped_lines:
                    effect_surface = self.fonts['mini'].render(line, True, color)
                    effect_rect = effect_surface.get_rect(centerx=card_width//2)
                    effect_rect.top = effect_y
                    card_surface.blit(effect_surface, effect_rect)
                    effect_y += 20  
                
                effect_y += 5 
                if ((self.current_selecting_player == 1 and self.player1_general == general_id) or
                    (self.current_selecting_player == 2 and self.player2_general == general_id)):
                    pygame.draw.rect(card_surface, (255, 215, 0), 
                                card_surface.get_rect(), 2)
                
                self.screen.blit(card_surface, (x, y))
        
        button_width = 200
        button_height = 40  
        button_y = screen_height - button_height - 10  
        
        cancel_button = pygame.Rect(
            20, button_y, button_width, button_height) 
         
        pygame.draw.rect(self.screen, (180, 30, 30), cancel_button, border_radius=10)
        cancel_text = self.fonts['small'].render("Cancel Selection", True, (255, 255, 255))
        cancel_rect = cancel_text.get_rect(center=cancel_button.center)
        self.screen.blit(cancel_text, cancel_rect)
        
        nav_text = "Next Player" if self.current_selecting_player == 1 else "Previous Player"
        nav_button = pygame.Rect(
            screen_width - button_width - 20, button_y, button_width, button_height)
        
        pygame.draw.rect(self.screen, (30, 180, 30), nav_button, border_radius=10)
        nav_text_surf = self.fonts['small'].render(nav_text, True, (255, 255, 255))
        nav_rect = nav_text_surf.get_rect(center=nav_button.center)
        self.screen.blit(nav_text_surf, nav_rect)
        
        if self.player1_general and self.player2_general:
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
        Handles general selection and navigation

        Args:
            pos (tuple): The position of the mouse cursor
        """

        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        button_width = 200
        button_height = 40
        button_y = screen_height - button_height - 20

        cancel_button = pygame.Rect(20, button_y, button_width, button_height)
        if cancel_button.collidepoint(pos):
            if self.current_selecting_player == 1:
                self.player1_general = None
            else:
                self.player2_general = None
            return

        nav_button = pygame.Rect(screen_width - button_width - 20, button_y, button_width, button_height)
        if nav_button.collidepoint(pos):
            if self.current_selecting_player == 1 and self.player1_general:
                self.current_selecting_player = 2
            elif self.current_selecting_player == 2:
                self.current_selecting_player = 1
            return

        if self.player1_general and self.player2_general:
            proceed_button = pygame.Rect(
                (screen_width - button_width) // 2,
                button_y,
                button_width,
                button_height
            )
            if proceed_button.collidepoint(pos):
                self.state = "map_select"
                return

        card_width = min(screen_width // 3.5, 280)
        card_height = int(card_width * 1.6)
        spacing = 30
        
        player_text = self.fonts['normal'].render(f"Player {self.current_selecting_player}'s Selection", 
                                                True, (255, 255, 255))
        player_rect = player_text.get_rect(centerx=screen_width//2, top=80)
        start_x = (screen_width - (card_width * 3 + spacing * 2)) // 2
        start_y = player_rect.bottom + 20

        for i, general_id in enumerate(self.generals.keys()):
            col = i % 3
            row = i // 3
            x = start_x + col * (card_width + spacing)
            y = start_y + row * (card_height + spacing)
            
            card_rect = pygame.Rect(x, y, card_width, card_height)
            if card_rect.collidepoint(pos):
                if self.current_selecting_player == 1:
                    if general_id != self.player2_general:
                        self.player1_general = general_id
                else:
                    if general_id != self.player1_general:
                        self.player2_general = general_id
                break
        
    def setup_resources(self):
        
        """
        Setup game resources and assets
        """

        self.original_menu_image = pygame.image.load(os.path.join("..", "assets", "images", "menu_image.png"))
        self.menu_image = self._scale_image_to_screen()
        
        self.fonts = {
            'title': pygame.font.Font(None, 100),
            'normal': pygame.font.Font(None, 74),
            'small': pygame.font.Font(None, 36),
            'mini': pygame.font.Font(None, 20)
        }

    def setup_audio(self):

        """
        Setup game audio and music
        """

        self.music_enabled = True
        self.sound_enabled = True
        self.music_volume = 0.7
        self.sound_volume = 0.7
        
        pygame.mixer.music.load(os.path.join("..", "assets", "sounds", "music", "menu_music.ogg"))
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(-1)

    def setup_ui_elements(self):
        
        """
        Setup game UI elements and buttons
        """

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
                lambda: self.change_state("general_selection")  
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
        
        """
        Setup game options and buttons
        """

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
        
        """
        Setup game map buttons
        """

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
                lambda: self.handle_map_selection(1)
            ),
            "map2": Button(
                (screen_width - button_width) // 2,
                screen_height // 2 + button_spacing // 2,
                button_width,
                button_height,
                "Map 2",
                lambda: self.handle_map_selection(2)
            )
        }

    def toggle_sound(self, enabled):
        
        """
        Enables sound
        """

        self.sound_enabled = enabled

    def toggle_music(self, enabled):
        
        """
        Enables or disables the background music 
        """

        self.music_enabled = enabled
        if enabled:
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()

    def set_sound_volume(self, volume):
        
        """
        Controls the sound volume
        """

        self.sound_volume = volume

    def set_music_volume(self, volume):
        
        """
        Controls the music volume
        """

        self.music_volume = volume
        pygame.mixer.music.set_volume(volume)

    def start_tutorial(self):
        
        """
        Activates the tutorial
        """

        self.tutorial.active = True
        self.tutorial.current_page = 0

    def change_state(self, new_state):
        
        """
        Change the state of the menu and setup the appropriate UI elements
        """

        self.state = new_state
        
        if new_state == "map_select":
            self.setup_map_buttons()
        elif new_state == "general_selection":
            self.player1_general = None
            self.player2_general = None
            self.current_selecting_player = 1
        elif new_state == "game_map1" or new_state == "game_map2":
            if self.player1_general:
                for unit in self.game.units1:
                    if unit.has_general:
                        unit.general_id = self.player1_general
            if self.player2_general:
                for unit in self.game.units2:
                    if unit.has_general:
                        unit.general_id = self.player2_general
    
        return new_state

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
            elif self.state == "general_selection":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_general_selection(event.pos)
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
        
        """
        Draws information to the screen
        """

        self.screen.blit(self.menu_image, (0, 0))
        
        if self.state == "main":
            self._draw_main_menu()
        elif self.state == "options":
            self._draw_options_menu()
        elif self.state == "general_selection":
            self.draw_general_selection()
        elif self.state == "map_select":
            self._draw_map_selection()
            
        if self.tutorial.active:
            self.tutorial.draw()
            
        pygame.display.flip()

    def _draw_main_menu(self):
        
        """
        Draws the main menu to the screen
        """

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
        
        """
        Draws the options menu to the screen
        """

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
        Changes the state of the menu
        """

        self.state = new_state
        if new_state == "map_select":
            self.setup_map_buttons()
        elif new_state == "general_selection":
            self.player1_general = None
            self.player2_general = None
            self.current_selecting_player = 1
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
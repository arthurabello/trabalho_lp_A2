"""
UI components for the menu system.
"""

import pygame

class Button:
    def __init__(self, x, y, width, height, text, callback, border_radius=10, fontsize=36) -> None:

        """
        Initialize button component. 

        Args:
            x (int): X-coordinate of the top-left corner of the button.
            y (int): Y-coordinate of the top-left corner of the button.
            width (int): Width of the button.
            height (int): Height of the button.
            text (str): Text to display on the button.
            callback (function): Callback function to be called when the button is clicked.
            border_radius (int, optional): Border radius of the button. Defaults to 10.
            fontsize (int, optional): Font size of the text. Defaults to 36.
        """

        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.border_radius = border_radius
        self.font = pygame.font.Font(None, fontsize)
        
        self.colors = {
            'default': (45, 45, 48),
            'hover': (70, 70, 75),
            'text': (255, 255, 255)
        }
        self.color_current = self.colors['default']

    def draw(self, screen) -> None:

        """
        Draw button on screen.
        
        Args:
            screen (pygame.Surface): Surface to draw the button on.
        """
        pygame.draw.rect(screen, self.color_current, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(screen, self.colors['text'], self.rect, 2, border_radius=self.border_radius)
        
        text_surface = self.font.render(self.text.capitalize(), True, self.colors['text'])
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event) -> bool:

        """
        Handle button events.

        Args:
            event (pygame.event.Event): Event to handle.
        
        Returns:
            bool: True if the button was clicked, False otherwise.
        """

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()
                return True
        elif event.type == pygame.MOUSEMOTION:
            self.color_current = self.colors['hover'] if self.rect.collidepoint(event.pos) else self.colors['default']
        return False

class ToggleButton:
    def __init__(self, x, y, size, initial_state, callback) -> None:

        """
        Initialize toggle button component.

        Args:
            x (int): X-coordinate of the top-left corner of the button.
            y (int): Y-coordinate of the top-left corner of the button.
            size (int): Size of the button.
            initial_state (bool): Initial state of the button.
            callback (function): Callback function to be called when the button is clicked.
        """

        self.rect = pygame.Rect(x, y, size, size)
        self.callback = callback
        self.state = initial_state
        self.font = pygame.font.Font(None, 24)
        
        self.colors = {
            'enabled': (76, 175, 80),
            'disabled': (244, 67, 54),
            'text': (255, 255, 255)
        }

    def draw(self, screen) -> None:

        """
        Draw toggle button on screen.
        
        Args:
            screen (pygame.Surface): Surface to draw the button on.
        """

        color = self.colors['enabled'] if self.state else self.colors['disabled']
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        
        text = "ON" if self.state else "OFF"
        text_surface = self.font.render(text, True, self.colors['text'])
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event) -> bool:

        """
        Handle toggle button events.
        
        Args:
            event (pygame.event.Event): Event to handle.
        
        Returns:
            bool: True if the button was clicked, False otherwise.
        """

        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.state = not self.state
            self.callback(self.state)
            return True
        return False

class Slider:
    def __init__(self, x, y, width, height, initial_value, callback) -> None:

        """
        Initialize slider component.

        Args:
            x (int): X-coordinate of the top-left corner of the slider.
            y (int): Y-coordinate of the top-left corner of the slider.
            width (int): Width of the slider.
            height (int): Height of the slider.
            initial_value (float): Initial value of the slider.
            callback (function): Callback function to be called when the slider is moved.
        """

        self.rect = pygame.Rect(x, y, width, height)
        self.callback = callback
        self.value = initial_value
        self.dragging = False
        
        self.colors = {
            'background': (70, 70, 75),
            'fill': (76, 175, 80),
            'handle': (120, 120, 125)
        }

    def draw(self, screen) -> None:

        """
        Draw slider on screen.
        
        Args:
            screen (pygame.Surface): Surface to draw the slider on.
        """

        pygame.draw.rect(screen, self.colors['background'], self.rect, border_radius=4)
        
        fill_rect = self.rect.copy()
        fill_rect.width *= self.value
        pygame.draw.rect(screen, self.colors['fill'], fill_rect, border_radius=4)

        handle_pos = self.rect.x + (self.rect.width * self.value)
        handle_rect = pygame.Rect(handle_pos - 8, self.rect.y - 6, 16, 20)
        pygame.draw.rect(screen, self.colors['handle'], handle_rect, border_radius=5)

    def handle_event(self, event) -> bool:

        """
        Handle slider events.
        
        Args:
            event (pygame.event.Event): Event to handle.
        
        Returns:
            bool: True if the slider was moved, False otherwise.
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

class GeneralCard:
    def __init__(self, general_id, info, x, y, width, height, fonts, sprite, selected=False) -> None:

        """
        Initialize general card component.

        Args:
            general_id (int): ID of the general.
            info (dict): Information about the general.
            x (int): X-coordinate of the top-left corner of the card.
            y (int): Y-coordinate of the top-left corner of the card.
            width (int): Width of the card.
            height (int): Height of the card.
            fonts (dict): Dictionary of fonts.
            sprite (pygame.Surface): Sprite of the general.
            selected (bool, optional): Whether the card is selected. Defaults to False.
        """

        self.general_id = general_id
        self.info = info
        self.rect = pygame.Rect(x, y, width, height)
        self.selected = selected
        self.fonts = fonts
        self.sprite = sprite
        
        self.colors = {
            'background': (40, 40, 45),
            'selected_border': (255, 215, 0),
            'title': (255, 215, 0),
            'passive': (150, 255, 150),
            'active': (255, 255, 150)
        }

    def draw(self, screen) -> None:

        """
        Draw general card on screen.
        
        Args:
            screen (pygame.Surface): Surface to draw the card on.
        """

        card_surface = pygame.Surface((self.rect.width, self.rect.height))
        card_surface.fill(self.colors['background'])
        
        portrait_size = int(self.rect.width * 0.7)
        portrait_x = (self.rect.width - portrait_size) // 2
        portrait_rect = pygame.Rect(portrait_x, 15, portrait_size, portrait_size)
        pygame.draw.rect(card_surface, (30, 30, 35), portrait_rect)
        
        if self.sprite:
            portrait = pygame.transform.scale(self.sprite, (portrait_size, portrait_size))
            card_surface.blit(portrait, (portrait_x, 15))
        
        text_start_y = portrait_rect.bottom + 15
        name_lines = self._wrap_text(self.info['name'], self.fonts['small'], self.rect.width - 20)
        
        for idx, line in enumerate(name_lines):
            name_surface = self.fonts['small'].render(line, True, self.colors['title'])
            name_rect = name_surface.get_rect(
                centerx=self.rect.width//2,
                top=text_start_y + idx * 25
            )
            card_surface.blit(name_surface, name_rect)

        effect_y = text_start_y + len(name_lines) * 22 + 15
        
        for idx, bonus in enumerate(self.info['bonus']):
            if idx > 0:
                self._draw_separator(card_surface, 20, effect_y - 8, self.rect.width - 40)
            
            color = self.colors['passive'] if '(Passive)' in bonus else self.colors['active']
            wrapped_lines = self._wrap_text(bonus, self.fonts['mini'], self.rect.width - 40)
            
            for line in wrapped_lines:
                effect_surface = self.fonts['mini'].render(line, True, color)
                effect_rect = effect_surface.get_rect(centerx=self.rect.width//2)
                effect_rect.top = effect_y
                card_surface.blit(effect_surface, effect_rect)
                effect_y += 20
            
            effect_y += 5

        if self.selected:
            pygame.draw.rect(card_surface, self.colors['selected_border'], 
                           card_surface.get_rect(), 2)
        
        screen.blit(card_surface, self.rect)

    def _wrap_text(self, text, font, max_width) -> list:

        """
        Wrap text to fit within a given width.
        
        Args:
            text (str): Text to wrap.
            font (pygame.font.Font): Font to use for wrapping.
            max_width (int): Maximum width for wrapping.
        
        Returns:
            list: Wrapped text lines.
        """

        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            text_surface = font.render(' '.join(current_line), True, (255, 255, 255))
            if text_surface.get_width() > max_width:
                current_line.pop()
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        return lines

    def _draw_separator(self, surface, x, y, width) -> None:

        """
        Draw a separator line on the surface.
        
        Args:
            surface (pygame.Surface): Surface to draw the separator on.
            x (int): X position of the separator.
            y (int): Y position of the separator.
            width (int): Width of the separator.
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

    def handle_event(self, event) -> bool:

        """
        Handle card events.
        
        Args:
            event (pygame.event.Event): Event to handle.
        
        Returns:
            bool: True if the card was clicked, False otherwise.
        """
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.rect.collidepoint(event.pos)
        return False
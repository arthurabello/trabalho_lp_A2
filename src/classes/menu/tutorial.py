"""
This module handles the tutorial system for Warbound, displaying game instructions in a book-like format.
"""

import pygame

class Tutorial:
    def __init__(self, screen):
        """
        Initialize the tutorial system.
        
        Args:
            screen (pygame.Surface): The game screen to draw on
        """
        self.screen = screen
        self.active = False
        self.current_page = 0
        self.font_title = pygame.font.Font(None, 48)
        self.font_text = pygame.font.Font(None, 36)
        
        self.pages = [
            {
                "title": "How to Play",
                "content": "Warbound is blablabla..."  
            },
        ]
        
        screen_width, screen_height = screen.get_size()
        self.window_width = int(screen_width * 0.8)
        self.window_height = int(screen_height * 0.8)
        self.window_x = (screen_width - self.window_width) // 2
        self.window_y = (screen_height - self.window_height) // 2
        
        button_width = 100
        button_height = 40
        self.close_button = pygame.Rect(
            self.window_x + self.window_width - 40, 
            self.window_y + 10, 
            30, 
            30
        )
        self.prev_button = pygame.Rect(
            self.window_x + 20,
            self.window_y + self.window_height - 60,
            button_width,
            button_height
        )
        self.next_button = pygame.Rect(
            self.window_x + self.window_width - button_width - 20,
            self.window_y + self.window_height - 60,
            button_width,
            button_height
        )
        
        self.colors = {
            'background': (245, 245, 220), 
            'border': (139, 69, 19),     
            'text': (0, 0, 0),            
            'button': (210, 180, 140),   
            'button_hover': (188, 143, 143),
            'button_text': (0, 0, 0)     
        }

    def add_page(self, title, content):

        """
        Add a new page to the tutorial.
        
        Args:
            title (str): Title of the page
            content (str): Content text for the page
        """

        self.pages.append({
            "title": title,
            "content": content
        })

    def handle_event(self, event):

        """
        Handle tutorial events (button clicks, etc.).
        
        Args:
            event (pygame.Event): The event to handle
            
        Returns:
            str: Action to take ('menu' if tutorial should close, None otherwise)
        """

        if not self.active:
            return None
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if self.close_button.collidepoint(mouse_pos):
                self.active = False
                return 'menu'
                
            if self.prev_button.collidepoint(mouse_pos) and self.current_page > 0:
                self.current_page -= 1
                
            if self.next_button.collidepoint(mouse_pos) and self.current_page < len(self.pages) - 1:
                self.current_page += 1
                
        return None

    def draw(self):

        """
        Draw the tutorial window and content.
        """

        if not self.active:
            return
            
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        pygame.draw.rect(self.screen, self.colors['background'], 
                        (self.window_x, self.window_y, self.window_width, self.window_height))
        pygame.draw.rect(self.screen, self.colors['border'],
                        (self.window_x, self.window_y, self.window_width, self.window_height), 3)
        
        pygame.draw.rect(self.screen, self.colors['button'], self.close_button)
        close_text = self.font_text.render('×', True, self.colors['button_text'])
        self.screen.blit(close_text, (self.close_button.centerx - 8, self.close_button.centery - 12))
        
        if self.current_page < len(self.pages):
            page = self.pages[self.current_page]
            
            title_surface = self.font_title.render(page['title'], True, self.colors['text'])
            title_rect = title_surface.get_rect(centerx=self.window_x + self.window_width//2,
                                              top=self.window_y + 30)
            self.screen.blit(title_surface, title_rect)
            
            words = page['content'].split()
            line_spacing = 36
            x = self.window_x + 50
            y = self.window_y + 100
            
            line = []
            for word in words:
                line.append(word)
                text_surface = self.font_text.render(' '.join(line), True, self.colors['text'])
                if text_surface.get_width() > self.window_width - 100:  
                    line.pop()  
                    text_surface = self.font_text.render(' '.join(line), True, self.colors['text'])
                    self.screen.blit(text_surface, (x, y))
                    y += line_spacing
                    line = [word] 
            
            if line:
                text_surface = self.font_text.render(' '.join(line), True, self.colors['text'])
                self.screen.blit(text_surface, (x, y))
                mouse_pos = pygame.mouse.get_pos()
        
        if self.current_page > 0:
            button_color = self.colors['button_hover'] if self.prev_button.collidepoint(mouse_pos) else self.colors['button']
            pygame.draw.rect(self.screen, button_color, self.prev_button)
            prev_text = self.font_text.render('<<', True, self.colors['button_text'])
            self.screen.blit(prev_text, (self.prev_button.centerx - 16, self.prev_button.centery - 12))
            
        if self.current_page < len(self.pages) - 1:
            button_color = self.colors['button_hover'] if self.next_button.collidepoint(mouse_pos) else self.colors['button']
            pygame.draw.rect(self.screen, button_color, self.next_button)
            next_text = self.font_text.render('>>', True, self.colors['button_text'])
            self.screen.blit(next_text, (self.next_button.centerx - 16, self.next_button.centery - 12))
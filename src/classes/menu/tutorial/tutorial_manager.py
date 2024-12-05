"""
Manages the tutorial system.
"""

import pygame

class TutorialManager:
    def __init__(self, screen):
        
        """
        Initialize tutorial system.

        Args:
            screen (pygame.Surface): Game window surface.
        """

        self.screen = screen
        self.active = False
        self.current_page = 0
        self.setup_fonts()
        self.setup_colors()
        self.setup_tutorial_content()
        self.setup_ui_elements()
        
    def setup_fonts(self):
        
        """
        Initialize fonts.
        """

        self.font_title = pygame.font.Font(None, 48)
        self.font_text = pygame.font.Font(None, 36)
        
    def setup_colors(self):
        
        """
        Setup color scheme.
        """

        self.colors = {
            'background': (245, 245, 220),
            'border': (139, 69, 19),
            'text': (0, 0, 0),
            'button': (210, 180, 140),
            'button_hover': (188, 143, 143),
            'button_text': (0, 0, 0)
        }
        
    def setup_tutorial_content(self):
        
        """
        Setup tutorial pages content.
        """

        self.pages = [
        {
            "title": "About Warbound",
            "content": [
                "Warbound is a turn-based strategy game where players command armies on a battlefield.",
                "Your objective is to defeat the enemy by eliminating their general or destroying their entire army.",
                "The game combines tactical positioning, unit management, and strategic decision-making."
            ]
        },
        {
            "title": "General Selection",
            "content": [
                "At the start of the game, choose a historical general who leads your army. Each general brings unique strategic advantages:",
                "- Alexander the Great: Specializes in infantry, particularly Hypaspists. Provides substantial defensive and strength bonuses, with exceptional synergy when Alexander is present.",
                "- Julius Caesar: Enhances legion movement and attack capabilities. Offers passive defense for legions and light cavalry improvements.",
                "- Edward the Elder: Strengthens archers and man-at-arms units, providing significant combat and mobility boosts.",
                "- Charlemagne: Focuses on heavy cavalry, offering defensive advantages and powerful strength enhancements.",
                "- Harald Hardrada: Boosts Viking units and archers, providing robust defensive and offensive capabilities.",
                "- Leonidas: Master of Spartan hoplites, delivering impressive defensive and movement bonuses.",
                "Your general choice significantly impacts your initial army formation and overall battle strategy."
            ]
        },
        {
            "title": "Moving Units",
            "content": [
                "Unit movement in Warbound follows these rules:",
                "- Use mouse to select and move units",
                "- Movements restricted by unit's movement range",
                "- Click unit first, then destination hex",
                "- Cannot move through other units"
                "- Movement through different terrains may consume additional movement points"
            ]
        },
        {
            "title": "Attacking Units: Melee",
            "content": [
                "Melee Units Combat Mechanics:",
                "- Attack range is 1 hex",
                "- Receive counter-attack when attacking",
                "- Close combat involves mutual damage",
                "- Positioning and direction are crucial"
            ]
        },
        {
            "title": "Attacking Units: Ranged",
            "content": [
                "Ranged Units Combat Mechanics:",
                "- Attack range greater than 1 hex",
                "- No counter-attack received",
                "- Can attack from a distance",
                "- Less vulnerable in direct confrontations"
            ]
        },
        {
            "title": "Passing the Turn",
            "content": [
                "Managing Your Turn:",
                "- Press SPACE key to end current turn",
                "- Transfer control to the other player",
                "- Plan your moves carefully before ending turn"
            ]
        },
        {
            "title": "Formation System",
            "content": [
                "Warbound Formations:",
                "- Phalanx: Increases attack, reduces defense",
                "- Turtle: Maximum defensive formation",
                "- Shield Wall: Strong defense against ranged attacks",
                "- V Formation: Balanced attack and defense",
                "- Spread: Good for ranged units",
                "Press 'G' to cycle through formations"
            ]
        },
        {
            "title": "Unit Orientation",
            "content": [
                "Unit Orientation System:",
                "- Four directions: North, South, East, West",
                "- Use directional keys to change orientation",
                "- One orientation change per turn",
                "- Orientation affects combat effectiveness",
                "Attacks from different angles have varied damage modifiers"
            ]
        },
        {
            "title": "Unit Types",
            "content": [
                "Warbound Unit Types:",
                "Melee Units:",
                "- Hoplite",
                "- Legionary",
                "- Viking",
                "- Men-at-Arms",
                "- Hypaspist",
                "- Cavalry",
                "- Heavy Cavalry",
                "\nRanged Units:",
                "- Archer",
                "- Crossbowman"
            ]
        },
        {
            "title": "Combat Mechanics",
            "content": [
                "Damage Calculation Factors:",
                "- Base damage calculation",
                "- Direction modifiers",
                "- Critical hit chances",
                "- Terrain effects",
                "- Unit formation",
                "- General's presence",
                "Damage varies 80-120% of base damage"
            ]
        },
        {
            "title": "Title Game Over",
            "content": [
                "After Losing the Game:",
                "- Press M: Return to main menu"
            ]
        },
        {
            "title": "Pro Tips",
            "content": [
                "Strategic Advice:",
                "- Position your general carefully",
                "- Use terrain to your advantage",
                "- Vary your formations strategically",
                "- Consider unit orientations during combat",
                "Good luck, commander!"
            ]
        }
    ]
        
    def setup_ui_elements(self):
        
        """
        Setup UI elements.
        """

        screen_width, screen_height = self.screen.get_size()
        self.window_width = int(screen_width * 0.8)
        self.window_height = int(screen_height * 0.8)
        self.window_x = (screen_width - self.window_width) // 2
        self.window_y = (screen_height - self.window_height) // 2
        
        self.setup_buttons()
        
    def setup_buttons(self):
        
        """
        Setup navigation buttons.
        """

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
        
    def handle_event(self, event):
        
        """
        Handle tutorial events.
        """

        if not self.active:
            return None

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            if self.close_button.collidepoint(mouse_pos):
                self.active = False
                return 'menu'
                
            if self.prev_button.collidepoint(mouse_pos) and self.current_page > 0:
                self.current_page -= 1
                return None
                
            if self.next_button.collidepoint(mouse_pos) and self.current_page < len(self.pages) - 1:
                self.current_page += 1
                return None
                
        return None
        
    def draw(self):
        
        """
        Draw tutorial window.
        """

        if not self.active:
            return
            
        self._draw_background()
        self._draw_content()
        self._draw_navigation()
        
    def _draw_background(self):
        
        """
        Draw tutorial background.
        """

        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        pygame.draw.rect(
            self.screen,
            self.colors['background'],
            (self.window_x, self.window_y, self.window_width, self.window_height)
        )
        pygame.draw.rect(
            self.screen,
            self.colors['border'],
            (self.window_x, self.window_y, self.window_width, self.window_height),
            3
        )
        
    def _draw_content(self):
        
        """
        Draw tutorial content.
        """

        if self.current_page >= len(self.pages):
            return
            
        page = self.pages[self.current_page]
        
        title_surface = self.font_title.render(page['title'], True, self.colors['text'])
        title_rect = title_surface.get_rect(
            centerx=self.window_x + self.window_width//2,
            top=self.window_y + 30
        )
        self.screen.blit(title_surface, title_rect)
        
        self._draw_wrapped_text(page['content'], self.window_y + 100)
        
    def _draw_navigation(self):
        
        """
        Draw navigation buttons.
        """

        mouse_pos = pygame.mouse.get_pos()
        
        pygame.draw.rect(self.screen, self.colors['button'], self.close_button)
        close_text = self.font_text.render('×', True, self.colors['button_text'])
        self.screen.blit(close_text, (self.close_button.centerx - 8, self.close_button.centery - 12))
        
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

    def _draw_wrapped_text(self, content, start_y):
        """
        Draw text with word wrapping.

        Args:
            content (list): List of lines of text.
            start_y (int): Y position to start drawing from.
        """
    
        x = self.window_x + 60
        line_spacing = 36
        indent = 40

        y = start_y
        for line in content:
            is_list_item = line.strip().startswith('-')
            line_x = x + indent if is_list_item else x

            words = line.split()
            current_line = []
            for word in words:
                test_line = ' '.join(current_line + [word])
                text_surface = self.font_text.render(test_line, True, self.colors['text'])
                if text_surface.get_width() > self.window_width - 120:
                    text_surface = self.font_text.render(' '.join(current_line), True, self.colors['text'])
                    self.screen.blit(text_surface, (line_x, y))
                    y += line_spacing
                    current_line = [word]
                else:
                    current_line.append(word)

            if current_line:
                text_surface = self.font_text.render(' '.join(current_line), True, self.colors['text'])
                self.screen.blit(text_surface, (line_x, y))
            y += line_spacing

        return y
        
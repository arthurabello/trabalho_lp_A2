"""
Handles UI element rendering including status panels and overlays.
"""

import pygame
from ...units.base.unit_direction import Direction

class UIRenderer:
    def __init__(self, screen) -> None:

        """
        Initialize the UI renderer.

        Args:
            screen (pygame.Surface): The game screen.
        """

        self.screen = screen
        self.status_surface = pygame.Surface((300, screen.get_height()), pygame.SRCALPHA)
        self.init_fonts()
        self.setup_colors()

    def init_fonts(self) -> None:

        """
        Initialize fonts for UI rendering.
        """

        self.title_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)
        self.mini_font = pygame.font.Font(None, 24)

    def setup_colors(self) -> None:
        
        """
        Setup colors for UI rendering.
        """

        self.colors = {
            'background_top': (31, 41, 55),
            'background_bottom': (17, 24, 39),
            'text': (229, 231, 235),
            'header': (252, 211, 77),
            'section_bg': (31, 41, 55, 128),
            'separator': (75, 85, 99),
            'hp_good': (34, 197, 94),
            'hp_medium': (234, 179, 8),
            'hp_bad': (239, 68, 68),
            'attack': (239, 68, 68),
            'defense': (59, 130, 246),
            'range': (168, 85, 247),
            'section_title': (156, 163, 175)
        }

    def render(self, state_manager) -> None:

        """
        Render the UI status panel.

        Args:
            state_manager (StateManager): The state manager.
        """

        PANEL_WIDTH = 300
        SECTION_PADDING = 15
        height = self.screen.get_height()

        for y in range(height):
            progress = y / height
            r = self.colors['background_top'][0] + (self.colors['background_bottom'][0] - self.colors['background_top'][0]) * progress
            g = self.colors['background_top'][1] + (self.colors['background_bottom'][1] - self.colors['background_top'][1]) * progress
            b = self.colors['background_top'][2] + (self.colors['background_bottom'][2] - self.colors['background_top'][2]) * progress
            pygame.draw.line(self.status_surface, (r, g, b), (0, y), (PANEL_WIDTH, y))

        y_offset = SECTION_PADDING

        header_text = self.title_font.render("Unit Status", True, self.colors['header'])
        header_rect = header_text.get_rect(centerx=PANEL_WIDTH // 2, top=y_offset)
        self.status_surface.blit(header_text, header_rect)

        y_offset += header_rect.height + SECTION_PADDING

        turn_bg = pygame.Surface((PANEL_WIDTH - 40, 60), pygame.SRCALPHA)
        turn_bg.fill(self.colors['section_bg'])
        self.status_surface.blit(turn_bg, (20, y_offset))

        turn_text = f"Player {state_manager.current_player}'s Turn"
        turn_surface = self.small_font.render(turn_text, True, self.colors['header'])
        self.status_surface.blit(turn_surface, (30, y_offset + 10))

        space_text = "Press SPACE to end turn"
        space_surface = self.mini_font.render(space_text, True, self.colors['text'])
        self.status_surface.blit(space_surface, (30, y_offset + 35))

        y_offset += 80
        y_offset += header_rect.height + SECTION_PADDING
        pygame.draw.line(self.status_surface, self.colors['separator'], 
                        (20, y_offset), (PANEL_WIDTH - 20, y_offset))
        y_offset += SECTION_PADDING

        if not state_manager.selected_unit:
            no_unit_text = self.mini_font.render("No Unit Selected", True, self.colors['text'])
            no_unit_rect = no_unit_text.get_rect(centerx=PANEL_WIDTH // 2, top=y_offset)
            self.status_surface.blit(no_unit_text, no_unit_rect)
        else:
            unit = state_manager.selected_unit
            self._draw_unit_section(unit, state_manager, y_offset, PANEL_WIDTH)

        status_x = self.screen.get_width() - 300
        self.screen.blit(self.status_surface, (status_x, 0))

    def _draw_unit_section(self, unit, state_manager, y_offset, PANEL_WIDTH) -> None:

        """
        Draw a section of the UI status panel for a unit.

        Args:
            unit (Unit): The unit to draw the section for.
            state_manager (StateManager): The state manager.
            y_offset (int): The y-coordinate of the top of the section.
            PANEL_WIDTH (int): The width of the panel.
        """

        section_bg = pygame.Surface((PANEL_WIDTH - 40, 80), pygame.SRCALPHA)
        section_bg.fill(self.colors['section_bg'])
        self.status_surface.blit(section_bg, (20, y_offset))

        type_text = self.small_font.render(unit.__class__.__name__, True, self.colors['header'])
        self.status_surface.blit(type_text, (30, y_offset + 10))

        hp_percent = (unit.current_hp / unit.max_hp) * 100
        hp_text = self.mini_font.render(f"HP: {hp_percent:.1f}%", True, self.colors['text'])
        self.status_surface.blit(hp_text, (30, y_offset + 40))

        pygame.draw.rect(self.status_surface, self.colors['separator'],
                        (30, y_offset + 60, PANEL_WIDTH - 60, 8))

        hp_color = (self.colors['hp_good'] if hp_percent > 70 else 
                   self.colors['hp_medium'] if hp_percent > 30 else 
                   self.colors['hp_bad'])
        hp_width = int((PANEL_WIDTH - 60) * (hp_percent / 100))
        pygame.draw.rect(self.status_surface, hp_color,
                        (30, y_offset + 60, hp_width, 8))

        y_offset += 100

        section_bg = pygame.Surface((PANEL_WIDTH - 40, 120), pygame.SRCALPHA)
        section_bg.fill(self.colors['section_bg'])
        self.status_surface.blit(section_bg, (20, y_offset))

        section_title = self.mini_font.render("COMBAT STATS", True, self.colors['section_title'])
        self.status_surface.blit(section_title, (30, y_offset + 10))

        stats_y = y_offset + 40
        stats_data = [
            (f"Attack Points: {unit.attack_points}", self.colors['attack']),
            (f"Defense Points: {unit.defense_points}", self.colors['defense']),
            (f"Attack Range: {unit.attack_range}", self.colors['range'])
        ]

        for text, color in stats_data:
            stat_text = self.mini_font.render(text, True, color)
            self.status_surface.blit(stat_text, (30, stats_y))
            stats_y += 25

        y_offset += 140

        section_bg = pygame.Surface((PANEL_WIDTH - 40, 120), pygame.SRCALPHA)
        section_bg.fill(self.colors['section_bg'])
        self.status_surface.blit(section_bg, (20, y_offset))

        section_title = self.mini_font.render("TACTICAL INFO", True, self.colors['section_title'])
        self.status_surface.blit(section_title, (30, y_offset + 10))

        facing_text = Direction.to_string(unit.facing_direction)

        tactical_y = y_offset + 40
        tactical_data = [
            (f"Movement Points: {state_manager.movement_points[unit]}", self.colors['text']),
            (f"Formation: {unit.formation}", self.colors['text']),
            (f"Terrain: {unit.terrain if hasattr(unit, 'terrain') else 'plains'}", self.colors['text']),
            (f"Facing: {facing_text}", self.colors['text'])
        ]

        for text, color in tactical_data:
            tact_text = self.mini_font.render(text, True, color)
            self.status_surface.blit(tact_text, (30, tactical_y))
            tactical_y += 25

        y_offset += 140

        self._draw_active_modifiers(unit, y_offset, PANEL_WIDTH)

    def _draw_active_modifiers(self, unit, y_offset, PANEL_WIDTH) -> None:

        """
        Draw the active modifiers section of the UI status panel.

        Args:
            unit (Unit): The unit to draw the modifiers for.
            y_offset (int): The y-coordinate of the top of the section.
            PANEL_WIDTH (int): The width of the panel.
        """

        section_bg = pygame.Surface((PANEL_WIDTH - 40, 180), pygame.SRCALPHA)  # Increased height
        section_bg.fill(self.colors['section_bg'])
        self.status_surface.blit(section_bg, (20, y_offset))

        section_title = self.mini_font.render("ACTIVE MODIFIERS", True, self.colors['section_title'])
        self.status_surface.blit(section_title, (30, y_offset + 10))

        mod_y = y_offset + 40

        # Formation modifiers
        if hasattr(unit, 'formations') and unit.formation in unit.formations:
            formation_mods = unit.formations[unit.formation]
            
            attack_mod = (formation_mods.get('attack_modifier', 1.0) - 1) * 100
            if attack_mod != 0:
                sign = "+" if attack_mod > 0 else ""
                mod_text = f"{sign}{attack_mod:.0f}% Attack ({unit.formation})"
                mod_color = self.colors['hp_good'] if attack_mod > 0 else self.colors['hp_bad']
                mod_surface = self.mini_font.render(mod_text, True, mod_color)
                self.status_surface.blit(mod_surface, (30, mod_y))
                mod_y += 25

            # Defense modifiers with attack type specification
            if unit.formation == "Spread":
                mod_text = f"+20% Ranged Defense (Spread)"
                mod_surface = self.mini_font.render(mod_text, True, self.colors['hp_good'])
                self.status_surface.blit(mod_surface, (30, mod_y))
                mod_y += 25
            elif unit.formation == "Shield Wall":
                mod_surface = self.mini_font.render("+50% Melee Defense (Shield Wall)", True, self.colors['hp_good'])
                self.status_surface.blit(mod_surface, (30, mod_y))
                mod_y += 25
                mod_surface = self.mini_font.render("+150% Ranged Defense (Shield Wall)", True, self.colors['hp_good'])
                self.status_surface.blit(mod_surface, (30, mod_y))
                mod_y += 25
            elif unit.formation == "Phalanx" and unit.attack_type == "melee":
                mod_surface = self.mini_font.render("+300% Frontal Defense (Phalanx)", True, self.colors['hp_good'])
                self.status_surface.blit(mod_surface, (30, mod_y))
                mod_y += 25
                mod_surface = self.mini_font.render("-20% Other Directions (Phalanx)", True, self.colors['hp_bad'])
                self.status_surface.blit(mod_surface, (30, mod_y))
                mod_y += 25
            elif unit.formation == "Turtle" and unit.attack_type == "melee":
                mod_surface = self.mini_font.render("+", True, self.colors['hp_good'])
                self.status_surface.blit(mod_surface, (30, mod_y))
                mod_y += 25
                mod_surface = self.mini_font.render("-20% Other Directions (Phalanx)", True, self.colors['hp_bad'])
                self.status_surface.blit(mod_surface, (30, mod_y))
                mod_y += 25

        # Terrain modifiers with attack type specification
        if hasattr(unit, 'terrain') and unit.terrain:
            if unit.terrain == "mountain":
                if hasattr(unit, 'attack_type'):
                    if unit.attack_type == "melee":
                        mod_text = "+50% Melee Defense (Mountain)"
                    else:
                        mod_text = "+20% Ranged Defense (Mountain)"
                    mod_surface = self.mini_font.render(mod_text, True, self.colors['hp_good'])
                    self.status_surface.blit(mod_surface, (30, mod_y))
                    mod_y += 25
            elif unit.terrain == "forest":
                if hasattr(unit, 'attack_type'):
                    if unit.attack_type == "ranged":
                        mod_text = "+70% Ranged Defense (Forest)"
                    else:
                        mod_text = "+25% Melee Defense (Forest)"
                    mod_surface = self.mini_font.render(mod_text, True, self.colors['hp_good'])
                    self.status_surface.blit(mod_surface, (30, mod_y))
                    mod_y += 25

        # Add attack type info
        attack_type_text = f"Attack Type: {unit.attack_type.capitalize()}"
        attack_surface = self.mini_font.render(attack_type_text, True, self.colors['text'])
        self.status_surface.blit(attack_surface, (30, mod_y))
        mod_y += 25


        self._draw_compass(unit, y_offset + 200, PANEL_WIDTH)

    def _draw_compass(self, unit, y_offset, PANEL_WIDTH) -> None:

        """
        Draw the compass on the UI status panel.

        Args:
            unit (Unit): The unit to draw the compass for.
            y_offset (int): The y-coordinate of the top of the compass.
            PANEL_WIDTH (int): The width of the panel.
        """
        
        center_x = PANEL_WIDTH // 2
        compass_size = 70

        directions = ['NORTH', 'EAST', 'SOUTH', 'WEST']
        current_direction = unit.facing_direction if hasattr(unit, 'facing_direction') else 'WEST'
        
        points = {
            'NORTH': [(center_x, y_offset), 
                     (center_x + 15, y_offset + 35), 
                     (center_x, y_offset + 30),
                     (center_x - 15, y_offset + 35)],
            'EAST': [(center_x + 50, y_offset + 50),
                    (center_x + 15, y_offset + 65),
                    (center_x + 20, y_offset + 50),
                    (center_x + 15, y_offset + 35)],
            'SOUTH': [(center_x, y_offset + 100),
                     (center_x + 15, y_offset + 65),
                     (center_x, y_offset + 70),
                     (center_x - 15, y_offset + 65)],
            'WEST': [(center_x - 50, y_offset + 50),
                    (center_x - 15, y_offset + 65),
                    (center_x - 20, y_offset + 50),
                    (center_x - 15, y_offset + 35)]
        }

        for direction, point_list in points.items():
            is_current = Direction[direction] == current_direction
            color = (252, 211, 77) if is_current else self.colors['text']
            pygame.draw.polygon(self.status_surface, color, point_list)

        pygame.draw.circle(self.status_surface, (55, 65, 81), (center_x, y_offset + 50), 3)
        pygame.draw.circle(self.status_surface, self.colors['header'], (center_x, y_offset + 50), 3, 1)

        direction_labels = [
            ('NORTH', 'N', center_x, y_offset - 10),
            ('EAST', 'E', center_x + 60, y_offset + 55),
            ('SOUTH', 'S', center_x, y_offset + 110),
            ('WEST', 'W', center_x - 60, y_offset + 55)
        ]

        for direction, label, x, y in direction_labels:
            is_current = Direction[direction] == current_direction
            color = (252, 211, 77) if is_current else self.colors['text']
            text = self.small_font.render(label, True, color)
            text_rect = text.get_rect(center=(x, y))
            self.status_surface.blit(text, text_rect)
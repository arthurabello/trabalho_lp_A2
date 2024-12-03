"""
Handles UI element rendering including status panels and overlays.
"""

import pygame

class UIRenderer:
    def __init__(self, screen):
        """Initialize UI renderer."""
        self.screen = screen
        self.status_surface = pygame.Surface((300, screen.get_height()))
        self.init_fonts()
        self.setup_colors()

    def init_fonts(self):
        """Initialize fonts for UI elements."""
        self.title_font = pygame.font.Font(None, 48)
        self.header_font = pygame.font.Font(None, 36)
        self.stats_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 24)

    def setup_colors(self):
        """Setup color schemes for UI."""
        self.colors = {
            'background': (17, 24, 39),
            'text': (229, 231, 235),
            'title': (255, 215, 0),  
            'section_header': (156, 163, 175),  
            'hp_bar': (34, 197, 94),  
            'attack': (239, 68, 68),  
            'defense': (147, 51, 234),  
            'missile_defense': (59, 130, 246),  
            'positive_modifier': (34, 197, 94), 
            'negative_modifier': (239, 68, 68),  
            'section_bg': (31, 41, 55)
        }

    def render(self, state_manager):
        """Render all UI elements."""
        self.status_surface.fill(self.colors['background'])
        
        if state_manager.selected_unit:
            self._draw_unit_status(state_manager.selected_unit)
        else:
            self._draw_no_selection()

        self._draw_turn_info(state_manager)
        status_x = self.screen.get_width() - 300
        self.screen.blit(self.status_surface, (status_x, 0))

    def _draw_unit_status(self, unit):
        """Draw complete unit status panel."""
        y_offset = 20
        
        title = self.title_font.render("Unit Status", True, self.colors['title'])
        title_rect = title.get_rect(centerx=150, top=y_offset)
        self.status_surface.blit(title, title_rect)
        y_offset = title_rect.bottom + 20
        y_offset = self._draw_unit_header(unit, y_offset)
        y_offset = self._draw_combat_stats(unit, y_offset)
        y_offset = self._draw_tactical_info(unit, y_offset)
        self._draw_active_modifiers(unit, y_offset)

    def _draw_unit_header(self, unit, y_offset):
        """Draw unit name and health bar."""
        name_text = self.header_font.render(unit.__class__.__name__, True, self.colors['text'])
        name_rect = name_text.get_rect(x=20, top=y_offset)
        self.status_surface.blit(name_text, name_rect)
        y_offset = name_rect.bottom + 10

        health_percent = unit.current_hp / unit.max_hp
        bar_width = 260
        bar_height = 20
        
        pygame.draw.rect(self.status_surface, (31, 41, 55),(20, y_offset, bar_width, bar_height))
        health_width = int(bar_width * health_percent)
        pygame.draw.rect(self.status_surface, self.colors['hp_bar'],(20, y_offset, health_width, bar_height))
        
        health_text = f"{unit.current_hp:.1f}%"
        health_surface = self.stats_font.render(health_text, True, self.colors['text'])
        health_rect = health_surface.get_rect(center=(150, y_offset + bar_height/2))
        self.status_surface.blit(health_surface, health_rect)
        
        return y_offset + bar_height + 20

    def _draw_tactical_info(self, unit, y_offset):
        """Draw tactical information section."""
        header = self.header_font.render("TACTICAL INFO", True, self.colors['section_header'])
        header_rect = header.get_rect(x=20, top=y_offset)
        self.status_surface.blit(header, header_rect)
        y_offset = header_rect.bottom + 10

        info = [
            f"Movement Points: {unit.movement_range}",
            f"Formation: {unit.formation}",
            f"Terrain: {unit.terrain if hasattr(unit, 'terrain') else 'plains'}"
        ]

        for text in info:
            info_surface = self.stats_font.render(text, True, self.colors['text'])
            self.status_surface.blit(info_surface, (30, y_offset))
            y_offset += 25

        return y_offset + 10

    def _draw_no_selection(self):
        """Draw the no unit selected state."""
        text = self.header_font.render("No Unit Selected", True, self.colors['text'])
        text_rect = text.get_rect(center=(150, 150))
        self.status_surface.blit(text, text_rect)

    def _draw_turn_info(self, state_manager):
        """Draw turn information at the bottom."""
        height = self.status_surface.get_height()
        pygame.draw.rect(self.status_surface, self.colors['section_bg'],
                        (0, height-80, 300, 80))
        
        turn_text = f"Player {state_manager.current_player}'s Turn"
        turn_surface = self.header_font.render(turn_text, True, self.colors['text'])
        turn_rect = turn_surface.get_rect(centerx=150, bottom=height-30)
        
        space_text = "Press SPACE to end turn"
        space_surface = self.small_font.render(space_text, True, self.colors['text'])
        space_rect = space_surface.get_rect(centerx=150, bottom=height-10)
        
        self.status_surface.blit(turn_surface, turn_rect)
        self.status_surface.blit(space_surface, space_rect)
    

    def _draw_combat_stats(self, unit, y_offset):
        """Draw combat statistics section."""
        header = self.header_font.render("COMBAT STATS", True, self.colors['section_header'])
        header_rect = header.get_rect(x=20, top=y_offset)
        self.status_surface.blit(header, header_rect)
        y_offset = header_rect.bottom + 10

        attack_mod = unit.attack_points if hasattr(unit, 'attack_points') else unit.base_attack
        defense_mod = unit.defense_points if hasattr(unit, 'defense_points') else unit.base_defense

        stats = [
            (f"Attack Points: {attack_mod}", self.colors['attack']),
            (f"Defense Points: {defense_mod}", self.colors['defense']),
            (f"Attack Range: {unit.attack_range}", self.colors['text'])
        ]

        for text, color in stats:
            stat_surface = self.stats_font.render(text, True, color)
            self.status_surface.blit(stat_surface, (30, y_offset))
            y_offset += 25

        return y_offset + 10

    def _draw_active_modifiers(self, unit, y_offset):
        """Draw active modifiers section."""
        header = self.header_font.render("ACTIVE MODIFIERS", True, self.colors['section_header'])
        header_rect = header.get_rect(x=20, top=y_offset)
        self.status_surface.blit(header, header_rect)
        y_offset = header_rect.bottom + 10

        modifiers = []
        
        if hasattr(unit, 'formations') and unit.formation in unit.formations:
            formation_mods = unit.formations[unit.formation]
            for name, value in formation_mods.items():
                modifier = (value - 1.0) * 100  
                if modifier != 0:  
                    sign = '+' if modifier > 0 else ''
                    color = self.colors['positive_modifier'] if modifier > 0 else self.colors['negative_modifier']
                    text = f"{sign}{modifier:.0f}% {name.replace('_modifier', '')} (Formation)"
                    modifiers.append((text, color))

        if hasattr(unit, 'terrain') and unit.terrain:
            if unit.terrain == "mountain":
                modifiers.append(("+50% Defense vs Melee (Mountain)", self.colors['positive_modifier']))
                modifiers.append(("+20% Defense vs Ranged (Mountain)", self.colors['positive_modifier']))
            elif unit.terrain == "forest":
                modifiers.append(("+70% Defense vs Ranged (Forest)", self.colors['positive_modifier']))
                modifiers.append(("+25% Defense vs Melee (Forest)", self.colors['positive_modifier']))

        if hasattr(unit, 'has_general') and unit.has_general:
            modifiers.append(("+25% Attack (General)", self.colors['positive_modifier']))
            modifiers.append(("+60% Defense (General)", self.colors['positive_modifier']))
            
            if unit.__class__.__name__ == "Hoplite" and unit.general_id == 'leonidas':
                modifiers.append(("+25% Defense (Leonidas)", self.colors['positive_modifier']))

        for text, color in modifiers:
            mod_surface = self.stats_font.render(text, True, color)
            self.status_surface.blit(mod_surface, (30, y_offset))
            y_offset += 25

        if not modifiers:
            no_attack_mod = self.stats_font.render("0% Attack Modifier", True, self.colors['text'])
            no_defense_mod = self.stats_font.render("0% Defense Modifier", True, self.colors['text'])
            self.status_surface.blit(no_attack_mod, (30, y_offset))
            self.status_surface.blit(no_defense_mod, (30, y_offset + 25))

        return y_offset + 10
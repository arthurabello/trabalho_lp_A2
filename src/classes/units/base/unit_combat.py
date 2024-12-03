"""
Combat-related functionality for units.
"""

import random
from .unit_direction import Direction

class UnitCombatMixin:
    def attack(self, target, board):
        """Execute attack against target unit."""
        if not self.is_alive or not target.is_alive or target.player == self.player:
            return

        attack_direction = target._get_attack_direction(self)
        direction_mod = self._get_direction_modifier(attack_direction)
        crit_chance = self._get_crit_chance(attack_direction)

        attack_mod = self._calculate_attack_modifiers()
        defense_mod = target._calculate_defense_modifiers(self, board)
        
        base_damage = (self.base_attack * attack_mod * direction_mod) * (1 - (target.base_defense * defense_mod / 100))
        variation = random.uniform(0.8, 1.2)
        if random.random() < crit_chance:
            variation *= 1.5
            
        final_damage = base_damage * variation
        target.current_hp = max(0, target.current_hp - final_damage)

        if self.attack_type == "melee" and target.attack_type == "melee":
            self._handle_counter_attack(target, attack_direction)
        
        if target.current_hp <= 0:
            target.is_alive = False
        if self.current_hp <= 0:
            self.is_alive = False
            
        self.has_attacked = True
        try:
            self._play_attack_sound()
        except Exception as e:
            print(f"Failed to play attack sound fudeu menor: {str(e)}")

    def _get_direction_modifier(self, attack_direction):
        """Get damage modifier based on attack direction."""
        return {
            "front": 1.0,
            "flank": 1.5,
            "rear": 2.0
        }[attack_direction]

    def _get_crit_chance(self, attack_direction):
        """Get critical hit chance based on attack direction."""
        return {
            "front": 0.05,
            "flank": 0.10,
            "rear": 0.15
        }[attack_direction]

    def _handle_counter_attack(self, target, attack_direction):
        """Handle counter-attack from melee units."""
        counter_mod = {
            "front": 0.6,
            "flank": 0.4,
            "rear": 0.2
        }[attack_direction]
        
        counter_base = (target.base_attack * counter_mod) * (1 - (self.base_defense/100))
        counter_variation = random.uniform(0.8, 1.2)  
        counter_damage = counter_base * counter_variation
        self.current_hp = max(0, self.current_hp - counter_damage)

    def can_attack(self, target_position):
        """
        Check if unit can attack a position.
        
        Args:
            target_position (tuple): Position to check as (row, col)
                
        Returns:
            bool: True if the position is within attack range
        """
        if not self.is_alive:
            return False
                
        row, col = self.position
        target_row, target_col = target_position
        
        row_diff = abs(row - target_row)
        col_diff = abs(col - target_col)
        
        return row_diff <= self.attack_range and col_diff <= self.attack_range
    
    def _play_attack_sound(self):
        """Play attack sound effect."""
        try:
            if hasattr(self, 'attack_sound') and self.attack_sound:
                self.attack_sound.play()
        except Exception as e:
            print(f"Failed to play attack sound: {str(e)}")

    def _calculate_attack_modifiers(self):
        """Calculate total attack modifiers."""
        modifiers = 1.0
        
        if self.has_general:
            modifiers *= 1.25
            
        if self.attack_type == "melee" and self.formation == "Phalanx":
            modifiers *= 1.75
            
        return modifiers

    def _calculate_defense_modifiers(self, attacker, board):
        """Calculate total defense modifiers."""
        modifiers = 1.0
        
        if self.has_general:
            modifiers *= 1.6

        if self.__class__.__name__ == "Hoplite": 
            if self.player == any(unit.player for unit in board.units if unit.has_general and unit.general_id == 'leonidas'):
                modifiers *= 1.1  
                if self.has_general and self.general_id == 'leonidas':
                    modifiers *= 1.15 

        row, col = self.position
        terrain = board.terrain.get((row, col))
        modifiers *= self._get_terrain_modifier(terrain, attacker)

        modifiers *= self._get_formation_modifier(attacker)
                
        return modifiers
    
    def _get_attack_direction(self, attacker):
        """
        Determines the direction of attack relative to the defender's facing direction.
        
        Args:
            attacker (BaseUnit): The unit performing the attack
        
        Returns:
            str: "front", "flank", or "rear" depending on attack direction
        """
        att_row, att_col = attacker.position
        def_row, def_col = self.position
        
        rel_row = def_row - att_row 
        rel_col = def_col - att_col  
        
        match self.facing_direction:
            case Direction.NORTH:
                if rel_row > 0:
                    return "rear"
                elif rel_row < 0:  
                    return "front"
                else:  
                    return "flank"
                    
            case Direction.SOUTH:
                if rel_row < 0: 
                    return "rear"
                elif rel_row > 0: 
                    return "front"
                else:
                    return "flank"
                    
            case Direction.EAST:
                if rel_col < 0:  
                    return "rear"
                elif rel_col > 0: 
                    return "front"
                else:
                    return "flank"
                    
            case Direction.WEST:
                if rel_col > 0: 
                    return "rear"
                elif rel_col < 0: 
                    return "front"
                else:
                    return "flank"
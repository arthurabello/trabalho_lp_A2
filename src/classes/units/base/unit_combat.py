"""
Combat-related functionality for units.
"""

import random
from .unit_direction import Direction

class UnitCombatMixin:
    def _get_damage_variation(self):
        """
        Returns the damage variation specific to a unit based on the general and unit type.
        The variation is a random value within a range determined by the general and unit type.

        Returns:
            float: A random damage variation multiplier, typically between 0.9 and 1.2, 
                  or other specific values depending on the general and unit.
        """
        unit_type = self.__class__.__name__
        general_id = self.general_id if self.has_general else None

        if general_id == 'leonidas' and (unit_type in ['Hoplite', 'Archer']):
            return random.uniform(0.95, 1.2) #THIS IS SPARTA

        if general_id == 'alexander':
            return random.uniform(0.9, 1.1) #normal

        if general_id == 'edward':
            if unit_type == 'Archer':
                return random.uniform(0.92, 1.09) #they have good longbows
            if unit_type == 'MenAtArms':
                return random.uniform(0.8, 1.1) #they are stupid
            return random.uniform(0.9, 1.1)

        if general_id == 'charlemagne':
            if unit_type == 'HeavyCavalry':
                return random.uniform(0.95, 1.17) #they eat good cheese and drink good wine
            return random.uniform(0.9, 1.1)

        if general_id == 'harald':
            if unit_type == 'Viking':
                return random.uniform(0.8, 1.2) #the gods are with them
            if unit_type == 'Archer':
                return random.uniform(0.9, 1.2)
            return random.uniform(0.9, 1.1)

        if general_id == 'julius':
            if unit_type == 'Legionary':
                return random.uniform(0.95, 1.15) #they eat good pecorino cheese
            return random.uniform(0.9, 1.1)

        return random.uniform(0.9, 1.1) #all other mere mortals

    def attack(self, target, board):
        """
        Executes an attack on a target unit.

        The attack calculates modifiers, checks for critical hits, computes the final damage, 
        and applies it to the target unit's health. It also handles counter-attacks if both 
        units are melee fighters.

        Args:
            target (BaseUnit): The unit being attacked.
            board (GameBoard): The game board, which contains the terrain and other state information.
        """
        if not self.is_alive or not target.is_alive or target.player == self.player:
            return

        attack_direction = target._get_attack_direction(self)
        direction_mod = self._get_direction_modifier(attack_direction)
        crit_chance = self._get_crit_chance(attack_direction)

        attack_mod = self._calculate_attack_modifiers()
        defense_mod = target._calculate_defense_modifiers(self, board)
        
        base_attack = self.base_attack * attack_mod * direction_mod
        defense_reduction = min(0.9, (target.base_defense * defense_mod) / 100) 
        base_damage = base_attack * (1 - defense_reduction)  
        
        variation = self._get_damage_variation()
        if random.random() < crit_chance:
            variation *= 1.5 
            
        final_damage = max(0, base_damage * variation)  
        target.current_hp = max(0, min(target.max_hp, target.current_hp - final_damage))  

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
            print(f"Failed to play attack sound: {str(e)}")

    def _get_direction_modifier(self, attack_direction):
        """
        Returns the damage modifier based on the attack direction.

        Args:
            attack_direction (str): The direction of the attack, which can be "front", "flank", or "rear".

        Returns:
            float: A multiplier based on the attack direction.
        """
        return {
            "front": 1.0,
            "flank": 1.5,
            "rear": 2.0
        }[attack_direction]

    def _get_crit_chance(self, attack_direction):
        """
        Returns the critical hit chance based on the attack direction.

        Args:
            attack_direction (str): The direction of the attack, which can be "front", "flank", or "rear".

        Returns:
            float: The chance of a critical hit occurring.
        """
        return {
            "front": 0.05,
            "flank": 0.10,
            "rear": 0.15
        }[attack_direction]

    def _handle_counter_attack(self, target, attack_direction):
        """
        Handles a counter-attack from a melee unit.

        Calculates the counter-attack damage based on the direction of the initial attack 
        and applies it to the attacking unit.

        Args:
            target (BaseUnit): The unit being attacked, which will retaliate.
            attack_direction (str): The direction of the initial attack.
        """
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
        """
        Calculates the attack modifiers based on unit type, general, and formation.

        Considers the general's influence, the unit's type, and any formation bonuses 
        to determine the final attack modifier.

        Returns:
            float: The final attack modifier after considering all factors.
        """
        modifiers = 1.0
        unit_type = self.__class__.__name__
        general_id = self.general_id if self.has_general else None
            
        if general_id == 'alexander' and unit_type == 'Hypaspist':
            if self.formation == 'Phalanx':
                modifiers *= 1.2 
            if self.has_general:
                modifiers *= 1.3  
        
        elif general_id == 'edward':
            if unit_type == 'Archer':
                modifiers *= 1.05 
                if self.has_general:
                    modifiers *= 1.25 
            elif unit_type == 'MenAtArms' and self.has_general:
                modifiers *= 1.25 
        
        elif general_id == 'charlemagne' and unit_type == 'HeavyCavalry':
            if self.has_general:
                modifiers *= 1.35  
        
        elif general_id == 'harald':
            if unit_type == 'Viking':
                if self.has_general:
                    modifiers *= 1.4  
            elif unit_type == 'Archer':
                modifiers *= 1.05  
        
        elif general_id == 'julius':
            if unit_type == 'Legionary' and self.has_general:
                modifiers *= 1.25 
            elif unit_type == 'LightHorsemen':
                modifiers *= 1.05 
        
        elif general_id == 'leonidas' and unit_type == 'Hoplite':
            if self.has_general:
                modifiers *= 1.25 
        
        if hasattr(self, 'formations') and self.formation in self.formations:
            formation_mods = self.formations[self.formation]
            modifiers *= formation_mods['attack_modifier']
        
        return modifiers

    def _calculate_defense_modifiers(self, attacker, board):
        """
        Calculates the defense modifiers based on the unit's type, general, terrain, and formation.

        Args:
            attacker (BaseUnit): The unit performing the attack.
            board (GameBoard): The game board, which contains terrain and other state information.
        
        Returns:
            float: The final defense modifier after considering all factors.
        """
        
        modifiers = 1.0
        unit_type = self.__class__.__name__
        general_id = self.general_id if self.has_general else None
        
        if general_id == 'alexander' and unit_type == 'Hypaspist':
            modifiers *= 1.1  
        
        elif general_id == 'edward' and unit_type == 'Archer':
            if self.has_general:
                modifiers *= 1.05  
        
        elif general_id == 'charlemagne' and unit_type == 'HeavyCavalry':
            modifiers *= 1.05  
        
        elif general_id == 'harald' and unit_type == 'Viking':
            modifiers *= 1.12 
        
        elif general_id == 'julius' and unit_type == 'Legionary':
            modifiers *= 1.10 
        
        elif general_id == 'leonidas' and unit_type == 'Hoplite':
            modifiers *= 1.20  
        
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
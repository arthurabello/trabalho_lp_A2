"""
Manages the overall game state.
"""

from ...units.constants.armies import Armies
from ...units.types.cavalry.melee.cavalry_melee_units import LightHorsemen, HeavyCavalry
from ...units.types.infantry.ranged.infantry_ranged_units import Archer, Crossbowmen
from ...units.types.infantry.melee.infantry_melee_units import Hoplite, Hypaspist, Legionary, MenAtArms, Viking

class GameStateManager:
    def __init__(self, player1_general, player2_general):
        """Initialize game state."""
        self.m = 20  
        self.n = 30 
        if self.m <= 0 or self.n <= 0:
            raise ValueError("Invalid board dimensions in state_manager/init")
        
        self.state = "game"
        self.running = True
        self.selected_square = None
        self.selected_unit = None
        self.current_player = 1
        self.game_over = False
        self.winner = None

        self.player1_general = player1_general
        self.player2_general = player2_general
        
        self.player1_formation = None
        self.player2_formation = None
        self.setup_formations()
        self.board = None
        
    def setup_formations(self):
        """Setup player formations based on generals."""
        if not self.player1_general or not self.player2_general:
            raise ValueError("Both players must select a general")
        
        general1 = self.player1_general.upper()
        general2 = self.player2_general.upper()
        
        if not hasattr(Armies, general1) or not hasattr(Armies, general2):
            raise ValueError("Invalid general selection")
            
        self.player1_formation = getattr(Armies, general1)
        self.player2_formation = getattr(Armies, general2)

    def setup_units(self):
        """Initialize units for both players."""
        self.units1 = self._create_units(1, self.player1_formation)
        self.units2 = self._create_units(2, self.player2_formation)
        
        if self.units1: 
            self.units1[0].has_general = True
            self.units1[0].general_id = self.player1_general
        if self.units2: 
            self.units2[0].has_general = True
            self.units2[0].general_id = self.player2_general
        
        self.movement_points = {}
        self._reset_movement_points()

    def _create_units(self, player, board_layout):
        """Creates units based on layout."""
        unit_mapping = {
            'H': Hoplite,
            'C': LightHorsemen,
            'P': HeavyCavalry,
            'V': Viking,
            'A': Archer,
            'B': Crossbowmen,
            'I': Hypaspist,
            'L': Legionary,
            'M': MenAtArms,
            '#': None
        }

        units = []
        
        if player == 2:   
            board_layout = [row[::-1] for row in board_layout]
        
        for row_idx, row in enumerate(board_layout):
            for col_idx, char in enumerate(row):
                if char in unit_mapping and char != '#':
                    unit_class = unit_mapping[char]
                    if player == 2:
                        position = (self.m - 1 - row_idx, col_idx)
                    else:
                        position = (row_idx, col_idx)
                    unit = unit_class(position, player)
                    unit.terrain = self.board.terrain.get(position)
                    units.append(unit)
        
        if units:
            units[0].has_general = True
            
        return units

    def _reset_movement_points(self):
        """Reset movement points for current player."""
        all_units = self._get_player_units(self.current_player)
        for unit in all_units:
            self.movement_points[unit] = unit.movement_range

    def _get_player_units(self, player):
        """Get all units for a player."""
        return self.units1 if player == 1 else self.units2

    def get_all_units(self):
        """Get all units in game."""
        return self.units1 + self.units2

    def get_unit_at_position(self, position):
        """Get unit at specified position."""
        for unit in self.get_all_units():
            if unit.is_alive and unit.position == position:
                return unit
        return None

    def can_general_move(self, from_unit, to_unit):
        """Check if general can move between units."""
        if not from_unit.has_general or not to_unit.is_alive:
            return False
            
        if to_unit.player != self.current_player:
            return False
            
        row1, col1 = from_unit.position
        row2, col2 = to_unit.position
        return abs(row1 - row2) <= 1 and abs(col1 - col2) <= 1
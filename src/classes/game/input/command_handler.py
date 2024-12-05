"""
Handles game commands and actions.
"""

import pygame
from ...units.base.unit_direction import Direction
from ...units.types.cavalry.melee.cavalry_melee_units import LightHorsemen, HeavyCavalry
from ...units.types.infantry.ranged.infantry_ranged_units import Archer, Crossbowmen
from ...units.types.infantry.melee.infantry_melee_units import Hoplite, Hypaspist, Legionary, MenAtArms, Viking
from ...board import Board
from typing import List, Tuple

class CommandHandler:
    def __init__(self, game_manager) -> None:
        
        """
        Initialize the command handler.
        """

        self.game_manager = game_manager
        self.state_manager = game_manager.state_manager

    def _handle_general_movement(self, clicked_unit) -> bool:
        
        """
        Handle general movement.

        Args:
            clicked_unit: The unit that was clicked on.

        Returns:
            True if the general moved, False otherwise.
        """

        if not self.state_manager.selected_unit:
            return False
                
        if self.state_manager.can_general_move(self.state_manager.selected_unit, clicked_unit):
            if clicked_unit == self.state_manager.selected_unit:
                return False
                
            clicked_unit.has_general = True
            clicked_unit.general_id = self.state_manager.selected_unit.general_id
            self.state_manager.selected_unit.has_general = False
            self.state_manager.selected_unit.general_id = None
            
            self.state_manager.selected_unit = clicked_unit
            self.game_manager.board.select_square(
                clicked_unit.position,
                self.state_manager.movement_points[clicked_unit]
            )
            return True
                
        return False

    def handle_key_command(self, key) -> None:
        
        """
        Handle key commands.

        Args:
            key: The key that was pressed.
        """

        if key == pygame.K_SPACE:
            self._end_turn()
        elif key == pygame.K_g:
            self._toggle_formation()
        elif self.state_manager.selected_unit and not self.state_manager.selected_unit.has_changed_direction:
            self._handle_direction_change(key)

    def _handle_direction_change(self, key) -> None:
        
        """
        Handle direction change.

        Args:
            key: The key that was pressed.
        """

        direction_map = {
            pygame.K_UP: Direction.NORTH,
            pygame.K_RIGHT: Direction.EAST,
            pygame.K_DOWN: Direction.SOUTH,
            pygame.K_LEFT: Direction.WEST
        }
        
        if key in direction_map:
            self.state_manager.selected_unit.change_direction(direction_map[key])

    def handle_left_click(self, clicked_square) -> None:
        
        """
        Handle left mouse click.

        Args:
            clicked_square: The square that was clicked on.
        """

        clicked_unit = self.state_manager.get_unit_at_position(clicked_square)
        
        if clicked_unit and clicked_unit.player == self.state_manager.current_player:
            self._handle_unit_selection(clicked_unit, clicked_square)
        else:
            self._handle_unit_movement(clicked_square)

    def handle_right_click(self) -> None:
        
        """
        Handle right mouse click.
        """

        self.state_manager.selected_unit = None
        self.game_manager.board.select_square(None, 0)
        self.game_manager.renderer.draw_board()

    def _handle_unit_selection(self, clicked_unit, clicked_square) -> None:
        
        """
        Handle unit selection.

        Args:
            clicked_unit: The unit that was clicked on.
            clicked_square: The square that was clicked on.
        """

        if not self._handle_general_movement(clicked_unit):
            self.state_manager.selected_unit = clicked_unit
            self.game_manager.board.selected_square = clicked_square
            
            all_units = self.state_manager.get_all_units()
            
            self.game_manager.board.select_square(
                clicked_square, 
                self.state_manager.movement_points[clicked_unit],
                all_units                
            )

            valid_squares = [clicked_square]
            for pos in self.game_manager.board.reachable_positions:
                if pos == clicked_square:
                    continue
                    
                path_blocked = False
                for check_pos in self._get_positions_between(clicked_square, pos):
                    if any(u.is_alive and u.position == check_pos for u in all_units):
                        path_blocked = True
                        break
                        
                if not path_blocked and not any(u.is_alive and u.position == pos for u in all_units):
                    valid_squares.append(pos)

            self.game_manager.board.reachable_positions = valid_squares

            self.game_manager.board.update_attack_overlays(
                clicked_unit, 
                all_units
            )
        self.game_manager.renderer.draw_board()

    def _handle_ranged_unit_action(self, clicked_square, target_unit) -> None:
        
        """
        Handle ranged unit actions.

        Args:
            clicked_square: The square that was clicked on.
            target_unit: The target unit.
        """

        unit = self.state_manager.selected_unit
        if unit.can_attack(clicked_square) and \
           target_unit and target_unit.player != self.state_manager.current_player and \
           not unit.has_attacked:
            self.game_manager.combat_manager.handle_combat(unit, target_unit)
            self.state_manager.movement_points[unit] = 0
            self._update_unit_selection(unit.position)

    def _handle_melee_unit_action(self, clicked_square, target_unit) -> None:
        
        """
        Handle melee unit actions.

        Args:
            clicked_square: The square that was clicked on.
            target_unit: The target unit.
        """

        unit = self.state_manager.selected_unit

        if target_unit and target_unit.player != self.state_manager.current_player:
            if unit.can_attack(clicked_square) and not unit.has_attacked:
                self.game_manager.combat_manager.handle_combat(unit, target_unit)
                self.state_manager.movement_points[unit] = 0
                self._update_unit_selection(unit.position)
                return
            
            elif clicked_square in self.game_manager.board.reachable_positions:
                movement_cost = self.game_manager.board.movement_costs[clicked_square]
                
                if self.state_manager.movement_points[unit] >= movement_cost:
                    unit.move(clicked_square)
                    unit.terrain = self.game_manager.board.terrain.get(clicked_square)
                    self.state_manager.movement_points[unit] -= movement_cost
                    if unit.can_attack(target_unit.position) and not unit.has_attacked:
                        self.game_manager.combat_manager.handle_combat(unit, target_unit)
                        self.state_manager.movement_points[unit] = 0
                    self._update_unit_selection(clicked_square)
                    return

    def _execute_movement(self, target_square, movement_cost) -> None:
        
        """
        Executes unit movement.

        Args:
            target_square: The target square.
            movement_cost: The movement cost.
        """

        unit = self.state_manager.selected_unit
        target_unit = self.state_manager.get_unit_at_position(target_square)

        if isinstance(unit, Archer) and target_unit and target_unit.player != self.state_manager.current_player:
            self.game_manager.combat_manager.handle_combat(unit, target_unit)
            self.state_manager.movement_points[unit] = 0
            return
        
        if target_unit and target_unit.player != self.state_manager.current_player:
            self.game_manager.combat_manager.handle_combat(unit, target_unit)
            if unit.is_alive:
                unit.move(target_square)
                unit.terrain = self.game_manager.board.terrain.get(target_square)
                self.state_manager.movement_points[unit] = 0
        elif not target_unit:
            unit.move(target_square)
            unit.terrain = self.game_manager.board.terrain.get(target_square)
            self.state_manager.movement_points[unit] -= movement_cost
        
        self._update_unit_selection(target_square)

    def _handle_unit_movement(self, clicked_square) -> None:
        
        """
        Handle the movement of a unit.

        Args:
            clicked_square: The square that was clicked on.
        """

        if not self.state_manager.selected_unit:
            return

        unit = self.state_manager.selected_unit
        target_unit = self.state_manager.get_unit_at_position(clicked_square)
        all_units = self.state_manager.get_all_units()

        if target_unit and target_unit.player != self.state_manager.current_player:
            if unit.can_attack(clicked_square) and not unit.has_attacked:
                self.game_manager.combat_manager.handle_combat(unit, target_unit)
                self.state_manager.movement_points[unit] = 0
                self._update_unit_selection(unit.position, all_units)
                return
        
        if clicked_square in self.game_manager.board.reachable_positions:
            unit_row, unit_col = unit.position
            target_row, target_col = clicked_square
            
            path_blocked = False
            for pos in self._get_positions_between(unit.position, clicked_square):
                if any(u.is_alive and u.position == pos for u in all_units):
                    path_blocked = True
                    break

            if not path_blocked and not target_unit:
                movement_cost = self.game_manager.board.movement_costs[clicked_square]
                if self.state_manager.movement_points[unit] >= movement_cost:
                    unit.move(clicked_square)
                    unit.terrain = self.game_manager.board.terrain.get(clicked_square)
                    self.state_manager.movement_points[unit] -= movement_cost
                    self._update_unit_selection(clicked_square, all_units)

    def _get_positions_between(self, start_pos, end_pos) -> List[Tuple[int, int]]:
        
        """
        Get the positions between two positions.

        Args:
            start_pos: The start position.
            end_pos: The end position.

        Returns:
            A list of positions between the start and end positions.
        """
        
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        if start_row == end_row: 
            start, end = min(start_col, end_col), max(start_col, end_col)
            return [(start_row, col) for col in range(start + 1, end)]
        else:
            start, end = min(start_row, end_row), max(start_row, end_row)
            return [(row, start_col) for row in range(start + 1, end)]


    def _update_unit_selection(self, position, all_units) -> None:
        
        """
        Update the unit selection.

        Args:
            position: The position to select.
            all_units: All units in the game.
        """

        unit = self.state_manager.selected_unit
        
        if not unit.is_alive:
            self.game_manager.board.select_square(None, 0, all_units)
            self.state_manager.selected_unit = None
        elif self.state_manager.movement_points[unit] <= 0:
            self.game_manager.board.select_square(None, 0, all_units)
            self.state_manager.selected_unit = None
        else:
            self.game_manager.board.select_square(
                position, 
                self.state_manager.movement_points[unit],
                all_units
            )
            self.game_manager.board.update_attack_overlays(unit, all_units)

        self.game_manager.renderer.draw_board()

    def _end_turn(self) -> None:
        
        """
        Ends the current player's turn.
        """

        self.state_manager.current_player = 3 - self.state_manager.current_player
        self.state_manager.selected_unit = None
        self.game_manager.board.select_square(None, 0)
        self.game_manager.board.update_attack_overlays(None, self.state_manager.get_all_units())
        self.state_manager._reset_movement_points()

        for unit in self.state_manager._get_player_units(self.state_manager.current_player):
            unit.has_attacked = False
            unit.reset_direction_change()

        self.game_manager.renderer.draw_board()

    def _toggle_formation(self) -> None:
        
        """
        Toggles the formation of the selected unit.
        """

        if self.state_manager.selected_unit:
            if self.state_manager.movement_points[self.state_manager.selected_unit] > 0:
                formations = list(self.state_manager.selected_unit.formations.keys())
                current_index = formations.index(self.state_manager.selected_unit.formation)
                next_index = (current_index + 1) % len(formations)
                next_formation = formations[next_index]
                self.state_manager.selected_unit.change_formation(next_formation)
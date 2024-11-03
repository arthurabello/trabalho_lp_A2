"""
This module represents the Warrior unit, which is a combat unit with extended movement range.
"""

import pygame
import os

class Warrior:

    """
    Represents a Warrior piece on the game board.
    
    Attributes:
        position (tuple): Current position of the warrior (row, col)
        player (int): Player number (1 or 2) who owns this warrior
        color (tuple): RGB color tuple for the warrior
        movement_range (int): Number of squares the warrior can move
        size (tuple): Size of the warrior piece (width, height)
        is_alive (bool): If the warrior is alive
    """
    
    PLAYER1_COLOR = (200, 0, 0)    
    PLAYER2_COLOR = (0, 0, 200)    
    BORDER_COLOR = (255, 255, 255) 
    TEXT_COLOR = (0, 0, 0)
    
    def __init__(self, initial_position, player):

        """
        Initialize a new Warrior piece.
        
        Args:
            initial_position (tuple): Starting position (row, col)
            player (int): Player number (1 or 2)
        """

        self.position = initial_position
        if not isinstance(initial_position, tuple) or len(initial_position) != 2:
            raise ValueError("Invalid initial position format in warrior/init")
        
        self.player = player
        if player not in [1, 2]:
            raise ValueError("Player must be 1 or 2 in warrior/init")
        
        self.color = self.PLAYER1_COLOR if player == 1 else self.PLAYER2_COLOR
        self.movement_range = 3  #this is changeable
        self.size = (0, 0) 
        
        if not pygame.font.get_init():
            try:
                pygame.font.init()

            except Exception as e:
                raise RuntimeError(f"Failed to initialize font system in warrior/init: {str(e)}")
            
        try:
            self.font = pygame.font.Font(None, 36)

        except Exception as e:
            raise RuntimeError(f"Failed to create font in warrior/init: {str(e)}")
           
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init()

            except Exception as e:
                raise RuntimeError(f"Failed to initialize audio system in warrior/init: {str(e)}")
            
        try:
            move_sound_path = os.path.join('..', 'assets', 'sounds', 'movement.wav')
            if not os.path.exists(move_sound_path):
                raise FileNotFoundError(f"Warrior Movement file not found in warrior/init: {move_sound_path}")
            
            self.move_sound = pygame.mixer.Sound(move_sound_path)
            self.move_sound.set_volume(0.7)
            
            attack_sound_path = os.path.join('..', 'assets', 'sounds', 'attack.wav')
            if not os.path.exists(attack_sound_path):
                raise FileNotFoundError(f"Warrior Attack file not found in warrior/init: {attack_sound_path}")
            
            self.attack_sound = pygame.mixer.Sound(attack_sound_path)
            self.attack_sound.set_volume(0.8)
            
        except Exception as e:
            raise RuntimeError(f"Failed to load warrior sounds in warrior/init: {str(e)}")
        
        self.is_alive = True

    def move(self, new_position):

        """
        Move the warrior to a new position.
        
        Args:
            new_position (tuple): New position (row, col)
        """

        if not self.is_alive:
            return   #dead men tell no tales
        
        self.position = new_position

        try:
            self.move_sound.play()

        except Exception as e:
            print(f"Failed to play warrior movement sound in warrior/move: {str(e)}")

    def attack(self, target):

        """
        Attack another unit.
        
        Args:
            target: The unit being attacked
        """

        if not self.is_alive or not target.is_alive or target.player == self.player:
            return  #unfortunately, no friendly fire (for now)
            
        try:
            self.attack_sound.play()

        except Exception as e:
            print(f"Failed to play warrior attack sound in warrior/attack: {str(e)}")
            
        target.is_alive = False

    def can_attack(self, target_position):

        """
        Check if this unit can attack a position.
        
        Args:
            target_position (tuple): Position to check
            
        Returns:
            bool: True if the position is within attack range
        """

        if not self.is_alive:
            return False    #dead men tell no tales
            
        row, col = self.position
        target_row, target_col = target_position
        
        return abs(row - target_row) <= self.movement_range and abs(col - target_col) <= self.movement_range
        
    def draw(self, screen, board):

        """
        Draw the warrior on the screen with a 'W' letter inside.
        
        Args:
            screen (pygame.Surface): Game screen to draw on
            board (Board): Game board instance for size calculations
        """

        if not self.is_alive:
            return #dead men tell no tales
        
        if not screen:
            raise ValueError("Invalid screen surface in warrior/draw")
            
        if not board:
            raise ValueError("Invalid board object in warrior/draw")
        
        try:
            width, height = screen.get_size()
            if width <= 0 or height <= 0:
                raise ValueError("Invalid screen dimensions")
            
        except Exception as e:
            raise RuntimeError(f"Failed to get screen dimensions: {str(e)}")
        
        try:
            square_width = width // board.n
            square_height = height // board.m
            self.size = (square_width, square_height)
        
            x = self.position[1] * square_width
            y = self.position[0] * square_height
        
            margin = square_width * 0.1
            warrior_width = square_width * 0.8
            warrior_height = square_height * 0.8
        
            x_centered = x + margin
            y_centered = y + margin
        
            pygame.draw.rect(screen, self.color, (x_centered, y_centered, warrior_width, warrior_height))
            pygame.draw.rect(screen, self.BORDER_COLOR, (x_centered, y_centered, warrior_width, warrior_height), 2)
        
            text_surface = self.font.render('W', True, self.TEXT_COLOR)
        
            text_width, text_height = text_surface.get_size()
        
            text_x = x_centered + (warrior_width - text_width) // 2
            text_y = y_centered + (warrior_height - text_height) // 2
        
            screen.blit(text_surface, (text_x, text_y))

        except Exception as e:
            raise RuntimeError(f"Failed to draw warrior: {str(e)}")
                        
    def can_move_to(self, position, board, all_units):

        """
        Check if the warrior can move to a given position.
        
        Args:
            position (tuple): Target position to check (row, col)
            board (Board): Game board instance
            all_units (list): List of all units on the board
            
        Returns:
            bool: True if the move is valid, False otherwise
        """

        if not self.is_alive:
            return False  #dead men tell no tales

        reachable = board.graph.get_reachable_positions(self.position, self.movement_range)
        if position not in reachable:
            return False

        for unit in all_units:
            if unit != self and unit.is_alive and unit.position == position:
                return False

        return True
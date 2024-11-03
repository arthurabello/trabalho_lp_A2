"""
This module represents the King piece, which is the main unit that players need to protect.
"""

import pygame
import os

class King:

    """
    Represents a King piece on the game board.
    
    Attributes:
        position (tuple): Current position of the king (row, col)
        player (int): Player number (1 or 2) who owns this king
        color (tuple): RGB color tuple for the king
        movement_range (int): Number of squares the king can move
        size (tuple): Size of the king piece (width, height)
        is_alive (bool) : if the king is alive
    """
    
    PLAYER1_COLOR = (255, 0, 0)   
    PLAYER2_COLOR = (0, 0, 255)    
    BORDER_COLOR = (255, 255, 255)  
    TEXT_COLOR = (0, 0, 0)
    
    def __init__(self, initial_position, player):

        """
        Initialize a new King piece.
        
        Args:
            initial_position (tuple): Starting position (row, col)
            player (int): Player number (1 or 2)
        """

        self.position = initial_position
        if not isinstance(initial_position, tuple) or len(initial_position) != 2:
            raise ValueError("Invalid initial position format in king/init")
        
        self.player = player
        if player not in [1, 2]:
            raise ValueError("Player must be 1 or 2 in king/init")
        
        self.color = self.PLAYER1_COLOR if player == 1 else self.PLAYER2_COLOR
        self.movement_range = 1  #not recommended, but this can be changed
        self.size = (0, 0)  #will be set when drawing based on screen size
        
        if not pygame.font.get_init():
            try:
                pygame.font.init()

            except Exception as e:
                raise RuntimeError(f"Failed to initialize font system in king/init: {str(e)}")
            
        try:
            self.font = pygame.font.Font(None, 36)

        except Exception as e:
            raise RuntimeError(f"Failed to create font in king/init: {str(e)}")
           
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init()

            except Exception as e:
                raise RuntimeError(f"Failed to initialize audio system in king/init: {str(e)}")
            
        try:
            move_sound_path = os.path.join('..', 'assets', 'sounds', 'movement.wav')
            if not os.path.exists(move_sound_path):
                raise FileNotFoundError(f"King Movement file not found in king/init: {move_sound_path}")
            
            self.move_sound = pygame.mixer.Sound(move_sound_path)
            self.move_sound.set_volume(0.7) #optionally adjust between 0 and 1
            
            attack_sound_path = os.path.join('..', 'assets', 'sounds', 'attack.wav')
            if not os.path.exists(attack_sound_path):
                raise FileNotFoundError(f"King Attack file not found in king/init: {attack_sound_path}")
            
            self.king_attack_sound = pygame.mixer.Sound(attack_sound_path)
            self.king_attack_sound.set_volume(0.8)
            
        except Exception as e:
            raise RuntimeError(f"Failed to load king sounds in king/init: {str(e)}")
        
        self.is_alive = True #clearly it has to be alive

    def move(self, new_position):

        """
        Move the king to a new position.
        
        Args:
            new_position (tuple): New position (row, col)
        """

        if not self.is_alive:
            return   #dead men tell no tales
        
        self.position = new_position

        try:
            self.move_sound.play()
        except Exception as e:
            print(f"Failed to play king movement sound in king/move: {str(e)}")

    def attack(self, target):

        """
        Attack another unit.
        
        Args:
            target_king (King): The king being attacked
        """

        if not self.is_alive or not target.is_alive:
            return   #dead men tell no tales
            
        try:
            self.king_attack_sound.play()
        except Exception as e:
            print(f"Failed to play king attack sound in king/attack: {str(e)}")
            
        target.is_alive = False #binary attack, eventually will not be binary

    def can_attack(self, target_position):

        """
        Check if this unit can attack a position.
        
        Args:
            target_position (tuple): Position to check
            
        Returns:
            bool: True if the position is within attack range
        """

        if not self.is_alive:
            return False  #dead men tell no tales
            
        row, col = self.position
        target_row, target_col = target_position
        
        return abs(row - target_row) <= self.movement_range and abs(col - target_col) <= self.movement_range
        
    def draw(self, screen, board):

        """
        Draw the king on the screen with a 'K' letter inside.
        
        Args:
            screen (pygame.Surface): Game screen to draw on
            board (Board): Game board instance for size calculations
        """

        if not self.is_alive:
            return   #dead men tell no tales
        
        if not screen:
            raise ValueError("Invalid screen surface in king/draw")
            
        if not board:
            raise ValueError("Invalid board object in king/draw")
        
        try:
            width, height = screen.get_size() #calculates square sizes bazed on dimension
            if width <= 0 or height <= 0:
                raise ValueError("Invalid screen dimensions")
            
        except Exception as e:
            raise RuntimeError(f"Failed to get screen dimensions: {str(e)}")
        

        try:
            square_width = width // board.n
            square_height = height // board.m
            square_width = width // board.n
            square_height = height // board.m
            self.size = (square_width, square_height)
        
            x = self.position[1] * square_width #calculate pixel position
            y = self.position[0] * square_height
        
            margin = square_width * 0.1
            king_width = square_width * 0.8 #creates a smaller square for the king
            king_height = square_height * 0.8
        
            x_centered = x + margin #center the king in the square
            y_centered = y + margin
        
            pygame.draw.rect(screen, self.color, (x_centered, y_centered, king_width, king_height))  #draw the king as a colored square with a white baorder
            pygame.draw.rect(screen, self.BORDER_COLOR,(x_centered, y_centered, king_width, king_height),2)
        
            text_surface = self.font.render('K', True, self.TEXT_COLOR) #render the "K" marker
        
            text_width, text_height = text_surface.get_size() #get the size of the rendered text
        
            text_x = x_centered + (king_width - text_width) // 2  #calculate position to center the text in the king square
            text_y = y_centered + (king_height - text_height) // 2
        
            screen.blit(text_surface, (text_x, text_y)) #draw the text

        except Exception as e:
            raise RuntimeError(f"Failed to draw king in game/draw (agora de fato fudeu): {str(e)}")
                        
    def can_move_to(self, position, board):

        """
        Check if the king can move to a given position.
        
        Args:
            position (tuple): Target position to check (row, col)
            board (Board): Game board instance
            
        Returns:
            bool: True if the move is valid, False otherwise
        """
        
        if not self.is_alive:
            return False   #dead men tell no tales
        
        reachable = board.graph.get_reachable_positions(self.position, self.movement_range)
        return position in reachable
"""
This module represents the game board, responsible for managing selectable squares, colors, and the highlighting system.
"""

import pygame
from .graph import BoardGraph

class Board:
    
    """
    Manages the board layout, including the selection of squares, highlighting reachable positions, 
    and drawing the board on the screen.

    Attributes:
        m (int): Number of rows on the board.
        n (int): Number of columns on the board.
        initial_width (int): Initial width of the game window.
        initial_height (int): Initial height of the game window.
        selected_square (tuple or None): The currently selected square on the board, or None if no square is selected.
        graph (BoardGraph): Instance of the BoardGraph class to manage board connectivity.
        reachable_positions (set): Set of squares that are reachable from the selected square.

    Methods:
        get_square_from_click(mouse_pos, screen): Determines which square was clicked based on mouse position.
        select_square(square, movement_points): Selects a square and calculates reachable positions based on movement points.
        draw(screen, selected_square): Draws the board, with highlights for reachable and selected squares.
    """

    COLOR_LIGHT_GREEN = (144, 238, 144)
    COLOR_DARK_GREEN = (0, 100, 0)
    COLOR_RED = (255, 0, 0)
    COLOR_GRAY = (139, 137, 137)
    COLOR_HIGHLIGHT = (255, 255, 0, 180)

    def __init__(self, m, n, initial_width, initial_height) -> None:

        """
        Initializes the board with dimensions and sets up the board graph for connectivity management.

        Args:
            m (int): Number of rows on the board
            n (int): Number of columns on the board
            initial_width (int): Initial width of the game window
            initial_height (int): Initial height of the game window
        """
        
        self.m = m
        self.n = n
        if m <= 0 or n <= 0:
            raise ValueError("Board dimensions must be positive integers in board/init")
        if initial_width <= 0 or initial_height <= 0:
            raise ValueError("Initial window dimensions must be positive in board/init")
        
        self.initial_width = initial_width
        self.initial_height = initial_height
        self.selected_square = None
        self.terrain = self.initialize_terrain()
        self.graph = BoardGraph(m, n, self.terrain)
        self.reachable_positions = set()

        self.sprites = {
            "plains": pygame.image.load("../assets/sprites/terrains/plains.png"),
            "mountain": pygame.image.load("../assets/sprites/terrains/mountain.png"),
            "forest": pygame.image.load("../assets/sprites/terrains/forest.png")
        }

    def get_square_from_click(self, mouse_pos, screen) -> None:

        """
        Determines the board square corresponding to a mouse click based on screen dimensions.

        Args:
            mouse_pos (tuple): The (x, y) position of the mouse click
            screen (pygame.Surface): The game screen surface

        Returns:
            tuple: The (row, column) of the clicked square
        """

        x, y = mouse_pos
        if not isinstance(mouse_pos, tuple) or len(mouse_pos) != 2:
            raise ValueError("Invalid mouse position format in board/get_square_from_click")
        
        width, height = screen.get_size()
        if x < 0 or x >= width or y < 0 or y >= height:
            return None  # clicked outside the board
        
        square_width = self.initial_width // self.n
        square_height = self.initial_height // self.m

        scale_x = width / self.initial_width
        scale_y = height / self.initial_height

        scaled_x = x / scale_x
        scaled_y = y / scale_y

        column = int(scaled_x // square_width)
        row = int(scaled_y // square_height)
        
        if row >= self.m or column >= self.n:
            return None 
        
        return row, column

    def select_square(self, square, movement_points) -> None:

        """
        Selects a square and calculates all reachable positions based on the movement points available.

        Args:
            square (tuple): The (row, column) position of the selected square
            movement_points (int): Number of movement points available for calculating reachable positions
        """

        if movement_points < 0:
            raise ValueError("Negative movement points in board/select_square")

        self.selected_square = square
        if square is not None:
            if not isinstance(square, tuple) or len(square) != 2:
                raise ValueError("Invalid square format")
            
            row, col = square
            if not (0 <= row < self.m and 0 <= col < self.n):
                raise ValueError("Square position out of bounds in board/select_square") #validating square position
            
        if square:
            self.reachable_positions, self.movement_costs = self.graph.get_reachable_positions(square, movement_points)
        else:
            self.reachable_positions = set()
            self.movement_costs = {}

    def initialize_terrain(self):
        """
        Initializes the terrain map. By default, it creates some mountains at specific positions.
        """
        terrain = {}
        for row in range(self.m):
            for col in range(self.n):
                terrain[(row,col)] = "plains"

                # mountains 
                if ((row + col) % 6 == 0 or (row - col) % 5 == 2) and row % 2 == 0:
                    terrain[(row, col)] = "mountain"
                
                if ((row + col) % 15 == 0):
                    terrain[(row, col)] = "forest"
        
        return terrain

    def draw(self, screen, selected_square=None):

        """
        Draws the board, with highlights for reachable and selected squares.
        
        Args:
            screen (pygame.Surface): Surface to draw the board on
            selected_square (tuple or None): Currently selected square coordinates
        """
        
        if not screen:
            raise ValueError("Invalid screen surface in board/draw")
                
        width, height = screen.get_size()
        if width <= 0 or height <= 0:
            raise ValueError("Invalid screen dimensions in board/draw")

        square_width = width // self.n
        square_height = height // self.m

        for row in range(self.m):
            for column in range(self.n):

                # First plains, then the rest
                plains_sprite = self.sprites["plains"]
                plains_sprite_scaled = pygame.transform.scale(plains_sprite, (square_width, square_height))
                screen.blit(plains_sprite_scaled, (column * square_width, row * square_height))

                if self.terrain[(row, column)] == "mountain":
                    mountain_sprite = self.sprites["mountain"]
                    mountain_sprite_scaled = pygame.transform.scale(mountain_sprite, (square_width, square_height))
                    screen.blit(mountain_sprite_scaled, (column * square_width, row * square_height))
                
                if self.terrain[(row, column)] == "forest":
                    forest_sprite = self.sprites["forest"]
                    forest_sprite_scaled = pygame.transform.scale(forest_sprite, (square_width, square_height))
                    screen.blit(forest_sprite_scaled, (column * square_width, row * square_height))


                if (row, column) in self.reachable_positions:
                    highlight_surface = pygame.Surface((square_width, square_height), pygame.SRCALPHA)
                    pygame.draw.rect(highlight_surface, self.COLOR_HIGHLIGHT, (0, 0, square_width, square_height))
                    screen.blit(highlight_surface, (column * square_width, row * square_height))

                if selected_square and (row, column) == selected_square:
                    pygame.draw.rect(screen, self.COLOR_RED, 
                                (column * square_width, row * square_height, square_width, square_height), 3)
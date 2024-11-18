"""
This module represents the game board, responsible for managing selectable squares, colors, and the highlighting system.
"""

import pygame
from .graph import BoardGraph
from .units.constants import Paths

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
    map1 = '''
            #######x#x#.##..###x##########
            #.x#xx#.##x##x#x.#x##x##x.#.#.
            ####..xx####.#######.####x##..
            ###.##x######.xx####x.###x.##.
            #.############.x############.#
            ###.#.x##.#.#####x##.####xxxx#
            .###x.#.#######.##.##x#######x
            ######xx#.#x.######x###.##.xx#
            ######.####..#####.#..##.##x.#
            x###x#x#####.###x#..#####.##x.
            x#####x###.#########.x#x.#####
            .x#########x#x#.########.##x.x
            x###x##.###.x##x##xx#####xx###
            ######x#x###.#####x#####x#x###
            #x#.####.##x##.##.##x####.##.#
            xx#x##x##x#x##x#.###x#.x####.#
            ###..##xx.###.##x###########..
            #xx#x.#.##.#####.###x########.
            #x#####.####x.#xx##x.##.#.####
            #.##.########.#####..#####x##x'''
    
    map2 = '''
            .#.x#..##..#x###.#x####x.#####
            .#############x#x##.######.##.
            ####.#####x#x#######.##..#...x
            ###.####x#####.xx##x##.#x##x##
            #x###xx#######x####x##x#######
            ##.#######.##########.####xxx#
            ##.#############.#########x##x
            x#x##.#.#####.########xxx#####
            #######xx#.###.x#.##x#.#####.#
            ####xx#.x####.x#.##.#####..###
            ##.#####..x###.x##x####.x###.x
            ######x###x######x#.##xx######
            ###x.###x#####x.#######.#.###.
            .#.##x###xx.#.xx.#..#####xx##.
            x#xx#.##.##.x#xx.####.xx##.x##
            #.############.x#############.
            ##xx##.######x#x##.x#####x##.#
            #.#x.#####...#..###.########x#
            #x##x#.###x####.#########.###.
            #xx#..###x.#x###x#x.###x###x##'''

    def __init__(self, m, n, initial_width, initial_height, units, map_choice=None) -> None:

        """
        Initializes the board with dimensions and sets up the board graph for connectivity management.

        Args:
            m (int): Number of rows on the board
            n (int): Number of columns on the board
            initial_width (int): Initial width of the game window
            initial_height (int): Initial height of the game window
        """
        if map_choice == 1:
            self.terrain_map = self.map1
        elif map_choice == 2:
            self.terrain_map = self.map2
        else:
            self.terrain_map = self.map1 # by default
            
        self.m = m
        self.n = n
        if m <= 0 or n <= 0:
            raise ValueError("Board dimensions must be positive integers in board/init")
        if initial_width <= 0 or initial_height <= 0:
            raise ValueError("Initial window dimensions must be positive in board/init")
        
        self.initial_width = initial_width
        self.initial_height = initial_height
        self.selected_square = None
        self.terrain = self.initialize_terrain(self.terrain_map)
        self.units = units
        self.graph = BoardGraph(m, n, self.terrain, units)
        self.reachable_positions = set()

        self.sprites = {
            "plains": pygame.image.load("../assets/sprites/terrains/plains.png"),
            "mountain": pygame.image.load("../assets/sprites/terrains/mountain.png"),
            "forest": pygame.image.load("../assets/sprites/terrains/forest.png"),
            "attackable": pygame.image.load(Paths.ATTACKABLE_SQUARE).convert_alpha(),
            "dangerous": pygame.image.load(Paths.DANGEROUS_SQUARE).convert_alpha()
        }
        self.dangerous_squares = set()
        self.attackable_squares = set()

    def _is_valid_position(self, row: int, col: int) -> bool:
        """
        Checks if a position is within the board boundaries.
        
        Args:
            row (int): Row index to check
            col (int): Column index to check
            
        Returns:
            bool: True if position is valid, False otherwise
        """
        return 0 <= row < self.m and 0 <= col < self.n
    
    def update_attack_overlays(self, selected_unit, all_units):

        """
        Updates the dangerous and attackable squares based on the selected unit
        and enemy positions. Only marks squares as dangerous if they are both:
        - Within the selected unit's movement range
        - Within an enemy unit's attack range
        """

        self.dangerous_squares.clear()
        self.attackable_squares.clear()
        
        if not selected_unit:
            return
                
        enemy_units = [unit for unit in all_units if unit.is_alive and unit.player != selected_unit.player]
        
        all_dangerous = set()
        for enemy in enemy_units:
            row, col = enemy.position
            attack_range = enemy.attack_range
            
            for i in range(-attack_range, attack_range + 1):
                for j in range(-attack_range, attack_range + 1):
                    new_row, new_col = row + i, col + j
                    if (self._is_valid_position(new_row, new_col) and 
                        abs(i) + abs(j) <= attack_range and
                        (new_row, new_col) != enemy.position): 
                        all_dangerous.add((new_row, new_col))
        
        self.dangerous_squares = all_dangerous.intersection(self.reachable_positions)
    
        for enemy in enemy_units:
            enemy_pos = enemy.position
            if selected_unit.can_attack(enemy_pos):
                self.attackable_squares.add(enemy_pos)


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
            self.reachable_positions, self.movement_costs = self.graph.get_reachable_positions(square, movement_points, self.units)
        else:
            self.reachable_positions = set()
            self.movement_costs = {}

    def initialize_terrain(self, terrain_map):

        """
        Initializes the terrain map from a provided map string.

        Args:
            terrain_map (str): A string representation of the terrain map where each line corresponds to a row 
            and each character represents a type of terrain. The expected characters are:
                - '#' for plains
                - '.' for mountains
                - 'x' for forests

        Returns:
            dict: A dictionary representing the terrain map, where:
                - Keys are tuples (row_index, col_index) indicating the row and column of each cell.
                - Values are strings representing the terrain type at each coordinate ("plains", "mountains" and "forests").
        """

        terrain = {}
        rows = [row.strip() for row in terrain_map.strip().split("\n")]

        for row_index, row in enumerate(rows):
            for col_index, cell in enumerate(row):
                if cell == "#":
                    terrain[(row_index, col_index)] = "plains"
                elif cell == ".":
                    terrain[(row_index, col_index)] = "mountain"
                elif cell == "x":
                    terrain[(row_index, col_index)] = "forest"
                else:
                    raise ValueError(f"Unexpected terrain character: {cell}")
        
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
        
        width, height = screen.get_size()
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
                    
                square_pos = (row, column)

                if square_pos in self.dangerous_squares:
                    dangerous_sprite = pygame.transform.scale(
                        self.sprites["dangerous"],
                        (square_width, square_height)
                    )
                    dangerous_sprite.set_alpha(128)  # 50% transparency
                    screen.blit(dangerous_sprite, 
                              (column * square_width, row * square_height))
                
                if square_pos in self.attackable_squares:
                    attackable_sprite = pygame.transform.scale(
                        self.sprites["attackable"],
                        (square_width, square_height)
                    )
                    attackable_sprite.set_alpha(128)  # 50% transparency
                    screen.blit(attackable_sprite, 
                              (column * square_width, row * square_height))
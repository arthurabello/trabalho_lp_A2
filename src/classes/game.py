"""
This module represents the main game structure, responsible for initializing, handling events, updating, and rendering the game.
"""

import pygame
from .board import Board

class Game:

    """
    Manages the main game loop and user interactions, such as resizing the window and handling fullscreen mode.

    Attributes:
        m (int): Number of rows on the board.
        n (int): Number of columns on the board.
        initial_width (int): Initial width of the game window.
        initial_height (int): Initial height of the game window.
        screen (pygame.Surface): The main display surface for rendering the game.
        board (Board): Instance of the Board class to manage board behavior.
        running (bool): Flag to control the game loop.
        fullscreen (bool): Flag to toggle fullscreen mode.
        current_size (list): Current width and height of the window.
        resizing (bool): Flag to handle window resizing events.

    Methods:
        handle_events(): Handles user interactions, such as mouse clicks, window resizing, and key presses.
        toggle_fullscreen(): Toggles the game display between fullscreen and resizable window modes.
        update(): Updates the screen state, handling window resizing.
        render(): Draws the game components on the screen and updates the display.
        run(): Runs the main game loop, processing events, updating game state, and rendering the display.
    """

    def __init__(self) -> None:

        """
        Initializes the game settings
        """

        pygame.init()
        self.m = 10
        self.n = 21
        self.initial_width = self.n * 40
        self.initial_height = self.m * 40
        self.screen = pygame.display.set_mode((self.initial_width, self.initial_height), 
                                            pygame.RESIZABLE)
        pygame.display.set_caption("The Art of Violence")
        self.board = Board(self.m, self.n, self.initial_width, self.initial_height)
        self.running = True
        self.fullscreen = False
        self.current_size = [self.initial_width, self.initial_height]
        self.resizing = False
        
    def handle_events(self) -> None:

        """
        Manages user interactions, such as closing the game, clicking on the board, resizing the window, and toggling fullscreen.
        
        Checks for pygame events and updates game state based on user actions, such as mouse clicks for selecting squares,
        resizing the window, and pressing keys to toggle fullscreen mode.
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_position = pygame.mouse.get_pos()
                    square = self.board.get_square_from_click(mouse_position, self.screen)
                    self.board.select_square(square, movement_points=5)  #change movement points depending on the unit
                    print(f"Selected square: row {square[0]}, column {square[1]}")

            elif event.type == pygame.VIDEORESIZE:
                self.resizing = True
                self.current_size = [event.w, event.h]
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.toggle_fullscreen()
    
    def toggle_fullscreen(self) -> None:

        """
        Toggles the display mode between fullscreen and resizable windowed mode.
        
        Adjusts the screen mode based on the current fullscreen flag. If the game is in windowed mode, it switches to fullscreen,
        and vice versa. It also updates the current window size after changing the display mode.
        """

        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.current_size = self.screen.get_size()
        else:
            self.screen = pygame.display.set_mode(self.current_size, pygame.RESIZABLE)
    
    def update(self) -> None:

        """
        Updates the game state, especially during window resizing.
        
        If the window is being resized, updates the display surface to reflect the new size. Resets the resizing flag once done.
        """

        if self.resizing:
            self.screen = pygame.display.set_mode(self.current_size, pygame.RESIZABLE)
            self.resizing = False
    
    def render(self) -> None:

        """
        Renders the game components on the screen.
        
        Clears the screen, draws the board, including any selected or highlighted squares, and updates the display.
        """

        self.screen.fill((0, 0, 0))
        self.board.draw(self.screen, self.board.selected_square)
        pygame.display.flip()
    
    def run(self) -> None:

        """
        Executes the main game loop, which continuously processes events, updates the game state, and renders the screen.
        
        The loop runs as long as the `running` flag is True. It handles user inputs, updates the game components,
        and refreshes the screen, providing a smooth gameplay experience. When the loop ends, it closes the game.
        """

        while self.running:
            self.handle_events()
            self.update()
            self.render()
        pygame.quit()
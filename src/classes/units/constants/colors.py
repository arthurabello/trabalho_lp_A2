class Colors:

    """
    Colors used for rendering units and board elements.
    """

    PLAYER1_PRIMARY = (255, 0, 0)            # bright red for player 1 main units
    PLAYER2_PRIMARY = (0, 0, 255)            # bright blue for player 2 main units
    PLAYER1_PRIMARY_HOVER = (255, 0, 0, 40)  # red with opacity       
    PLAYER2_PRIMARY_HOVER = (0, 0, 255, 40)  # blue with opacity
            
    PLAYER1_SECONDARY = (200, 0, 0)      # darker red for player 1 secondary units
    PLAYER2_SECONDARY = (0, 0, 200)      # darker blue for player 2 secondary units
    BORDER = (255, 255, 255)             # white borders
    TEXT = (0, 0, 0)                     # black text
    COLOR_HIGHLIGHT = (255, 255, 0, 180) # for reachable positions
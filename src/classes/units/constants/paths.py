import os

class Paths:

    """
    Paths to assets used for rendering units.
    """
    
    ASSETS_DIR = os.path.join('..', 'assets')
    SPRITES_DIR = os.path.join(ASSETS_DIR, 'sprites')
    
    # Terrain sprites
    TERRAIN_DIR = os.path.join(SPRITES_DIR, 'terrains')
    PLAIN_SPRITE = os.path.join(TERRAIN_DIR, 'plains.png')
    FOREST_SPRITE = os.path.join(TERRAIN_DIR, 'forest.png')
    MOUNTAIN_SPRITE = os.path.join(TERRAIN_DIR, 'mountain.png')

    # Sound effects
    SOUNDS_DIR = os.path.join(ASSETS_DIR, 'sounds')
    MOVE_SOUND_DIR = os.path.join(SOUNDS_DIR, 'movement')
    ATTACK_SOUND_DIR = os.path.join(SOUNDS_DIR, 'attack')
    DEF_MOVE_SOUND = os.path.join(MOVE_SOUND_DIR, 'movement.wav')
    DEF_ATTACK_SOUND = os.path.join(ATTACK_SOUND_DIR, 'attack.wav')
    
    # UI elements
    ATTACKABLE_SQUARE = os.path.join(SPRITES_DIR, 'attackable_square.png')
    DANGEROUS_SQUARE = os.path.join(SPRITES_DIR, 'dangerous_square.png')
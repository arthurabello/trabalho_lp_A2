"""
Manages menu state and configuration.
"""

class MenuState:
    def __init__(self):
        """Initialize menu state."""
        self.running = True
        self.current = "main"
        self.should_start_game = False
        
        self.player1_general = None
        self.player2_general = None
        self.current_selecting_player = 1
        
        self.map_choice = None
        
        self.music_enabled = True
        self.sound_enabled = True
        self.music_volume = 0.7
        self.sound_volume = 0.7
        
        self.setup_general_info()
        
    def setup_general_info(self):
        """Setup general information and bonuses."""
        self.generals = {
            'alexander': {
                'name': 'Alexander the Great of Macedon',
                'bonus': [
                    'Hypaspists: +10% Defense (Passive)',
                    'Hypaspists: +20% Strength in Phalanx',
                    'Hypaspists: +30% Strength w/Alexander'
                ]
            },
            'edward': {
                'name': 'Edward the Elder of Wessex',
                'bonus': [
                    'Archers: +5% Strength (Passive)',
                    'Man-at-arms: +25% Strength w/Edward',
                    'Archers: +25% Str, +5% Def, +1 Move w/Edward'
                ]
            },
            'charlemagne': {
                'name': 'Charlemagne of The Franks',
                'bonus': [
                    'Heavy Cavalry: +5% Defense (Passive)',
                    'Heavy Cavalry: +35% Strength, +1 Move w/Charlemagne'
                ]
            },
            'harald': {
                'name': 'Harald Hardrada of Norway',
                'bonus': [
                    'Vikings: +12% Defense (Passive)',
                    'Vikings: +40% Strength w/Harald',
                    'Archers: +5% Strength (Passive)'
                ]
            },
            'julius': {
                'name': 'Julius Caesar of Rome',
                'bonus': [
                    'Legions: +10% Defense (Passive)',
                    'Light Cav: +5% Strength (Passive)',
                    'Legions: +25% Str, +1 Move w/Julius'
                ]
            },
            'leonidas': {
                'name': 'Leonidas I of Sparta',
                'bonus': [
                    'Hoplites: +20% Defense (Passive)',
                    'Hoplites: +25% Str, +1 Move w/Leonidas'
                ]
            }
        }

    def reset_general_selection(self):
        """Reset general selection state."""
        self.player1_general = None
        self.player2_general = None
        self.current_selecting_player = 1

    def can_start_game(self):
        """Check if game can be started."""
        return (self.player1_general and 
                self.player2_general and 
                self.map_choice is not None)

    def toggle_sound(self, enabled):
        """Toggle sound effects."""
        self.sound_enabled = enabled

    def toggle_music(self, enabled):
        """Toggle background music."""
        self.music_enabled = enabled

    def set_sound_volume(self, volume):
        """Set sound effect volume."""
        self.sound_volume = volume

    def set_music_volume(self, volume):
        """Set background music volume."""
        self.music_volume = volume
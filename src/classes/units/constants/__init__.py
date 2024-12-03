"""
Constants package initialization.
"""

from .colors import Colors
from .armies import Armies
from .maps import Maps
from .paths import Paths
from .unit_defaults import UnitDefaults

# Export all constants classes for easy access
__all__ = [
    'Colors',
    'Formations',
    'Maps',
    'Paths',
    'UnitDefaults'
]
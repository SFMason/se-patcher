"""
games.py - List of all the games this patcher supports.
"""

import os
from typing import Tuple, List, Optional, TypedDict
from collections import namedtuple

# cSpell: words TESV, skse, nvse, fose

Game = namedtuple("Game", ["exe", "se_exe"])

FALLOUT_4 = Game("Fallout4", "f4se")
SKYRIM = Game("TESV", "skse")
FALLOUT_NEW_VEGAS = Game("FalloutNV", "nvse")
FALLOUT_3 = Game("Fallout3", "fose")


def detect_game(path: Optional[str] = None) -> Optional[Game]:
    """Search the current directory for a supported game."""
    if path is None:
        path = os.getcwd()
    for game in (FALLOUT_4, SKYRIM, FALLOUT_NEW_VEGAS, FALLOUT_3):
        if os.path.isfile(os.path.join(path, "{}.exe".format(game.exe))):
            return game
    return None


def patched_game_name(game: Game) -> str:
    """Get the name of the game executable after patching."""
    return ".{}.exe".format(game.exe)

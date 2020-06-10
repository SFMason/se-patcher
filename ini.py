"""
ini.py - Edit the script extender config file.
"""

import os
import configparser
import pathlib

from games import Game, patched_game_name

# cSpell: words unpatched

_CONFIG_SECTION = "Loader"
_CONFIG_KEY = "RuntimeName"


def _get_ini_path(game: Game, install_path: str) -> pathlib.Path:
    path = pathlib.Path(
        os.path.abspath(
            os.path.join(
                install_path, "Data", game.se_exe, "{}.ini".format(game.se_exe)
            )
        )
    )
    path.parent.mkdir(mode=0o775, parents=True, exist_ok=True)
    path.touch(mode=0o775, exist_ok=True)
    return path


def _get_parser(ini_file: str) -> configparser.ConfigParser:
    parser = configparser.ConfigParser()
    if not parser.read(str(ini_file), encoding="utf-8"):
        raise OSError("Could not read script extender config file.")
    if not parser.has_section(_CONFIG_SECTION):
        parser.add_section(_CONFIG_SECTION)
    return parser


def check(install_dir: str, game: Game) -> bool:
    """
    Check whether the game is patched right now according to the script extender ini.
    """
    path = _get_ini_path(game, install_dir)
    parser = _get_parser(str(path))
    try:
        return parser.get(_CONFIG_SECTION, _CONFIG_KEY) == patched_game_name(game)
    except configparser.NoOptionError:
        return False


def patch(install_dir: str, game: Game, install=True):
    """
    Patch the script extender ini.

    Note: assumes that file is in a valid game install directory. It will create
    subdirectories and the config file as necessary.

    :param install_dir: Path to the game's installation directory.
    :param game: The Game to work on.
    :param install: If true, the script extender will be patched in. If false, it will
    be unpatched.
    :raises OSError: Failed to access the config file, maybe due to permissions.
    """
    new_value = patched_game_name(game) if install else game.exe
    path = _get_ini_path(game, install_dir)
    parser = _get_parser(str(path))
    parser.set(_CONFIG_SECTION, _CONFIG_KEY, new_value)

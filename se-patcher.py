import os
import configparser

SE_NAME = ""
GAME_NAME = ""
PATCHED_GAME_NAME = GAME_NAME + "_"


def detectGame():
    Games = [
        ["Fallout4", "f4se"],
        ["TESV", "skse"],
        ["FalloutNV", "nvse"],
        ["Fallout3", "fose"],
    ]
    global SE_NAME
    global GAME_NAME
    global PATCHED_GAME_NAME

    for game in Games:
        if os.path.isfile(game[0] + ".exe"):
            SE_NAME = game[1]
            GAME_NAME = game[0]
            PATCHED_GAME_NAME = GAME_NAME + "_"
            return game[0]
    return None


def joinPath(*dirs):
    dlen = len(dirs)
    if dlen > 1:
        return os.path.join(dirs[0], joinPath(*dirs[1:]))
    if dlen == 1:
        return dirs[0]
    return ""


def editIni(patched):
    """Handles editing the se .ini file to point the se to the correct executable name.
    Will add the option for the executable name if not patched, else will remove the option.
    If patched, this will set up the ini for being unpatched, else it will patch the ini"""

    filePath = os.path.abspath(joinPath("Data", SE_NAME, SE_NAME + ".ini"))
    parser = configparser.ConfigParser()

    print("Reading script extender config file")
    os.makedirs(os.path.abspath(os.path.dirname(filePath)), exist_ok=True)
    with os.fdopen(os.open(filePath, os.O_RDWR | os.O_CREAT), "r+") as configFile:
        parser.read_file(configFile)

    if not parser.has_section("Loader"):
        parser.add_section("Loader")
    parser["Loader"]["RuntimeName"] = (
        GAME_NAME if patched else PATCHED_GAME_NAME
    ) + ".exe"

    print("Updating script extender config file")
    with open(filePath, "r+") as configFile:
        parser.write(configFile)


def patch(patched):
    editIni(patched)

    dir = os.path.dirname(os.getcwd())

    if patched:
        print("Renaming script extender")
        os.rename(GAME_NAME + ".exe", SE_NAME + "_loader.exe")
        print("Renaming game executable")
        os.rename(PATCHED_GAME_NAME + ".exe", GAME_NAME + ".exe")
    else:
        print("Renaming game executable")
        os.rename(GAME_NAME + ".exe", PATCHED_GAME_NAME + ".exe")
        print("Renaming script extender")
        os.rename(SE_NAME + "_loader.exe", GAME_NAME + ".exe")


def main():
    print("Detecting game")
    game = detectGame()
    if game == None:
        print(
            "Error: No valid game found. Make sure that this script is in the same folder as your script extender and game executable."
        )
        return -1
    else:
        print("Game found. Patching for: " + game)

    print("Detecting whether script extender is already patched")
    patched = os.path.exists(joinPath(os.getcwd(), PATCHED_GAME_NAME + ".exe"))
    if patched:
        print("Game is already patched; unpatching.")
    else:
        print("Game is not patched; patching")

    patch(patched)
    print("Done")


if __name__ == "__main__":
    try:
        main()
    finally:
        input("Press enter to continue...")

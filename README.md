# GameVault-IT

![screenshot](https://github.com/Toylerrr/gamevault-it/blob/main/img/Screenshot%202024-01-04%20141009.png?raw=true)

GameVault-IT is a Python script that facilitates zipping the contents of a folder, appending game information from the RAWG API to the name, and optionally using a GUI for user-friendly interaction.

RAWG API is required to match the name to the game https://rawg.io/apidocs

## Features:

- **Folder Zipper:** Zips the contents of a specified folder into a compressed archive.

- **Game Information Appender:** Fetches game information from the RAWG API and appends it to the zip file name.

- **User Interaction:** Provides a graphical user interface (GUI) for easy folder selection, game name input, and API key entry.

- **Command-Line Flags:** Allows the user to pass directory, game, and API key via command-line flags for script automation.

## Usage:

1. **GUI Mode:**
   - Run the script without command-line flags.
   - GUI prompts for folder selection, game name, and API key (if not found in `api.txt`).

2. **Command-Line Flags:**
   - Use `-d` for specifying the directory path.
   - Use `-g` for specifying the game name.
   - Use `-api` for passing the RAWG API key directly.

   Example:
   ```bash
   python gamevault-it.py -d /path/to/folder -g "Game Name" -api YOUR_RAWG_API_KEY
THIS PROJECT IS 100% AI GENERATED 

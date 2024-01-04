import os
import argparse
import tkinter as tk
from tkinter import filedialog, simpledialog
import requests
from zipfile import ZipFile
import re
from PIL import Image, ImageTk
import base64
import io

def scrub_filename(name):
    # Remove special characters and spaces from the name
    return re.sub(r'[^\w\s]', '', name)

def zip_folder(folder_path, zip_filename):
    with ZipFile(zip_filename, 'w') as zip_file:
        for folder_root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(folder_root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zip_file.write(file_path, arcname=arcname)

def get_folder_and_game():
    root = tk.Tk()
    root.title("Folder and Game Input")
    # Display base64 image
    base64_image = " data:image/png;base64,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"
    base64_image = base64_image.split(",")[1]  # Extract the base64 part
    img_data = base64.b64decode(base64_image)

    image = Image.open(io.BytesIO(img_data))
    tk_image = ImageTk.PhotoImage(image)

    img_label = tk.Label(root, image=tk_image)
    img_label.image = tk_image
    img_label.pack()

    # Frame for folder selection
    folder_frame = tk.Frame(root)
    folder_frame.pack(pady=10)

    folder_label = tk.Label(folder_frame, text="Select Folder:")
    folder_label.pack(side="left")

    folder_path_var = tk.StringVar()
    folder_entry = tk.Entry(folder_frame, textvariable=folder_path_var, width=40)
    folder_entry.pack(side="left", padx=5)

    def select_folder():
        folder_path = filedialog.askdirectory(title="Select Folder")
        folder_path_var.set(folder_path)

    folder_button = tk.Button(folder_frame, text="Browse", command=select_folder)
    folder_button.pack(side="left")

    # Frame for game name input
    game_frame = tk.Frame(root)
    game_frame.pack(pady=10)

    game_label = tk.Label(game_frame, text="Enter Game Name:")
    game_label.pack(side="left")

    game_name_var = tk.StringVar()
    game_entry = tk.Entry(game_frame, textvariable=game_name_var, width=40)
    game_entry.pack(side="left", padx=5)

    # Function to close the window
    def close_window():
        root.destroy()

    # OK button to close the window
    ok_button = tk.Button(root, text="OK", command=close_window)
    ok_button.pack(pady=10)



    root.mainloop()

    # Return folder and game name after the window is closed
    return folder_path_var.get(), scrub_filename(game_name_var.get())

def get_api_key(api_key_argument):
    if api_key_argument:
        return api_key_argument
    else:
        api_key_file = 'api.txt'
        if os.path.exists(api_key_file):
            with open(api_key_file, 'r') as file:
                return file.read().strip()
        else:
            print(f'{api_key_file} not found. Asking for API key with GUI.')

            # Ask for API key with a GUI dialog
            api_key = simpledialog.askstring("API Key", "Enter your RAWG API key:")
            
            # Save the entered API key to api.txt
            with open(api_key_file, 'w') as file:
                file.write(api_key)

            return api_key

def get_game_info(game_name, api_key):
    rawg_api_url = "https://api.rawg.io/api/games"
    params = {'key': api_key, 'search': game_name}
    response = requests.get(rawg_api_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['results']:
            game_info = data['results'][0]
            print(f'Game information fetched from RAWG API: {game_info}')
            return game_info
        else:
            print(f'No results found for the game name: {game_name}')
            return None
    else:
        print(f'Error fetching game information from RAWG API. Status Code: {response.status_code}')
        return None

def main():
    parser = argparse.ArgumentParser(description='Zip contents of a folder and append game information from RAWG API to the name')
    parser.add_argument('-d', '--directory', help='Specify the directory path')
    parser.add_argument('-g', '--game', help='Specify the game name')
    parser.add_argument('-api', '--api_key', help='Specify the RAWG API key')
    args = parser.parse_args()

    # If no flags are provided, use GUI for both folder and game prompts
    if not (args.directory and args.game):
        folder_path, game_name_input = get_folder_and_game()
        if not folder_path or not game_name_input:
            return
    else:
        folder_path = args.directory
        game_name_input = args.game

    # Get the API key
    api_key = get_api_key(args.api_key)

    if not api_key:
        print('Error: API key not found.')
        return

    # Use the RAWG API to get game information
    game_info = get_game_info(game_name_input, api_key)

    # Verify if game information is fetched
    if not game_info:
        print('Game information not fetched from RAWG API.')
        return

    # Create the zip file named after the scrubbed game name without underscores
    scrubbed_name = scrub_filename(game_info["name"]).replace('_', '')
    release_year = game_info.get("released", "")[:4]  # Extract the release year
    zip_filename = f'{scrubbed_name} ({release_year}) (W_P).zip'
    zip_folder(folder_path, zip_filename)

    # Print the full location where the zipped game is placed
    full_location = os.path.abspath(zip_filename)
    print(f'Folder "{folder_path}" has been zipped to "{full_location}"')

if __name__ == "__main__":
    main()

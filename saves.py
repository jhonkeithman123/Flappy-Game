import json
import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog

def reset_save_directory_config():
    """Resets the save directory by deleting the configuration file."""
    config_file = Path.home() / ".flappy_config.fgs"
    if config_file.exists():
        config_file.unlink()

def get_user_save_directory():
    """
    Checks for a configuration file holding the user's save directory.
    If not found, prompts the user to choose a folder, then saves and returns that directory.
    """
    config_file = Path.home() / ".flappy_config.fgs"

    if config_file.exists():
        try:
            with config_file.open("r", encoding="utf-8") as f:
                config = json.load(f)
            save_directory = config.get("save_directory")
            if save_directory and Path(save_directory).exists():
                return save_directory
        except (json.JSONDecodeError, ValueError):
            config_file.unlink()  # Reset on error

    # Ask the user to choose a directory
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(title="Select a directory to store game settings and files")
    root.destroy()

    if directory and Path(directory).exists():
        config = {"save_directory": directory}
        with config_file.open("w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
        return directory
    return None


def get_save_dir(user_specified_directory=None):
    """
    Returns a Path object for the save directory.
    If the directory doesn't exist, it is created.
    """
    if not user_specified_directory:
        user_specified_directory = get_user_save_directory()
    save_dir = Path(user_specified_directory) / "FlappySaves"
    save_dir.mkdir(parents=True, exist_ok=True)
    return save_dir

def save_settings(settings, user_directory=None):
    """
    Saves the settings dictionary to the settings.fgs file in the chosen directory.
    """
    save_dir = get_save_dir(user_directory)
    file_path = save_dir / "settings.fgs"
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)
    print(f"Settings saved to: {file_path}")
    return file_path

def load_settings(user_directory=None):
    """
    Loads the settings dictionary from the settings.fgs file.
    If the file does not exist or is invalid, returns an empty dictionary.
    """
    save_dir = get_save_dir(user_directory)
    file_path = save_dir / "settings.fgs"
    if file_path.exists():
        try:
            with file_path.open("r", encoding="utf-8") as f:
                settings = json.load(f)
            print(f"Settings loaded from: {file_path}")
            return settings
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error loading settings: {e}")
            return {}
    else:
        print(f"No settings file found at: {file_path}. Returning empty settings.")
        return {}

def get_save_file_path(filename="data.fgs"):
    """
    Returns the full file path for the given filename within the save directory.
    The default filename uses the .fgs extension.
    """
    save_dir = get_save_dir()
    return save_dir / filename

def load_data(filename="data.fgs"):
    """
    Loads the JSON data from the save file.
    Returns a dictionary with stored data. If the file doesn't exist or is invalid, returns an empty dict.
    """
    file_path = get_save_file_path(filename)
    if not file_path.exists():
        default_data = {
            "high_score": 0,
            "coins": 0,
            "owned_characters": ["default"],
            "selected_character": "default",
        }
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=4)
        print(f"New save file created: {file_path}")
        return default_data
    try:
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data
        else:
            return {}
    except (json.JSONDecodeError, ValueError):
        return {}

def get_character(filename="data.fgs"):
    """Retrieves the selected character from the save file."""
    data = load_data(filename)
    return data.get("selected_character", "default")

def save_character(character, filename="data.fgs"):
    """Updates and saves the selected character in the save file."""
    file_path = get_save_file_path(filename)
    data = load_data(filename)
    data["selected_character"] = character
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    return data["selected_character"]

def get_owned_characters(filename="data.fgs"):
    """Retrieves the owned characters from the save file."""
    data = load_data(filename)
    return set(data.get("owned_characters", ["default"]))

def save_owned_characters(owned_characters, filename="data.fgs"):
    """Saves the owned characters list into the save file."""
    file_path = get_save_file_path(filename)
    data = load_data(filename)
    data["owned_characters"] = list(owned_characters)
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    return data["owned_characters"]

def get_high_score(filename="data.fgs"):
    """Retrieves the stored high score from the save file."""
    data = load_data(filename)
    return data.get("high_score", 0)


def save_high_score(new_score, filename="data.fgs"):
    """
    Compares the new score with the stored high score.
    If new_score is higher, updates the save file.
    """
    file_path = get_save_file_path(filename)
    data = load_data(filename)
    current_high = data.get("high_score", 0)
    if new_score > current_high:
        data["high_score"] = new_score
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return new_score
    return current_high

def get_coins(filename="data.fgs"):
    """Retrieves the stored coin count from the save file."""
    data = load_data(filename)
    return data.get("coins", 0)

def save_coins(new_coins, filename="data.fgs"):
    """Updates the coin count in the save file."""
    file_path = get_save_file_path(filename)
    data = load_data(filename)
    data["coins"] = new_coins
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    return new_coins

# Testing purposes
#if __name__ == "__main__":
#    print("Current High Score:", get_high_score())
#    print("Current Coins:", get_coins())
#    test_coins = 60
#    new_coin_val = save_coins(test_coins)
#    print("New Coins:", new_coin_val)
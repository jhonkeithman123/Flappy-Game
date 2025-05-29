import json
import os
from pathlib import Path
def get_save_dir():
    """
    Returns a Path object for the save directory.
    If the directory doesn't exist, it is created.
    For example, this will create a hidden folder in the user's home directory called "PycharmProjects/flappy/saves".
    """
    home_dir = Path.home()
    save_dir = home_dir / "flappy" / "saves"
    save_dir.mkdir(parents=True, exist_ok=True)
    return save_dir

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
    if file_path.exists():
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
                else:
                    return {}
        except (json.JSONDecodeError, ValueError):
            return {}
    else:
        return {}

def get_high_score(filename="data.fgs"):
    """
    Reads the JSON file at the specified filename (with .fgs extension) stored
    in the save directory, and returns the high score stored there.
    If the file does not exist or is invalid, returns 0.
    """
    data = load_data(filename)
    return data.get("high_score", 0)

def get_coins(filename="data.fgs"):
    """
    Reads the JSON file at the specified filename (with .fgs extension) stored
    in the saved directory, and returns the coins stored there.
    If the file does not exist or is invalid, returns 0.
    """
    data = load_data(filename)
    return data.get("coins", 0)

def save_high_score(new_score, filename="data.fgs"):
    """
    Compares new_score with the stored high score.
    If new_score is higher, updates the JSON file and returns the new high score.
    Otherwise, returns the current high score.
    """
    file_path = get_save_file_path(filename)
    data = load_data(filename)
    current_high = data.get("high_score", 0)
    if new_score > current_high:
        data["high_score"] = new_score
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        return new_score
    return current_high

def save_coins(new_coins, filename="data.fgs"):
    """
    Compares new_coins with the stored coins.
    If new_score is higher, updates the JSON file and returns the new coins.
    Otherwise, returns the current coins.
    """
    file_path = get_save_file_path(filename)
    data = load_data(filename)
    data["coins"] = new_coins
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    return new_coins

# Testing purposes
#if __name__ == "__main__":
#    print("Current High Score:", get_high_score())
#    print("Current Coins:", get_coins())
#    test_coins = 60
#    new_coin_val = save_coins(test_coins)
#    print("New Coins:", new_coin_val)
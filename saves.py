import json
import os
from pathlib import Path
def get_save_dir():
    """
    Returns a Path object for the save directory.
    If the directory doesn't exist, it is created.
    For example, this will create a hidden folder in the user's home directory called "PycharmProjects/flappy/saves".
    """
    save_dir = Path.home() / "PycharmProjects/flappy/saves"
    save_dir.mkdir(exist_ok=True)
    return save_dir

def get_save_file_path(filename="data.fgs"):
    """
    Returns the full file path for the given filename within the save directory.
    The default filename uses the .fgs extension.
    """
    save_dir = get_save_dir()
    return save_dir / filename

def get_high_score(filename="data.fgs"):
    """
    Reads the JSON file at the specified filename (with .fgs extension) stored
    in the save directory, and returns the high score stored there.
    If the file does not exist or is invalid, returns 0.
    """
    file_path = get_save_file_path(filename)
    if file_path.exists():
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("high_score", 0)
        except (json.JSONDecodeError, ValueError):
            return 0
    else:
        return 0
def save_high_score(new_score, filename="data.fgs"):
    """
    Compares new_score with the stored high score.
    If new_score is higher, updates the JSON file and returns the new high score.
    Otherwise, returns the current high score.
    """
    current_high = get_high_score(filename)
    file_path = get_save_file_path(filename)
    if new_score > current_high:
        data = {"high_score": new_score}
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        return new_score
    return current_high

# Testing purposes
#if __name__ == "__main__":
#    print("Current High Score:", get_high_score())
#    test_score = 420
#    new_high = save_high_score(test_score)
#    print("New High Score:", new_high)
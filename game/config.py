
VERSION: str = "v2.3"

# Default resolutions
DEFAULT_WIDTH: int = 800
DEFAULT_HEIGHT: int = 600

# Supported resolutions (width, height)
RESOLUTIONS: list[tuple[int, int]] = [
    (800, 600),
    (1024, 768),
    (1280, 720),
    (1600, 900),
]

# Min/max logical size (min enforced, max used to  cap UI scale)
MIN_WIDTH: int = DEFAULT_WIDTH
MIN_HEIGHT: int = DEFAULT_HEIGHT

# 1080p cap for UI scale
MAX_WIDTH_CAP: int = 1920
MAX_HEIGHT_CAP: int = 1080

# Current resolutions (can be changed by settings)
WIDTH: int = DEFAULT_WIDTH
HEIGHT: int = DEFAULT_HEIGHT

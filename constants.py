from pathlib import Path

WIDTH = 1440
HEIGHT = 720
FPS = 240
MAX_CATCHUP_TIME = 0.25
HEALTHY = [2, 3]
REBIRTH = [3]
CELL_SIZE = 20
FONT_SIZE = 24
CAMERA_SPEED = 600 * FPS
BASE_ZOOMS = [1, 1.5, 2, 2.5, 3, 5, 7]
ZOOMS = [round(zoom*10**i, 4) for i in range(-2, 4) for zoom in BASE_ZOOMS] + [10000]
SPEEDS = [0.1, 0.25, 0.5, 0.75, 1, 2, 3, 4, 6, 8, 10, 15, 20, 30, 40, 60, 80, 120, 160, 200, 240]
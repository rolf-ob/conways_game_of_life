import pygame as py

import time
from collections import defaultdict

from core.input import handle_input
from core.physics import update
from rendering.drawing import draw
from rendering.textcache import TextCache
from entities.sprite import Sprite
from entities.camera import Camera
from entities.frame_limiter import FrameLimiter
from constants import WIDTH, HEIGHT, FPS, FONT_SIZE, SPEEDS, IMAGES_DIR

class Game:
    def __init__(self):
        py.init()

        self.running = True

        self.paused = False
        self.last_update = time.perf_counter()
        self.step_requested = False
        self.speed_index = 9
        self.width = WIDTH
        self.height = HEIGHT
        self.last_click = None
        self.box_start = None
        self.box_end = None
        self.show_grid = True
        self.debug = False
        self.active_cells = set()
        self.selected_cells = []
        self.cells = defaultdict(dict)

        self.camera = Camera(0, 0, 100)
        self.font = py.font.SysFont("Arial", FONT_SIZE)
        self.text_cache = TextCache(self.font)
        self.frame_limiter = FrameLimiter()
        self.screen = py.display.set_mode((WIDTH, HEIGHT), py.RESIZABLE)

        self.sprites = {}
        self.load_assets()

    def load_assets(self):
        for file in IMAGES_DIR.glob("*.png"):
            self.sprites[file.stem] = Sprite(py.image.load(str(file)).convert_alpha())

    def run(self):
        while self.running:
            now = time.perf_counter()

            handle_input(self)

            if not self.paused and now - self.last_update >= 1 / SPEEDS[self.speed_index] or self.step_requested:
                self.last_update = now
                self.step_requested = False
                update(self)
            
            draw(self)

            py.display.flip()
            self.frame_limiter.limit_fps(FPS)
            self.frame_limiter.tick()

        py.quit()
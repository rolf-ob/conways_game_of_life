import pygame as py

import time
from collections import defaultdict

from core.input import handle_input
from core.physics import update
from rendering.drawing import draw
from rendering.textcache import TextCache
from entities.camera import Camera
from entities.frame_limiter import FrameLimiter
from constants import WIDTH, HEIGHT, FPS, FONT_SIZE, IMAGES_DIR

class Game:
    def __init__(self):
        py.init()

        self.running = True

        self.paused = False
        self.last_update = time.perf_counter()
        self.updates_per_second = 10
        self.width = WIDTH
        self.height = HEIGHT
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
            name = file.stem
            image = py.image.load(str(file)).convert_alpha()
            size = image.get_size()
            tinted = self.tint_image(image, size, (0, 255, 0))

            self.sprites[name] = {
                "original image": image,
                "image": image,
                "original size": size,
                "size": size,
                "original tinted": tinted,
                "tinted": tinted
            }

    def tint_image(self, image, size, color):
        tinted_image = image.copy()
        color_surface = py.Surface(size)
        color_surface.fill(color)
        tinted_image.blit(color_surface, (0, 0), special_flags=py.BLEND_RGBA_MULT)
        
        return tinted_image

    def run(self):
        while self.running:
            now = time.perf_counter()

            handle_input(self)

            if not self.paused and now - self.last_update >= 1 / self.updates_per_second or self.last_update == 0:
                self.last_update = now
                update(self)
            
            draw(self)

            py.display.flip()
            self.frame_limiter.limit_fps(FPS)
            self.frame_limiter.tick()

        py.quit()
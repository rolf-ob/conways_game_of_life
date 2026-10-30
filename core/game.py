import pygame as py

from collections import defaultdict

from core.input import handle_input
from core.physics import update
from rendering.drawing import draw
from rendering.textcache import TextCache
from entities.camera import Camera
from entities.frame_limiter import FrameLimiter
from constants import WIDTH, HEIGHT, FRAME_TIME, FONT_SIZE

class Game:
    def __init__(self):
        py.init()

        self.running = True

        self.paused = False
        self.frames_since_update = 0
        self.updates_per_second = 10
        self.width = WIDTH
        self.height = HEIGHT
        self.box_start = None
        self.box_end = None
        self.show_grid = True
        self.debug = False
        self.cells = defaultdict(dict)

        self.camera = Camera(0, 0, 100)
        self.font = py.font.SysFont("Arial", FONT_SIZE)
        self.text_cache = TextCache(self.font)
        self.frame_limiter = FrameLimiter()
        self.screen = py.display.set_mode((WIDTH, HEIGHT), py.RESIZABLE)

    def run(self):
        while self.running:
            if not self.paused:
                self.frames_since_update += 1

            handle_input(self)
            if round(self.frames_since_update, 12) >= (1 / FRAME_TIME) / self.updates_per_second:
                self.frames_since_update = 0
                update(self)
            draw(self)

            py.display.flip()
            self.frame_limiter.limit_fps()
            self.frame_limiter.tick()

        py.quit()
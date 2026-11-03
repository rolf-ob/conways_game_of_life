import pygame as py

import time

from core.input import handle_input
from core.physics import update
from rendering.drawing import draw
from rendering.textcache import TextCache
from entities.camera import Camera
from entities.frame_limiter import FrameLimiter
from constants import WIDTH, HEIGHT, FPS, MAX_CATCHUP_TIME, FONT_SIZE, ZOOMS, SPEEDS

class Game:
    def __init__(self):
        py.init()

        self.running = True

        self.accumulator = 0
        self.last_frame = time.perf_counter()
        self.delta_time = 0

        self.zoom_index = ZOOMS.index(100)
        self.speed_index = SPEEDS.index(8)

        self.width = WIDTH
        self.height = HEIGHT

        self.last_click = None
        self.box_start = None
        self.box_end = None

        self.paused = False
        self.show_grid = True
        self.debug = False

        self.cells = set()
        self.active_cells = set()
        self.selected_cells = set()

        self.camera = Camera(0, 0, ZOOMS[self.zoom_index])
        self.font = py.font.SysFont("Arial", FONT_SIZE)
        self.text_cache = TextCache(self.font)
        self.frame_limiter = FrameLimiter()
        self.screen = py.display.set_mode((WIDTH, HEIGHT), py.RESIZABLE)

    def run(self):
        while self.running:
            now = time.perf_counter()
            self.delta_time = min(now - self.last_frame, MAX_CATCHUP_TIME)
            self.last_frame = now

            handle_input(self)

            if not self.paused:
                self.accumulator += self.delta_time
                period = 1 / SPEEDS[self.speed_index]
                start = time.perf_counter()
                while self.accumulator >= period and time.perf_counter() - start < period * 2:
                    update(self)
                    self.accumulator -= period
                
                if self.accumulator >= period:
                    self.accumulator = 0.0
                    self.frame_limiter.reset()
            
            draw(self)
            py.display.flip()
            self.frame_limiter.limit_fps(FPS)
            self.frame_limiter.tick()

        py.quit()
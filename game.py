import pygame as py

from input import handle_input
from physics import update
from drawing import draw
from camera import Camera
from cell import Cell
from frame_limiter import FrameLimiter
from constants import WIDTH, HEIGHT, CELL_SIZE, FRAME_TIME

class Game:
    def __init__(self):
        py.init()

        self.running = True

        self.paused = False
        self.frames_since_update = 0
        self.updates_per_second = 1
        self.debug = False

        self.cells = [
            [
                Cell(column * CELL_SIZE, row * CELL_SIZE)
                for row in range(HEIGHT // CELL_SIZE)
            ]
            for column in range(WIDTH // CELL_SIZE)
        ]

        self.camera = Camera(0, 0, 1)
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
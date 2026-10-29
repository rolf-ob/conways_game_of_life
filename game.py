import pygame as py

from input import handle_input
from drawing import draw
from camera import Camera
from cell import Cell
from frame_limiter import FrameLimiter
from constants import WIDTH, HEIGHT

class Game:
    def __init__(self):
        py.init()

        self.running = True

        self.cells = [
            Cell(column * 20, row * 20)
            for row in range(HEIGHT // 20)
            for column in range(WIDTH // 20)
        ]

        self.debug = False

        self.camera = Camera(0, 0, 1)
        self.frame_limiter = FrameLimiter()
        self.screen = py.display.set_mode((WIDTH, HEIGHT), py.RESIZABLE)

    def run(self):
        while self.running:
            handle_input(self)
            draw(self)

            py.display.flip()
            self.frame_limiter.limit_fps()
            self.frame_limiter.tick()

        py.quit()
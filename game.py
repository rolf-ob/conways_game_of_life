import pygame as py

from input import handle_input
from drawing import draw
from cell import Cell
from frame_limiter import FrameLimiter
from constants import WIDTH, HEIGHT

class Game:
    def __init__(self):
        py.init()

        self.running = True

        self.cells = []
        for row in range(HEIGHT // 20):
            for column in range(WIDTH // 20):
                self.cells.append(Cell(column * 20, row * 20))

        self.screen = py.display.set_mode((WIDTH, HEIGHT), py.RESIZABLE)
        self.frame_limiter = FrameLimiter()

    def run(self):
        while self.running:
            handle_input(self)
            draw(self)

            py.display.flip()
            self.frame_limiter.limit_fps()
            self.frame_limiter.tick()

        py.quit()
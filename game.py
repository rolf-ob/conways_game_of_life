import pygame as py

from input import handle_input
from drawing import draw
from frame_limiter import FrameLimiter

class Game:
    def __init__(self):
        py.init()

        self.running = True

        self.screen = py.display.set_mode((1440, 720), py.RESIZABLE)
        self.frame_limiter = FrameLimiter()

    def run(self):
        while self.running:
            handle_input(self)
            draw(self)

            py.display.flip()
            self.frame_limiter.limit_fps()
            self.frame_limiter.tick()

        py.quit()
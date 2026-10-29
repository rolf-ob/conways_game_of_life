import pygame as py

from input import handle_input
from drawing import draw

class Game:
    def __init__(self):
        py.init()

        self.running = True

        self.screen = py.display.set_mode((1440, 720), py.RESIZABLE)
        self.clock = py.time.Clock()

    def run(self):
        while self.running:
            handle_input(self)
            draw(self)
            py.display.flip()
            self.clock.tick(240)

        py.quit()
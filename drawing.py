import pygame as py

from spatial import world_to_screen
from constants import CELL_SIZE

def draw_cells(game, screen):
    for row in game.cells:
        for cell in row:
            if cell.alive:
                x, y = world_to_screen(game, cell.x, cell.y)
                py.draw.rect(screen, (255,)*3, (x, y, CELL_SIZE, CELL_SIZE))
                py.draw.rect(screen, (0,)*3, (x, y, CELL_SIZE, CELL_SIZE), 1)

def draw_debug(game, screen):
    pass

def draw(game):
    screen = game.screen
    
    screen.fill((0,)*3)
    draw_cells(game, screen)
    draw_debug(game, screen)
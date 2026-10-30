import pygame as py

from spatial import world_to_screen
from constants import CELL_SIZE

def draw_cells(game, screen):
    for column in game.cells.values():
        for cell in column.values():
            x, y = world_to_screen(game, cell.x, cell.y)
            width = height = CELL_SIZE * game.camera.zoom
            py.draw.rect(screen, (255,)*3, (x, y, width, height))
            py.draw.rect(screen, (0,)*3, (x, y, width, height), 1)

def draw_debug(game, screen):
    margin = 40
    debug_screen = [
        f"FPS {game.frame_limiter.get_fps()}",
        f"Paused: {game.paused}",
        f"Updates/s {game.updates_per_second}",
        f"Position: {game.camera.x} / {game.camera.y}",
        f"Camera zoom: {game.camera.zoom}"
    ]

    for i, line in enumerate(debug_screen):
        screen.blit(game.text_cache.get_surface(line, "screen", (255,)*3), (margin, margin + i*20))

def draw(game):
    screen = game.screen
    
    screen.fill((0,)*3)
    draw_cells(game, screen)
    if game.debug:
        draw_debug(game, screen)
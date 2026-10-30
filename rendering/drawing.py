import pygame as py

from core.spatial import world_to_screen, screen_to_world
from constants import CELL_SIZE

def draw_cells(game, screen):
    start_x, start_y = [coordinate // CELL_SIZE * CELL_SIZE for coordinate in screen_to_world(game, 0, 0)]
    end_x, end_y = [(coordinate + CELL_SIZE) // CELL_SIZE * CELL_SIZE for coordinate in screen_to_world(game, game.width, game.height)]

    viewed_cells = {
        row: {
            column: game.cells[row][column]
            for column in range(start_y, end_y, CELL_SIZE)
            if column in game.cells[row]
        }
        for row in range(start_x, end_x, CELL_SIZE)
        if row in game.cells
    }            

    for column in viewed_cells.values():
        for cell in column.values():
            x, y = world_to_screen(game, cell.x, cell.y)
            width = height = CELL_SIZE * game.camera.zoom / 100
            py.draw.rect(screen, (255,)*3, (x, y, width, height))
            py.draw.rect(screen, (0,)*3, (x, y, width, height), max(1, int(1 * game.camera.zoom / 100)))

def draw_debug(game, screen):
    margin = 40
    debug_screen = [
        f"FPS {game.frame_limiter.get_fps()}",
        f"Paused: {game.paused}",
        f"Updates/s {game.updates_per_second}",
        f"Position: {int(game.camera.x)} / {int(game.camera.y)}",
        f"Camera zoom: {int(game.camera.zoom)}"
    ]

    for i, line in enumerate(debug_screen):
        screen.blit(game.text_cache.get_surface(line, "screen", (255,)*3), (margin, margin + i*20))

def draw(game):
    screen = game.screen
    
    screen.fill((0,)*3)
    draw_cells(game, screen)
    if game.debug:
        draw_debug(game, screen)
import pygame as py

from itertools import product

from core.spatial import world_to_screen, screen_to_world
from constants import CELL_SIZE, FONT_SIZE, SPEEDS
 
def draw_grid(game, screen):
    start_x, start_y = [axis // CELL_SIZE * CELL_SIZE for axis in screen_to_world(game, 0, 0)]
    end_x, end_y = [(axis + CELL_SIZE) // CELL_SIZE * CELL_SIZE for axis in screen_to_world(game, game.width, game.height)]

    for column in range(start_x, end_x, CELL_SIZE):
        x = world_to_screen(game, column, 0)[0]
        py.draw.line(screen, (40,)*3, (x, 0), (x, game.height), max(1, int(1 * game.camera.zoom / 100)))

    for row in range(start_y, end_y, CELL_SIZE):
        y = world_to_screen(game, 0, row)[1]
        py.draw.line(screen, (40,)*3, (0, y), (game.width, y), max(1, int(1 * game.camera.zoom / 100)))

def draw_cells(game, screen):
    start_x, start_y = [axis // CELL_SIZE for axis in screen_to_world(game, 0, 0)]
    end_x, end_y = [(axis + CELL_SIZE) // CELL_SIZE for axis in screen_to_world(game, game.width, game.height)]

    viewed_cells = (
        game.cells.intersection(product(range(start_x, end_x), range(start_y, end_y)))
        if (end_x - start_x) * (end_y - start_y) <= len(game.cells) else
        {cell for cell in game.cells if start_x <= cell[0] < end_x and start_y <= cell[1] < end_y}
    )

    x_center = game.width / 2
    y_center = game.height / 2
    camera_x_offset = -game.camera.x - x_center
    camera_y_offset = -game.camera.y - y_center
    zoom = game.camera.zoom / 100
    dimensions = (max(1, CELL_SIZE * zoom),) * 2

    for cell in viewed_cells:
        color = (0, 255, 0) if cell in game.selected_cells else (255,)*3
        x = (cell[0] * CELL_SIZE + camera_x_offset) * zoom + x_center
        y = (cell[1] * CELL_SIZE + camera_y_offset) * zoom + y_center

        py.draw.rect(screen, color, (x, y, *dimensions))
        if zoom >= 1:
            py.draw.rect(screen, (0,)*3, (x, y, *dimensions), int(zoom))
            
def draw_selection_box(game, screen):
    x, y = world_to_screen(game,
        min(game.box_start[0], game.box_end[0]),
        min(game.box_start[1], game.box_end[1])
    )
    x2, y2 = world_to_screen(game,
        max(game.box_start[0], game.box_end[0]),
        max(game.box_start[1], game.box_end[1])
    )
    py.draw.rect(screen, (0, 200, 0), (x, y, x2-x, y2-y), 1)

def draw_debug(game, screen):
    debug_screen = [
        f"FPS: {game.frame_limiter.get_fps()}",
        f"Paused: {game.paused}",
        f"Updates per second: {SPEEDS[game.speed_index]}",
        f"Checks per update: {len(game.changed_cells)}",
        f"Live cells: {len(game.cells)}",
        f"Position: {int(game.camera.x)} / {int(game.camera.y)}",
        f"Camera zoom: {round(game.camera.zoom / 100, 4)}",
    ]
    for i, line in enumerate(debug_screen):
        if i != 5:
            screen.blit(game.text_cache.get_surface(line, "screen", (255,)*3), (FONT_SIZE, FONT_SIZE + i*FONT_SIZE))
        else:
            screen.blit(game.font.render(line, True, (255,)*3), (FONT_SIZE, FONT_SIZE + i*FONT_SIZE))

def draw(game):
    screen = game.screen
    
    screen.fill((0, 0, 20))

    if game.show_grid and game.camera.zoom > 50:
        draw_grid(game, screen)

    draw_cells(game, screen)

    if game.box_start:
        draw_selection_box(game, screen)

    if game.debug:
        draw_debug(game, screen)
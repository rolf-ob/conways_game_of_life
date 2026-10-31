import pygame as py

from core.spatial import world_to_screen, screen_to_world
from constants import CELL_SIZE

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
    start_x, start_y = [axis // CELL_SIZE * CELL_SIZE for axis in screen_to_world(game, 0, 0)]
    end_x, end_y = [(axis + CELL_SIZE) // CELL_SIZE * CELL_SIZE for axis in screen_to_world(game, game.width, game.height)]

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
            if cell.selected:
                image = game.tint_image(game.sprites["cell"], (0, 255, 0, 128))
            else:
                image = game.sprites["cell"]["image"]
            
            position = world_to_screen(game, cell.x, cell.y)
            screen.blit(image, position)
            
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
    
    screen.fill((0, 0, 20))

    if game.show_grid and game.camera.zoom > 50:
        draw_grid(game, screen)

    draw_cells(game, screen)

    if game.box_start:
        draw_selection_box(game, screen)

    if game.debug:
        draw_debug(game, screen)
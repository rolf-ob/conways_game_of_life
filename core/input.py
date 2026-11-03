import pygame as py

from itertools import product

from core.physics import update
from core.world import move_cells, heal_cells, heal_cell, kill_cell, select_cell
from core.spatial import screen_to_world
from constants import CELL_SIZE, CAMERA_SPEED, ZOOMS, SPEEDS

def move_camera(game, keys):
    if keys[py.K_w]:
        game.camera.y -= CAMERA_SPEED / game.camera.zoom * game.delta_time
    if keys[py.K_a]:
        game.camera.x -= CAMERA_SPEED / game.camera.zoom * game.delta_time
    if keys[py.K_s]:
        game.camera.y += CAMERA_SPEED / game.camera.zoom * game.delta_time
    if keys[py.K_d]:
        game.camera.x += CAMERA_SPEED / game.camera.zoom * game.delta_time

def zoom(game, y):
    game.zoom_index = max(0, min(len(ZOOMS)-1, game.zoom_index + y))
    game.camera.zoom = ZOOMS[game.zoom_index]

def handle_input(game):
    keys = py.key.get_pressed()
    clicking = py.mouse.get_pressed()

    if not keys[py.K_LCTRL]:
        move_camera(game, keys)

    if keys[py.K_LSHIFT] and clicking[0]:
        x, y = [axis // CELL_SIZE for axis in screen_to_world(game, *py.mouse.get_pos())]
        heal_cells(game, x, y)
        game.last_click = x, y
    else:
        game.last_click = None

    if game.paused and keys[py.K_LSHIFT] and clicking[2]:
        world_x, world_y = screen_to_world(game, *py.mouse.get_pos())
        if game.box_start is None:
            game.box_start = (world_x, world_y)
        game.box_end = (world_x, world_y)
        
    elif game.box_start is not None:
        x = min(game.box_start[0], game.box_end[0])
        y = min(game.box_start[1], game.box_end[1])
        width = abs(game.box_end[0] - game.box_start[0])
        height = abs(game.box_end[1] - game.box_start[1])
        start_x, start_y = [axis // CELL_SIZE for axis in (x, y)]
        end_x, end_y = [(axis + CELL_SIZE) // CELL_SIZE for axis in (x + width, y + height)]

        cells_in_box = (
            game.cells.intersection(product(range(start_x, end_x), range(start_y, end_y)))
            if (end_x - start_x) * (end_y - start_y) <= len(game.cells) else
            {cell for cell in game.cells if start_x <= cell[0] < end_x and start_y <= cell[1] < end_y}
        )

        for cell in cells_in_box:
            if cell not in game.selected_cells:
                game.selected_cells.add(cell)

        game.box_start = None
        game.box_end = None

    for event in py.event.get():
        if event.type == py.QUIT:
            game.running = False

        elif event.type == py.VIDEORESIZE:
            game.width, game.height = event.size

        elif event.type == py.KEYDOWN:
            if keys[py.K_LCTRL]:
                if event.key == py.K_w:
                    move_cells(game, 0, -1)
                elif event.key == py.K_a:
                    move_cells(game, -1, 0)
                elif event.key == py.K_s:
                    move_cells(game, 0, 1)
                elif event.key == py.K_d:
                    move_cells(game, 1, 0)
            
            if event.key == py.K_SPACE:
                game.paused = not game.paused
                if not game.paused:
                    game.selected_cells.clear()

            elif event.key == py.K_q:
                game.speed_index = max(0, game.speed_index - 1)

            elif event.key == py.K_e:
                game.speed_index = min(len(SPEEDS)-1, game.speed_index + 1)

            elif event.key == py.K_r:
                game.selected_cells.clear()
                game.cells.clear()
                game.changed_cells.clear()
                game.neighbour_amounts.clear()

            elif event.key == py.K_g:
                game.show_grid = not game.show_grid

            elif event.key == py.K_u:
                game.selected_cells.clear()

            elif event.key == py.K_BACKSPACE:
                for cell in game.selected_cells:
                    kill_cell(game, cell)
                game.selected_cells.clear()

            elif event.key == py.K_TAB:
                if game.paused:
                    game.selected_cells.clear()
                    update(game)
            
            elif event.key == py.K_F3:
                game.debug = not game.debug

        elif event.type == py.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not keys[py.K_LSHIFT]:
                    x, y = [axis // CELL_SIZE for axis in screen_to_world(game, *event.pos)]
                    cell = (x, y)

                    if cell in game.cells:
                        kill_cell(game, cell)
                    else:
                        heal_cell(game, cell)

            elif event.button == 3:
                if game.paused and not keys[py.K_LSHIFT]:
                    x, y = [axis // CELL_SIZE for axis in screen_to_world(game, *event.pos)]
                    cell = (x, y)
                    select_cell(game, cell)

        elif event.type == py.MOUSEWHEEL:
            zoom(game, event.y)
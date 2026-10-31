import pygame as py

from collections import defaultdict

from entities.world import move_cells, heal_cells, heal_cell, select_cell, deselect_cells, kill_cells
from core.spatial import screen_to_world
from constants import CELL_SIZE, FPS, SPEEDS

def move_camera(game, keys):
    if keys[py.K_w]:
        game.camera.y -= 600 / game.camera.zoom * FPS / game.frame_limiter.get_fps()
    if keys[py.K_a]:
        game.camera.x -= 600 / game.camera.zoom * FPS / game.frame_limiter.get_fps()
    if keys[py.K_s]:
        game.camera.y += 600 / game.camera.zoom * FPS / game.frame_limiter.get_fps()
    if keys[py.K_d]:
        game.camera.x += 600 / game.camera.zoom * FPS / game.frame_limiter.get_fps()

def zoom(game, y):
    game.camera.zoom = min(1084, max(5.21, game.camera.zoom * 1.1 ** y))

    game.sprites["cell"].size = [
        size * game.camera.zoom / 100
        for size in game.sprites["cell"].original_size
    ]
    for sprite in ("image", "tinted"):
        setattr(game.sprites["cell"], sprite,
            py.transform.scale(
                getattr(game.sprites["cell"], f"original_{sprite}"),
                game.sprites["cell"].size
            ))

def handle_input(game):
    keys = py.key.get_pressed()
    clicking = py.mouse.get_pressed()

    if not keys[py.K_LCTRL]:
        move_camera(game, keys)

    if keys[py.K_LSHIFT] and clicking[0]:
        mouse_x, mouse_y = py.mouse.get_pos()
        heal_cells(game, *screen_to_world(game, mouse_x, mouse_y))
        game.last_click = mouse_x, mouse_y
    else:
        game.last_click = None

    if game.paused and keys[py.K_LSHIFT] and clicking[2]:
        mouse_x, mouse_y = screen_to_world(game, *py.mouse.get_pos())
        if not game.box_start:
            game.box_start = (mouse_x, mouse_y)
        game.box_end = (mouse_x, mouse_y)
        
    elif game.box_start:
        x = min(game.box_start[0], game.box_end[0])
        y = min(game.box_start[1], game.box_end[1])
        width = abs(game.box_end[0] - game.box_start[0])
        height = abs(game.box_end[1] - game.box_start[1])
        start_x, start_y = [axis // CELL_SIZE for axis in (x, y)]
        end_x, end_y = [(axis + CELL_SIZE) // CELL_SIZE for axis in (x + width, y + height)]
        
        cells_in_box = [
            game.cells[row][column]
            for row in range(start_x, end_x)
            if row in game.cells
            for column in range(start_y, end_y)
            if column in game.cells[row]
        ]

        for cell in cells_in_box:
            if not cell.selected:
                cell.selected = True
                game.selected_cells.append(cell)

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
                    game.last_update = 0
                    deselect_cells(game)

            elif event.key == py.K_q:
                game.speed_index = max(0, game.speed_index - 1)

            elif event.key == py.K_e:
                game.speed_index = min(len(SPEEDS)-1, game.speed_index + 1)

            elif event.key == py.K_r:
                deselect_cells(game)
                game.cells = defaultdict(dict)

            elif event.key == py.K_g:
                game.show_grid = not game.show_grid

            elif event.key == py.K_u:
                deselect_cells(game)

            elif event.key == py.K_BACKSPACE:
                kill_cells(game)

            elif event.key == py.K_TAB:
                if game.paused:
                    deselect_cells(game)
                    game.step_requested = True
            
            elif event.key == py.K_F3:
                game.debug = not game.debug

        elif event.type == py.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                heal_cell(game, *screen_to_world(game, mouse_x, mouse_y))

            elif event.button == 3:
                if game.paused and not keys[py.K_LSHIFT]:
                    mouse_x, mouse_y = event.pos
                    select_cell(game, *screen_to_world(game, mouse_x, mouse_y))

        elif event.type == py.MOUSEWHEEL:
            zoom(game, event.y)
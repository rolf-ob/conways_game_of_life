import pygame as py

from collections import defaultdict

from core.spatial import screen_to_world
from entities.cell import Cell
from constants import CELL_SIZE, FRAME_TIME

def heal_cells(game, mouse_x, mouse_y):    
    if game.last_click and game.last_click != (mouse_x, mouse_y):
        dx = (mouse_x - game.last_click[0])
        dy = (mouse_y - game.last_click[1])
        step = abs(dx) if abs(dx) >= abs(dy) else abs(dy)
        dx /= step
        dy /= step
        x = game.last_click[0]
        y = game.last_click[1]

        for _ in range(step):
            heal_cell(game, int(x // CELL_SIZE * CELL_SIZE), int(y // CELL_SIZE * CELL_SIZE))
            x += dx
            y += dy

    heal_cell(game, mouse_x, mouse_y)

def heal_cell(game, x, y):
    grid_x = x // CELL_SIZE * CELL_SIZE
    grid_y = y // CELL_SIZE * CELL_SIZE
    game.cells[grid_x][grid_y] = Cell(grid_x, grid_y)

def select_cell(game, x, y):
    grid_x = x // CELL_SIZE * CELL_SIZE
    grid_y = y // CELL_SIZE * CELL_SIZE

    if grid_x in game.cells and grid_y in game.cells[grid_x]:
        cell = game.cells[grid_x][grid_y]

        cell.selected = not cell.selected
        if cell.selected:
            game.selected_cells.append(cell)
        else:
            game.selected_cells.remove(cell)

def kill_cells(game):
    for cell in game.selected_cells.copy():
        del game.cells[cell.x][cell.y]
        game.selected_cells.remove(cell)

def change_speed(game, way, shift):
    micro = True if (
        way == "down" and game.updates_per_second <= 1 or
        way == "up" and game.updates_per_second < 1
        ) else False
    change = -1 if way == "down" else 1
    if shift and not (micro and way == "down"):
        change *= 10

    if micro:
        game.updates_per_second = max(0.1, round(game.updates_per_second + change/10, 1))
    else:
        game.updates_per_second = max(0.1, round(game.updates_per_second + change))

def zoom(game, y):
    if y > 0:
        game.camera.zoom = game.camera.zoom + game.camera.zoom / 10 * y
    else:
        game.camera.zoom = max(5, game.camera.zoom + game.camera.zoom / 10 / y)

def handle_input(game):
    keys = py.key.get_pressed()
    clicking = py.mouse.get_pressed()
    
    if keys[py.K_w]:
        game.camera.y -= 600 / game.camera.zoom
    if keys[py.K_a]:
        game.camera.x -= 600 / game.camera.zoom
    if keys[py.K_s]:
        game.camera.y += 600 / game.camera.zoom
    if keys[py.K_d]:
        game.camera.x += 600 / game.camera.zoom

    if keys[py.K_LSHIFT] and clicking[0]:
        mouse_x, mouse_y = [axis // CELL_SIZE * CELL_SIZE for axis in screen_to_world(game, *py.mouse.get_pos())]
        heal_cells(game, mouse_x, mouse_y)
        game.last_click = mouse_x, mouse_y
    else:
        game.last_click = None

    if keys[py.K_LSHIFT] and clicking[2]:
        mouse_x, mouse_y = screen_to_world(game, *py.mouse.get_pos())
        if not game.box_start:
            game.box_start = (mouse_x, mouse_y)
        game.box_end = (mouse_x, mouse_y)
        
    elif game.box_start:
        x = min(game.box_start[0], game.box_end[0])
        y = min(game.box_start[1], game.box_end[1])
        width = abs(game.box_end[0] - game.box_start[0])
        height = abs(game.box_end[1] - game.box_start[1])
        start_x, start_y = [axis // CELL_SIZE * CELL_SIZE for axis in screen_to_world(game, x, y)]
        end_x, end_y = [(axis + CELL_SIZE) // CELL_SIZE * CELL_SIZE for axis in screen_to_world(game, x + width, y + height)]
        
        cells_in_box = [
            game.cells[row][column]
            for row in range(start_x, end_x, CELL_SIZE)
            if row in game.cells
            for column in range(start_y, end_y, CELL_SIZE)
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
            if event.key == py.K_SPACE:
                game.paused = not game.paused

            elif event.key == py.K_q:
                change_speed(game, "down", keys[py.K_LSHIFT])

            elif event.key == py.K_e:
                change_speed(game, "up", keys[py.K_LSHIFT])

            elif event.key == py.K_r:
                game.cells = defaultdict(dict)

            elif event.key == py.K_g:
                game.show_grid = not game.show_grid

            elif event.key == py.K_BACKSPACE:
                kill_cells(game)

            elif event.key == py.K_TAB:
                game.frames_since_update = (1 / FRAME_TIME) / game.updates_per_second
            
            elif event.key == py.K_F3:
                game.debug = not game.debug

        elif event.type == py.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                heal_cell(game, *screen_to_world(game, mouse_x, mouse_y))

            elif event.button == 3 and not keys[py.K_LSHIFT]:
                mouse_x, mouse_y = event.pos
                select_cell(game, *screen_to_world(game, mouse_x, mouse_y))

        elif event.type == py.MOUSEWHEEL:
            zoom(game, event.y)
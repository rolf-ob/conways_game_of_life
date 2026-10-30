import pygame as py

from collections import defaultdict

from core.spatial import screen_to_world
from entities.cell import Cell
from constants import CELL_SIZE, FRAME_TIME

def heal_cell(game, x, y):
    grid_x = x // CELL_SIZE * CELL_SIZE
    grid_y = y // CELL_SIZE * CELL_SIZE
    game.cells[grid_x][grid_y] = Cell(grid_x, grid_y)

def kill_cell(game, x, y):
    grid_x = x // CELL_SIZE * CELL_SIZE
    grid_y = y // CELL_SIZE * CELL_SIZE

    if grid_x in game.cells and grid_y in game.cells[grid_x]:
        del game.cells[grid_x][grid_y]

def change_speed(game, way):
    game.frames_since_update = 0

    micro = True if (
        way == "down" and game.updates_per_second <= 1 or
        way == "up" and game.updates_per_second < 1
        ) else False
    change = -1 if way == "down" else 1

    if game.updates_per_second > 0.1 or change == 1:
        if micro:
            game.updates_per_second = round(game.updates_per_second + change/10, 1)
        else:
            game.updates_per_second += change

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
        mouse_x, mouse_y = py.mouse.get_pos()
        heal_cell(game, *screen_to_world(game, mouse_x, mouse_y))
    
    if keys[py.K_LSHIFT] and clicking[2]:
        mouse_x, mouse_y = py.mouse.get_pos()
        kill_cell(game, *screen_to_world(game, mouse_x, mouse_y))

    if keys[py.K_LCTRL] and clicking[2]:
        if not game.box_start:
            game.box_start = py.mouse.get_pos()
        game.box_end = py.mouse.get_pos()

    else:
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
                change_speed(game, "down")

            elif event.key == py.K_e:
                change_speed(game, "up")

            elif event.key == py.K_r:
                game.cells = defaultdict(dict)

            elif event.key == py.K_g:
                game.show_grid = not game.show_grid

            elif event.key == py.K_TAB:
                game.frames_since_update = (1 / FRAME_TIME) / game.updates_per_second
            
            elif event.key == py.K_F3:
                game.debug = not game.debug

        elif event.type == py.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                heal_cell(game, *screen_to_world(game, mouse_x, mouse_y))

            elif event.button == 3:
                mouse_x, mouse_y = event.pos
                kill_cell(game, *screen_to_world(game, mouse_x, mouse_y))

        elif event.type == py.MOUSEWHEEL:
            zoom(game, event.y)
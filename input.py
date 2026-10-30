import pygame as py

from spatial import screen_to_world
from cell import Cell
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

def zoom(game, y):
    if y > 0:
        game.camera.zoom = game.camera.zoom + game.camera.zoom / 10 * y
    else:
        game.camera.zoom = max(15, game.camera.zoom + game.camera.zoom / 10 / y)

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

    for event in py.event.get():
        if event.type == py.QUIT:
            game.running = False

        elif event.type == py.VIDEORESIZE:
            game.width, game.height = event.size

        elif event.type == py.KEYDOWN:
            if event.key == py.K_SPACE:
                game.paused = not game.paused

            elif event.key == py.K_q:
                game.frames_since_update = 0

                if game.updates_per_second > 0.1:
                    if game.updates_per_second <= 1:
                        game.updates_per_second = round(game.updates_per_second - 0.1, 1)
                    else:
                        game.updates_per_second -= 1

            elif event.key == py.K_e:
                game.frames_since_update = 0

                if game.updates_per_second < 1:
                    game.updates_per_second = round(game.updates_per_second + 0.1, 1)
                else:
                    game.updates_per_second += 1

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
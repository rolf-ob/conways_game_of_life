import pygame as py

from spatial import screen_to_world
from constants import CELL_SIZE

def heal_cell(game, x, y):
    grid_x = x // CELL_SIZE
    grid_y = y // CELL_SIZE

    if 0 <= grid_x < len(game.cells) and 0 <= grid_y < len(game.cells[0]):
        game.cells[grid_x][grid_y].alive = True

def zoom(game, y):
    game.camera.zoom += y

def handle_input(game):
    keys = py.key.get_pressed()
    clicking = py.mouse.get_pressed()
    
    if keys[py.K_w]:
        game.camera.y -= 10
    if keys[py.K_a]:
        game.camera.x -= 10
    if keys[py.K_s]:
        game.camera.y += 10
    if keys[py.K_d]:
        game.camera.x += 10

    if keys[py.K_LSHIFT] and clicking[0]:
        mouse_x, mouse_y = py.mouse.get_pos()
        heal_cell(game, *screen_to_world(game, mouse_x, mouse_y))

    for event in py.event.get():
        if event.type == py.QUIT:
            game.running = False

        elif event.type == py.KEYDOWN:
            if event.key == py.K_F3:
                game.debug = not game.debug

        elif event.type == py.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = py.mouse.get_pos()
            heal_cell(game, *screen_to_world(game, mouse_x, mouse_y))

        elif event.type == py.MOUSEWHEEL:
            zoom(game, event.y)
import pygame as py

def world_to_screen(game, world_x, world_y):
    screen_x = world_x - game.camera.x
    screen_y = world_y - game.camera.y

    return screen_x, screen_y

def draw_cells(game, screen):
    for cell in game.cells:
        x, y = world_to_screen(game, cell.x, cell.y)
        py.draw.rect(screen, (255,)*3, (x, y, 20, 20))
        py.draw.rect(screen, (0,)*3, (x, y, 20, 20), 1)

def draw_debug(game, screen):
    pass

def draw(game):
    screen = game.screen
    
    screen.fill((0,)*3)
    draw_cells(game, screen)
    draw_debug(game, screen)
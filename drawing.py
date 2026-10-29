import pygame as py

def draw(game):
    screen = game.screen

    screen.fill((0,)*3)

    for cell in game.cells:
        py.draw.rect(screen, (255,)*3, (cell.x, cell.y, 20, 20), 1)
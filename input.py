import pygame as py

def handle_input(game):
    for event in py.event.get():
        if event.type == py.QUIT:
            game.running = False
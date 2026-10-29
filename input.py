import pygame as py

def zoom(game, y):
    game.camera.zoom += y

def handle_input(game):
    keys = py.key.get_pressed()
    
    if keys[py.K_w]:
        game.camera.y -= 10
    if keys[py.K_a]:
        game.camera.x -= 10
    if keys[py.K_s]:
        game.camera.y += 10
    if keys[py.K_d]:
        game.camera.x += 10

    for event in py.event.get():
        if event.type == py.QUIT:
            game.running = False

        elif event.type == py.KEYDOWN:
            pass

        elif event.type == py.MOUSEBUTTONDOWN:
            if event.key == py.K_F3:
                game.debug = not game.debug

        elif event.type == py.MOUSEWHEEL:
            zoom(game, event.y)
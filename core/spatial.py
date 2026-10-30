def world_to_screen(game, world_x, world_y):
    zoom = game.camera.zoom / 100
    screen_x = (world_x - game.camera.x - game.width / 2) * zoom + game.width / 2
    screen_y = (world_y - game.camera.y - game.height / 2) * zoom + game.height / 2
    return int(screen_x), int(screen_y)

def screen_to_world(game, screen_x, screen_y):
    zoom = game.camera.zoom / 100
    world_x = (screen_x - game.width / 2) / zoom + game.camera.x + game.width / 2
    world_y = (screen_y - game.height / 2) / zoom + game.camera.y + game.height / 2
    return int(world_x), int(world_y)
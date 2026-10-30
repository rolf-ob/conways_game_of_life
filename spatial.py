from constants import WIDTH, HEIGHT

def world_to_screen(game, world_x, world_y):
    screen_x = (world_x - game.camera.x - WIDTH / 2) * game.camera.zoom + WIDTH / 2
    screen_y = (world_y - game.camera.y - HEIGHT / 2) * game.camera.zoom + HEIGHT / 2
    return int(screen_x), int(screen_y)

def screen_to_world(game, screen_x, screen_y):
    world_x = (screen_x - WIDTH / 2) / game.camera.zoom + game.camera.x + WIDTH / 2
    world_y = (screen_y - HEIGHT / 2) / game.camera.zoom + game.camera.y + HEIGHT / 2
    return int(world_x), int(world_y)
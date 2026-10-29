def world_to_screen(game, world_x, world_y):
    screen_x = world_x - game.camera.x
    screen_y = world_y - game.camera.y
    return screen_x, screen_y

def screen_to_world(game, screen_x, screen_y):
    world_x = screen_x + game.camera.x
    world_y = screen_y + game.camera.y
    return world_x, world_y
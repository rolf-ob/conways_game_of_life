from constants import CELL_SIZE

def move_cells(game, move_x, move_y):
    target_cells = game.selected_cells.copy()
    game.selected_cells.clear()
    
    for cell in target_cells:
        game.cells.remove(cell)
        game.changed_cells.add(cell)

    for cell in target_cells:
        distance = max(1, 100 // game.camera.zoom) ** 2
        x = cell[0] + move_x * distance
        y = cell[1] + move_y * distance
        game.cells.add((x, y))
        game.selected_cells.add((x, y))
        game.changed_cells.add((x, y))

def heal_cells(game, world_x, world_y):  
    if game.last_click and game.last_click != (world_x, world_y):
        dx = (world_x - game.last_click[0])
        dy = (world_y - game.last_click[1])
        step = abs(dx) if abs(dx) >= abs(dy) else abs(dy)
        dx /= step
        dy /= step
        x = game.last_click[0]
        y = game.last_click[1]

        for _ in range(step):
            toggle_cell(game, x, y)
            x += dx
            y += dy
    toggle_cell(game, world_x, world_y)

def toggle_cell(game, world_x, world_y, kill=False):
    cell = (
        int(world_x // CELL_SIZE),
        int(world_y // CELL_SIZE)
    )

    if cell not in game.cells:
        game.cells.add(cell)

    elif kill:
        game.cells.remove(cell)
        if cell in game.selected_cells:
            game.selected_cells.remove(cell)

    game.changed_cells.add(cell)

def select_cell(game, world_x, world_y):
    cell = (
        int(world_x // CELL_SIZE),
        int(world_y // CELL_SIZE)
    )

    if cell in game.cells:
        if cell not in game.selected_cells:
            game.selected_cells.add(cell)
        else:
            game.selected_cells.remove(cell)

def kill_cells(game):
    for cell in game.selected_cells:
        game.cells.remove(cell)
        game.changed_cells.add(cell)
    game.selected_cells.clear()
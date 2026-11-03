from constants import CELL_SIZE

def move_cells(game, move_x, move_y):
    target_cells = game.selected_cells.copy()
    game.selected_cells.clear()
    
    for cell in target_cells:
        kill_cell(game, cell)

    for cell in target_cells:
        distance = max(1, 100 // game.camera.zoom) ** 2
        x = cell[0] + move_x * distance
        y = cell[1] + move_y * distance

        heal_cell(game, cell)
        game.selected_cells.add((x, y))

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
            cell = (x // CELL_SIZE, y // CELL_SIZE)
            if cell not in game.cells:
                heal_cell(game, cell)
            x += dx
            y += dy
    cell = (world_x // CELL_SIZE, world_y // CELL_SIZE)
    if cell not in game.cells:
        heal_cell(game, cell)

def select_cell(game, cell):
    if cell in game.cells:
        if cell not in game.selected_cells:
            game.selected_cells.add(cell)
        else:
            game.selected_cells.remove(cell)

def heal_cell(game, cell):
    game.cells.add(cell)
    game.changed_cells.add(cell)
    
    for other_cell in [(cell[0]+x, cell[1]+y) for x in (-1, 0, 1) for y in (-1, 0, 1)]:
        if other_cell != cell:
            game.neighbour_amounts[other_cell] += 1

def kill_cell(game, cell):
    game.cells.remove(cell)
    game.changed_cells.add(cell)

    for other_cell in [(cell[0]+x, cell[1]+y) for x in (-1, 0, 1) for y in (-1, 0, 1)]:
        if other_cell != cell:
            game.neighbour_amounts[other_cell] -= 1
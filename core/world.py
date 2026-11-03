def move_cells(game, move_x, move_y):
    distance = max(1, 100 // game.camera.zoom) ** 2
    distance_x = move_x * distance
    distance_y = move_y * distance

    target_cells = game.selected_cells.copy()
    game.selected_cells.clear()
    
    for cell in target_cells:
        kill_cell(game, cell)

    for cell in target_cells:
        x = cell[0] + distance_x
        y = cell[1] + distance_y

        heal_cell(game, (x, y))
        game.selected_cells.add((x, y))

def heal_cells(game, x, y):  
    if game.last_click is not None and game.last_click != (x, y):
        dx = (x - game.last_click[0])
        dy = (y - game.last_click[1])
        step = abs(dx) if abs(dx) >= abs(dy) else abs(dy)
        dx /= step
        dy /= step
        new_x = game.last_click[0]
        new_y = game.last_click[1]

        for _ in range(step):
            if (new_x, new_y) not in game.cells:
                heal_cell(game, (int(new_x), int(new_y)))
            new_x += dx
            new_y += dy
    
    if (x, y) not in game.cells:
        heal_cell(game, (x, y))

def select_cell(game, cell):
    if cell in game.cells:
        if cell not in game.selected_cells:
            game.selected_cells.add(cell)
        else:
            game.selected_cells.remove(cell)

def heal_cell(game, cell):
    if cell in game.cells:
        return

    game.cells.add(cell)
    game.changed_cells.add(cell)
    
    for other_cell in [(cell[0]+x, cell[1]+y) for x in (-1, 0, 1) for y in (-1, 0, 1)]:
        if other_cell != cell:
            game.neighbour_amounts[other_cell] = game.neighbour_amounts.get(other_cell, 0) + 1

def kill_cell(game, cell):
    if cell not in game.cells:
        return

    game.cells.remove(cell)
    game.changed_cells.add(cell)

    for other_cell in [(cell[0]+x, cell[1]+y) for x in (-1, 0, 1) for y in (-1, 0, 1)]:
        if other_cell != cell:
            game.neighbour_amounts[other_cell] = game.neighbour_amounts.get(other_cell, 0) - 1
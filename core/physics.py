def get_cell_condition(game, cells, cell):
    neighbor_amount = 0
    for other_x in range(cell[0] - 1, cell[0] + 2):
        for other_y in range(cell[1] - 1, cell[1] + 2):
            if not (other_x == cell[0] and other_y == cell[1]):
                if (other_x, other_y) in game.cells:
                    neighbor_amount += 1

    if cell in game.cells:
        if neighbor_amount < 2 or neighbor_amount > 3:
            cells["dying"].append(cell)

    elif neighbor_amount == 3:
        cells["healing"].append(cell)

def update(game):
    cells = {
        "dying": [],
        "healing": [],
    }

    cell_checks = {
        (x+x2, y+y2) for x2 in (-1, 0, 1) for y2 in (-1, 0, 1)
        for (x, y) in game.changed_cells
    }

    for cell in cell_checks:
        get_cell_condition(game, cells, cell)
    game.changed_cells.clear()

    for cell in cells["dying"]:
        game.cells.remove(cell)
        game.changed_cells.add(cell)

    for cell in cells["healing"]:
        game.cells.add(cell)
        game.changed_cells.add(cell)
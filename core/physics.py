def get_cell_condition(game, cells, cell, active=False):
    if cell not in cells["seen"]:
        cells["seen"].add(cell)

        neighbor_amount = 0
        for other_x in range(cell[0] - 1, cell[0] + 2):
            for other_y in range(cell[1] - 1, cell[1] + 2):
                if not (other_x == cell[0] and other_y == cell[1]):
                    if (other_x, other_y) in game.cells:
                        neighbor_amount += 1

                    if active and (other_x, other_y) not in game.active_cells:
                        get_cell_condition(game, cells, (other_x, other_y))

        if cell in game.cells:
            if neighbor_amount < 2 or neighbor_amount > 3:
                cells["dying"].append(cell)

        elif neighbor_amount == 3:
            cells["healing"].append(cell)

def update(game):
    cells = {
        "dying": [],
        "healing": [],
        "seen": set()
    }

    for cell in game.active_cells:
        get_cell_condition(game, cells, cell, True)
    game.active_cells.clear()

    for cell in cells["dying"]:
        game.cells.remove(cell)
        game.active_cells.add(cell)

    for cell in cells["healing"]:
        game.cells.add(cell)
        game.active_cells.add(cell)
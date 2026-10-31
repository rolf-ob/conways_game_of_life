from entities.cell import Cell
from constants import CELL_SIZE

def get_cell_condition(game, cells, x, y, active=False):
    if (x, y) not in cells["seen"]:
        cells["seen"].add((x, y))

        neighbor_amount = 0
        for other_x in range(x - CELL_SIZE, x + CELL_SIZE*2, CELL_SIZE):
            for other_y in range(y - CELL_SIZE, y + CELL_SIZE*2, CELL_SIZE):
                if not (other_x == x and other_y == y):
                    if other_x in game.cells and other_y in game.cells[other_x]:
                        neighbor_amount += 1

                    if active and (other_x, other_y) not in game.active_cells:
                        get_cell_condition(game, cells, other_x, other_y)

        if x in game.cells and y in game.cells[x]:
            if neighbor_amount < 2 or neighbor_amount > 3:
                cells["dying"].append((x, y))

        elif neighbor_amount == 3:
            cells["healing"].append((x, y))

def update(game):
    cells = {
        "dying": [],
        "healing": [],
        "seen": set()
    }

    for axis in game.active_cells:
        get_cell_condition(game, cells, axis[0], axis[1], True)

    game.active_cells = set()

    for axis in cells["dying"]:
        del game.cells[axis[0]][axis[1]]
        if not game.cells[axis[0]]:
            del game.cells[axis[0]]
        
        game.active_cells.add(axis)
    
    for axis in cells["healing"]:
        game.cells[axis[0]][axis[1]] = Cell(axis[0], axis[1])
        game.active_cells.add(axis)
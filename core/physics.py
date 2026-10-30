from entities.cell import Cell
from constants import CELL_SIZE

def get_cell_condition(game, cell):
    dying = []
    healing = []

    neighbor_amount = 0
    for x in range(cell.x - CELL_SIZE, cell.x + CELL_SIZE*2, CELL_SIZE):
        for y in range(cell.y - CELL_SIZE, cell.y + CELL_SIZE*2, CELL_SIZE):
            if not (x == cell.x and y == cell.y):
                if x in game.cells and y in game.cells[x]:
                    neighbor_amount += 1

                else:
                    dead_neighbor_amount = 0
                    for dead_x in range(x - CELL_SIZE, x + CELL_SIZE*2, CELL_SIZE):
                        for dead_y in range(y - CELL_SIZE, y + CELL_SIZE*2, CELL_SIZE):
                            if not (dead_x == x and dead_y == y) and dead_x in game.cells and dead_y in game.cells[dead_x]:
                                    dead_neighbor_amount += 1

                    if dead_neighbor_amount == 3:
                        healing.append((x, y))

    if neighbor_amount < 2 or neighbor_amount > 3:
        dying.append((cell.x, cell.y))
    
    return {"dying": dying, "healing": healing}

def update(game):
    dying_cells = []
    healing_cells = []

    for column in game.cells.values():
        for cell in column.values():
            condition = get_cell_condition(game, cell)
            dying_cells.extend(condition["dying"])
            healing_cells.extend(condition["healing"])

    for coordinate in dying_cells:
        del game.cells[coordinate[0]][coordinate[1]]
    for coordinate in healing_cells:
        game.cells[coordinate[0]][coordinate[1]] = Cell(coordinate[0], coordinate[1])
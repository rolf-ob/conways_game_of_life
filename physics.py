from cell import Cell
from constants import CELL_SIZE

def update_cell(cell):
    neighbor_amount = 0
    grid_x = cell.x // CELL_SIZE #!
    grid_y = cell.y // CELL_SIZE

    for x in range(grid_x-1, grid_x+2):
        for y in range(grid_y-1, grid_y+2):
            if not (x == grid_x and y == grid_y):
                neighbor_amount += 1

    if neighbor_amount < 2 or neighbor_amount > 3:
        return "dying"

def update(game):
    dying_cells = []
    healing_cells = []

    for column in game.cells:
        for cell in column:
            condition = update_cell(game, cell)

            if condition == "dying":
                dying_cells.append(cell)
            elif condition == "healing":
                healing_cells.append(cell)

    for cell in dying_cells:
        game.cells.remove(cell)
    for cell in healing_cells:
        game.cells.append(Cell(cell[0], cell[1])) #!
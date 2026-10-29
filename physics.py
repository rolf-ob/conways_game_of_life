from constants import CELL_SIZE

def update_cell(game, cell):
    neighbor_amount = 0
    grid_x = cell.x // CELL_SIZE
    grid_y = cell.y // CELL_SIZE

    for x in range(grid_x-1, grid_x+2):
        for y in range(grid_y-1, grid_y+2):
            not_self = not (x == grid_x and y == grid_y)
            in_bounds = 0 <= x < len(game.cells) and 0 <= y < len(game.cells[0])

            if not_self and in_bounds and game.cells[x][y].alive:
                neighbor_amount += 1

    if cell.alive:
        if neighbor_amount < 2 or neighbor_amount > 3:
            return "dying"
    
    elif neighbor_amount == 3:
        return "healing"

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
        cell.alive = False
    for cell in healing_cells:
        cell.alive = True
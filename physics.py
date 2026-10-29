from constants import CELL_SIZE

def update_cell(game, cell):
    neighbor_amount = 0
    grid_x = cell.x // CELL_SIZE
    grid_y = cell.y // CELL_SIZE

    for x in range(grid_x-1, grid_x+2):
        for y in range(grid_y-1, grid_y+2):
            not_self = not (x == 0 and y == 0)
            in_bounds = 0 <= x < len(game.cells) and 0 <= y < len(game.cells[0])

            if not_self and in_bounds and game.cells[x][y].alive:
                neighbor_amount += 1

    if cell.alive:
        if neighbor_amount < 2:
            cell.alive = False
        elif neighbor_amount > 3:
            cell.alive = False
    
    elif neighbor_amount == 3:
        cell.alive = True

def update(game):
    for column in game.cells:
        for cell in column:
            update_cell(game, cell)
from entities.cell import Cell
from constants import CELL_SIZE

def move_cells(game, move_x, move_y):
    target_cells = game.selected_cells.copy()
    deselect_cells(game)
    
    for cell in target_cells:
        del game.cells[cell.x][cell.y]
        game.active_cells.add((cell.x, cell.y))

    for cell in target_cells:
        distance = max(1, 100 // game.camera.zoom) ** 2
        x = cell.x + move_x * distance
        y = cell.y + move_y * distance
        new_cell = Cell(x, y, selected=True)
        game.cells[x][y] = new_cell
        game.selected_cells.append(new_cell)
        game.active_cells.add((x, y))

def heal_cells(game, mouse_x, mouse_y):  
    if game.last_click and game.last_click != (mouse_x, mouse_y):
        dx = (mouse_x - game.last_click[0])
        dy = (mouse_y - game.last_click[1])
        step = abs(dx) if abs(dx) >= abs(dy) else abs(dy)
        dx /= step
        dy /= step
        x = game.last_click[0]
        y = game.last_click[1]

        for _ in range(step):
            heal_cell(game, x, y)
            x += dx
            y += dy
    heal_cell(game, mouse_x, mouse_y)

def heal_cell(game, mouse_x, mouse_y):
    grid_x = mouse_x // CELL_SIZE
    grid_y = mouse_y // CELL_SIZE

    if not (grid_x in game.cells and grid_y in game.cells[grid_x]):
        game.cells[grid_x][grid_y] = Cell(grid_x, grid_y)
        game.active_cells.add((grid_x, grid_y))

def select_cell(game, x, y):
    if x in game.cells and y in game.cells[x]:
        cell = game.cells[x][y]

        cell.selected = not cell.selected
        if cell.selected:
            game.selected_cells.append(cell)
        else:
            game.selected_cells.remove(cell)

def deselect_cells(game):
    for cell in game.selected_cells:
        cell.selected = False
    game.selected_cells = []

def kill_cells(game):
    for cell in game.selected_cells.copy():
        del game.cells[cell.x][cell.y]
        game.selected_cells.remove(cell)
        game.active_cells.add((cell.x, cell.y))
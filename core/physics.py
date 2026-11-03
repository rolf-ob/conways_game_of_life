from core.world import heal_cell, kill_cell
from constants import HEALTHY, REBIRTH

def update(game):
    dying = []
    healing = []

    cell_checks = {
        (x+x2, y+y2) for x2 in (-1, 0, 1) for y2 in (-1, 0, 1)
        for (x, y) in game.changed_cells
    }
    game.changed_cells.clear()

    for cell in cell_checks:
        if cell in game.cells and game.neighbour_amounts[cell] not in HEALTHY:
            dying.append(cell)

        elif not cell in game.cells and game.neighbour_amounts[cell] in REBIRTH:
            healing.append(cell)

    for cell in dying:
        kill_cell(game, cell)
    for cell in healing:
        heal_cell(game, cell)
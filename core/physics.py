from core.world import heal_cell, kill_cell
from constants import HEALTHY, REBIRTH

def update(game):
    dying, healing = [], []

    game.cell_checks = {
        (x+x2, y+y2) for x2 in (-1, 0, 1) for y2 in (-1, 0, 1)
        for (x, y) in game.changed_cells
    }
    game.changed_cells.clear()

    for cell in game.cell_checks:
        if cell in game.cells:
            if game.neighbour_amounts.get(cell, 0) not in HEALTHY:
                dying.append(cell)

        elif game.neighbour_amounts.get(cell, 0) in REBIRTH:
            healing.append(cell)

    for cell in dying:
        kill_cell(game, cell)
    for cell in healing:
        heal_cell(game, cell)
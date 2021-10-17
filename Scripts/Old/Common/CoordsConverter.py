from typing import Tuple


def worldToGrid(worldXPos: int, worldYPos: int):
    x = int(worldXPos / CELL_SIZE)
    y = int(worldYPos / CELL_SIZE)
    return (x, y)


def worldToGridT(worldPos: Tuple[int, int]):
    return worldToGrid(worldPos[0], worldPos[1])


def gridToWorld(gridXPos: int, gridYPos: int):
    x = int(gridXPos * CELL_SIZE + CELL_SIZE / 2)
    y = int(gridYPos * CELL_SIZE + CELL_SIZE / 2)
    return (x, y)


def gridToWorldT(gridPos: Tuple[int, int]):
    return gridToWorld(gridPos[0], gridPos[1])

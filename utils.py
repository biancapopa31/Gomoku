import constants as const

# functions for coords

# Normalizeaza coordonatele (coltul stanga sus al tablei este (0,0))
def normalizeCoords(mouse_x, mouse_y):
        return mouse_x - const.ROWS_OFFSET, mouse_y - const.COLS_OFFSET
    
def validateCoords(mouse_x, mouse_y):
    # Validare x
    if(mouse_x <= -const.CELL_SIZE/2):
        return False
    if(mouse_x >= const.ROWS * const.CELL_SIZE - const.CELL_SIZE/2):
        return False
    
    # Validare y
    if(mouse_y <= -const.CELL_SIZE/2):
        return False
    if(mouse_y >= const.COLS * const.CELL_SIZE - const.CELL_SIZE/2):
        return False

    return True

def indexToCoords( i, j):
        return const.ROWS_OFFSET + i * const.CELL_SIZE, const.COLS_OFFSET + j * const.CELL_SIZE


def coordsToIndex(mouse_x, mouse_y):

        mouse_x, mouse_y = normalizeCoords(mouse_x, mouse_y)

        if validateCoords(mouse_x, mouse_y):
            return round((mouse_x + const.CELL_SIZE)/const.CELL_SIZE)-1, round((mouse_y + const.CELL_SIZE)/const.CELL_SIZE)-1
        else:
            return None, None
import random
from items import item
from show import tag_text, Color

def setup_board(
    x_length: int,
    y_length: int,
    snake: list[tuple[int, int]],
    target: tuple[int, int] | None = None,
) -> tuple[list[list[str]], dict[tuple[int, int], str], tuple[int, int]]:
    
    def create_target():
        random_column = random.randint(0, x_length-1)
        random_row = random.randint(0, y_length-1)
        
        return (random_column, random_row)
            
    grid = [ [ "·" for _ in range(x_length) ] for _ in range(y_length)]
    
    for index, (column, row) in enumerate(snake):
        if index == 0:
            grid[row][column] = tag_text(item, Color.GREEN)
        else:
            grid[row][column] = tag_text(item, Color.BLUE)    
    if target:
        grid[target[1]][target[0]] = tag_text("★", Color.GOLD)
    else:
        
        while True:
            target = create_target()
            
            if target not in snake:
                break
        
        grid[target[1]][target[0]] = tag_text("★", Color.GOLD)
        
    table: dict[tuple[int, int], int] = {
        (column_index, row_index): value
            for row_index, row in enumerate(grid)
                for column_index, value in enumerate(row)
    }
    
    return grid, table, target

from typing import TypeAlias, Literal

direction_entity: TypeAlias = Literal["up", "right", "down", "left"]

class Neighbors:
    def __init__(
        self,
        column: int,
        row: int,
        x_length: int,
        y_length: int,
    ):
        
        row_up = row - 1
        row_down = row + 1
        
        column_right = column + 1
        column_left = column - 1
        
        self.upper = (column, row_up if row_up >= 0 else (y_length - 1))
        self.right = (column_right if column_right <= (x_length - 1) else 0, row)
        self.below = (column, row_down if row_down <= (y_length - 1) else 0)
        self.left = (column_left if column_left >= 0 else (x_length - 1), row)
        
        
        self.all = [
            self.upper,
            self.below,
            self.right,
            self.left
        ]

class SnakeController:
    
    def __init__(
        self,
        scale: tuple[int, int],
        snake: list[tuple[int, int]],
        table: dict[tuple[int, int], str],
        target: tuple[int, int],
    ):
        self.scale = scale
        self.snake = snake
        self.table = table
        self.target = target
            
    def find_prv(
        self,
        coordinate: tuple[int, int],
        where: Literal["first", "last"],
    ) -> tuple[int, int] | None:
        
        neighbors = Neighbors(*coordinate, *self.scale)
        
        intersection = [i for i in self.snake if i in neighbors.all]
                    
        if intersection:
            
            if where == "first":
                return intersection[0]
            
            if where == "last":
                return intersection[-1]
        
        return None
    
    def find_direction(self) -> direction_entity:
        head = self.snake[0]
        prv = self.find_prv(head, "last") or head
        
        head_dx, head_dy = head
        prv_dx, prv_dy = prv
        
        column_difference = abs(head_dx - prv_dx)
        row_difference = abs(head_dy - prv_dy)
        
        if row_difference == 1 and head_dy > prv_dy:
            return "down"
        
        if row_difference == 1 and head_dy < prv_dy:
            return "up"
        
        if column_difference == 1 and head_dx > prv_dx:
            return "right"
        
        if column_difference == 1 and head_dx < prv_dx:
            return "left"
        
        return None
        
    
    def move(
        self,
        direction: direction_entity,
    ) -> tuple[list[tuple[int, int]], tuple[int, int]]:
        
        head = self.snake[0]
        next_cell = head
        
        neighbors = Neighbors(*head, *self.scale)
        
        target = self.target

        if direction == "up":
            next_cell = neighbors.upper
            
        elif direction == "right":
            next_cell = neighbors.right
        
        elif direction == "down":
            next_cell = neighbors.below
        
        elif direction == "left":
            next_cell = neighbors.left
            
        if next_cell == self.find_prv(head, "first"):
            return self.snake, target    
        
        if next_cell in self.snake:
            return None, None
                
        if next_cell == self.target:
            
            last = self.snake[-1]
            
            prv = self.find_prv(last, "last") or last
            
            last_dx, last_dy = last
            prv_dx, prv_dy = prv
                        
            column_difference = abs(last_dx - prv_dx)
            row_difference = abs(last_dy - prv_dy)
            
            # direction vectors
            dirs = {
                "up":     (-1, 0),
                "right":  (0, 1),
                "down": (1, 0),
                "left":   (0, -1),
            }

            if column_difference == 1 and row_difference == 0:  # horizontal bend
                direction = "left" if last_dx < prv_dx else "right"

            elif column_difference == 0 and row_difference == 1:  # vertical bend
                direction = "up" if last_dy < prv_dy else "down"

            dx, dy = dirs[direction]
            new_cell = (last[0] + dx, last[1] + dy)

                    
            self.snake.append(new_cell)
            target = None
        
        for i in range(len(self.snake)):
            self.snake[i], next_cell = next_cell, self.snake[i]
                        
        return self.snake, target
    
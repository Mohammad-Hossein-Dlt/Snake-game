import random
from multiprocessing import Process, Queue
import queue
from board import setup_board
from get_input import get_direction
from show import Color, show
from snake import SnakeController, direction_entity
from tprint import clear_output, print_output

speed: float = 0.5
scale: tuple[int, int] = (20, 10)

if __name__ == '__main__':
    
    snake_pattern: list[tuple[int, int]] = [
        (
            random.randint(0, scale[0] - 1),
            random.randint(0, scale[1] - 1),
        ),
    ]

    target: tuple[int, int] = None
    
    grid, table, target = setup_board(*scale, snake_pattern, target)
    
    queue_data = Queue()
    
    get_key_process = Process(target=get_direction, args=(queue_data,), daemon=True)
    get_key_process.start()
    
    direction: direction_entity = "right"
    
    # print(show(grid, "Game closed", Color.TURQUOISE))
                            
    while True:
        
        snake = SnakeController(scale, snake_pattern, table, target)
        
        snake_pattern, target = snake.move(direction)
                
        if snake_pattern == None:
            content = show(grid, "You lose", Color.RED)
            print_output(content)
            queue_data.close()
            get_key_process.terminate()
            get_key_process.join()
            break
        
        grid, table, target = setup_board(*scale, snake_pattern, target)
        
        content = show(grid, f"Score: {len(snake_pattern) - 1}", Color.GREEN)
        
        print_output(content)
        clear_output(content)
        
        try:
            direction = queue_data.get(timeout=speed)
        except queue.Empty:
            pass
        
        if not direction:
            content = show(grid, "Game closed", Color.TURQUOISE)
            print_output(content)
            queue_data.close()
            get_key_process.terminate()
            get_key_process.join()
            break
                    
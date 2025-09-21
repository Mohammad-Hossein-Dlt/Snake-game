from multiprocessing import Queue
import readchar
from snake import direction_entity

def get_direction(
    data: Queue,
):

    while True:
        
        try:
            key = readchar.readkey()
        except KeyboardInterrupt:
            data.put(None)
            break

        new_direction: direction_entity = "right"
        
        if key == readchar.key.UP:
            new_direction = "up"
        elif key == readchar.key.RIGHT:
            new_direction = "right"
        elif key == readchar.key.DOWN:
            new_direction = "down"
        elif key == readchar.key.LEFT:
            new_direction = "left"
                
        data.put(new_direction)

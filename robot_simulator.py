from enum import Enum

class Direction(Enum):
    WEST = "WEST"
    EAST = "EAST"
    NORTH = "NORTH"
    SOUTH = "SOUTH"

class Command(Enum):
    PLACE = "PLACE"
    MOVE = "MOVE"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    REPORT = "REPORT"

#NÄMN ATT PYTHON TILLÅTER ÄNDRING AV VARIABLER OM JAG EJ ANVÄNDER BIBLOTEK SOM attrs

TABLE_BOUNDS_X = (0,5)
TABLE_BOUNDS_Y = (0,5)

MOVE_DIRECTIONS = {
    Direction.NORTH: (0, 1),
    Direction.SOUTH: (0, -1),
    Direction.EAST: (1, 0),
    Direction.WEST: (-1, 0)
}

MOVE_MAP = {
    Command.LEFT: {
        Direction.NORTH: Direction.WEST,
        Direction.WEST: Direction.SOUTH,
        Direction.SOUTH: Direction.EAST,
        Direction.EAST: Direction.NORTH
    },
    Command.RIGHT: {
        Direction.NORTH: Direction.EAST,
        Direction.WEST:  Direction.NORTH,
        Direction.SOUTH: Direction.WEST,
        Direction.EAST:  Direction.SOUTH
    }
}

def within_bounds(x,y):
    within_x_bound = TABLE_BOUNDS_X[0] <= x <= TABLE_BOUNDS_X[1]
    within_y_bound = TABLE_BOUNDS_Y[0] <= y <= TABLE_BOUNDS_Y[1]
    if within_x_bound and within_y_bound:
        return True
    else:
        return False

def place(x,y,f):
    try:
        x = int(x)
        y = int(y)
        valid_direction = any(f == direction.value for direction in Direction)
        if within_bounds(x,y) and valid_direction:
            return x,y,Direction(f),True
        else: 
            print("placement out of range or non excisitng direction")
            return None,None,None,False
    except ValueError:
        print("Invalid form. EX PLACE,1,2,EAST ")
        return None,None,None,False
      
def move(x, y, f):
    if f not in MOVE_DIRECTIONS:
        print("Invalid direction:", f)
        return x, y
    
    delta_x, delta_y = MOVE_DIRECTIONS[f]
    new_x = x + delta_x
    new_y = y + delta_y
    
    if within_bounds(new_x,new_y):
        return new_x, new_y
    else:
        return x,y

def rotate(f, turn):
    if Command(turn) not in MOVE_MAP:
        print("Invalid command:", turn)
        return f
    return MOVE_MAP[Command(turn)][f]

def simulation(): 
    placed = False 
    exit_simulation = False
    while not exit_simulation:
        commands_list = input("input command:").split(',') 
        if Command.PLACE.value not in commands_list and not placed:
            print("Robot must be placed on table")
        else:
            while len(commands_list) != 0:
                command = commands_list.pop(0)
                if not placed:
                    if command == Command.PLACE.value:
                        if len(commands_list) >= 3:
                            input_x = commands_list.pop(0)
                            input_y = commands_list.pop(0)
                            input_f = commands_list.pop(0)
                            x,y,f,valid_place = place(input_x,input_y,input_f)
                            if valid_place:
                                placed = True
                    else: 
                        continue
                elif placed:
                    if command == Command.MOVE.value:
                        x,y = move(x,y,f)
                    elif command in [Command.LEFT.value, Command.RIGHT.value]:
                        f = rotate(f, command)
                    elif command == Command.REPORT.value:
                        print(f"{x},{y},{f.value}")
                        if __name__ != '__main__':
                            exit_simulation = True
                            break
                    elif command == Command.PLACE.value:
                        if len(commands_list) >= 3:
                            input_x = commands_list.pop(0)
                            input_y = commands_list.pop(0)
                            input_f = commands_list.pop(0)
                            new_x,new_y,new_f,valid_place = place(input_x,input_y,input_f)
                            if valid_place:
                                x = new_x
                                y = new_y
                                f = new_f
                        else: 
                            print("Invalid place command,EX PLACE,0,0,NORTH")

def main():
    print("Welcome to the Robot Simulator!")
    print("Place the robot on the table and roam around")
    simulation()

if __name__ == '__main__':
    main()

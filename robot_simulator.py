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

def place(state, commands_list):
    if len(commands_list) < 3:
        print("PLACE needs three agruments E.g. PLACE,1,2,EAST ")
        return state                        
    try:
        input_x = int(commands_list.pop(0))
        input_y = int(commands_list.pop(0))
        input_f = commands_list.pop(0)

        valid_direction = any(input_f == direction.value for direction in Direction)
        if within_bounds(input_x,input_y) and valid_direction:
            state= {"x":input_x,
            "y":input_y,
            "f": Direction(input_f),
            "placed": True}
            return state
        else: 
            print("Placement out of range or non excisitng direction")
            return state
    except ValueError:
        print("Invalid form. E.g. PLACE,1,2,EAST ")
        return state
      
def move(state):
    x = state["x"]
    y = state["y"]
    f = state["f"]
    if f not in MOVE_DIRECTIONS:
        print("Invalid direction:", f)
        return state
    
    delta_x, delta_y = MOVE_DIRECTIONS[f]
    new_x = x + delta_x
    new_y = y + delta_y
    
    if within_bounds(new_x,new_y):
        state["x"] = new_x
        state["y"] = new_y
        return state
    else:
        return state

def rotate(state, turn):
    f = state["f"]
    if Command(turn) not in MOVE_MAP:
        print("Invalid command:", turn)
        return state
    state["f"] = MOVE_MAP[Command(turn)][f]
    return state

def simulation(): 
    exit_simulation = False
    state = {
        "x":None,
        "y":None,
        "f": None,
        "placed": False
    }

    while not exit_simulation:
        commands_list = input("input command:").split(',') 
        if Command.PLACE.value not in commands_list and not state["placed"]:
            print("Robot must first be placed on table")
        else:
            while len(commands_list) != 0:
                command = commands_list.pop(0)
                if command == Command.PLACE.value:
                    state = place(state, commands_list)
                elif not state["placed"]:
                    continue
                elif command == Command.MOVE.value:
                    state = move(state)
                elif command in [Command.LEFT.value, Command.RIGHT.value]:
                    state = rotate(state, command)
                elif command == Command.REPORT.value:
                    print(f'{state["x"]},{state["y"]},{state["f"].value}')
                    if __name__ != '__main__':
                        exit_simulation = True
                        break

def main():
    print("Welcome to the Robot Simulator!")
    print("Place the robot on the table and roam around")
    simulation()

if __name__ == '__main__':
    main()

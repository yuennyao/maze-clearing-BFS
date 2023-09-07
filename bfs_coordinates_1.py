# Generate room connections according to “even-q” vertical layout shoves even columns down (Offset coordinates)
def generate_room_connections(grid_size):
    room_connections = {}

    for x in range(grid_size[0]):
        for y in range(grid_size[1]):
            current_room = (x, y)
            neighbors = get_neighbors(x, y, grid_size)
            room_connections[current_room] = sorted(neighbors)

    return room_connections

# Generate neighbours for a room according to “even-q” vertical layout 
# which shoves even columns down based on an approach of Offset coordinates.
def get_neighbors(x, y, grid_size):
    # When a room is loacted in an odd column
    if x % 2 == 1: 
        neighbors = [
            (x-1, y-1),
            (x-1, y),
            (x, y+1),
            (x+1, y),
            (x+1, y-1),
            (x, y-1)
        ]
    # When a room is loacted in an even column
    else:  
        neighbors = [
            (x-1, y),
            (x-1, y+1),
            (x, y+1),
            (x+1, y+1),
            (x+1, y),
            (x, y-1)
        ]

    valid_neighbors = []
    for neighbor in neighbors:
        nx, ny = neighbor
        if 0 <= nx < grid_size[0] and 0 <= ny < grid_size[1]:
            valid_neighbors.append(neighbor)

    return valid_neighbors

# Define the available actions for Ronny to move between rooms
if __name__ == '__main__':
    grid_size = (9, 6) #cols, rows
    # The function can use to generate rooms connection for different grid size
    room_connections = generate_room_connections(grid_size)

    # (VISUALISATION PURPOSE) Print the state_room dictionary line by line
    # print("Room Connections:")
    # for room, neighbors in room_connections.items():
    #     print(f"'{room}': {neighbors}")

    # Define the initial state
    initial_state = {
        'in': (0, 0),
        'binWeight': (0, 0),
        'roomToClear': 12
    }

    # Define the goal state
    goal_state = {
        'binWeight': (0, 0),
        'roomToClear': 0
    }

    # Define maximum size and weight of the bin
    bin_max_sw = {
        'size': 5,
        'weight': 40
    }

    name = "Ronny"

# Rubbish room format: ((x, y), (size, weight))
rubbish_room = [
        ((0, 5), (1, 10)),  
        ((1, 3), (3, 30)),
        ((2, 2), (1, 5)),
        ((3, 1), (1, 5)),
        ((3, 4), (3, 5)),
        ((4, 2), (2, 10)),
        ((4, 4), (1, 20)),
        ((6, 1), (2, 10)),
        ((6, 4), (2, 5)),
        ((7, 0), (1, 30)),
        ((7, 3), (2, 20)),
        ((8, 1), (3, 10))
    ]

disposal_room = [(2, 5), (5, 0), (8, 5)]

# Generate state of each room (size, weight)
state_room = {}
for x in range(grid_size[0]):
    for y in range(grid_size[1]):
        coordinate = (x, y)
        size_weight = next((sw for coord, sw in rubbish_room if coord == coordinate), (0, 0))
        state_room[coordinate] = size_weight

# (VISUALISATION PURPOSE) Print the state_room dictionary
# for coordinate, (size, weight) in state_room.items():
#     print(f"{coordinate}: (Size: {size}, Weight: {weight})")

# -------------------------------------------------------------------------------------------------------------------------------------------
class Node:
  def __init__(self, state=None, parent=None):
    self.state = state
    self.parent = parent
    self.children = []
    
  def __str__(self):
    return self.state

  def addChildren(self, children):
    self.children.extend(children)

def expandAndReturnChildren(room_connections, node):
    children = []
    # Access the state attribute of the node object
    state = node.state
    # Check if the state exists in room_connections dictionary
    if state in room_connections:
        # Add all neighboring rooms to the children list
        for room in room_connections[state]:
           # Create a child node with the neighboring room and the current state as the parent
           child = Node(room, node)
           children.append(child)
  
    return children
  
def bfs(room_connections, initial_state, goal_state):
    global init_size, init_weight
    frontier = []
    explored = []
    solution = []
    cleared_rubbish = False
 
    frontier.append(Node(initial_state['in'], None))
    
    children = []
    x = 0 # To keep track of the index of the current node in the frontier
    saved_room = "room"
    init_size = initial_state['binWeight'][0]
    init_weight = initial_state['binWeight'][1]
    init_rooms = initial_state['roomToClear']

    while not cleared_rubbish:
        # If x is within or equivalent to the number of values in frontier.
        if x <= (len(frontier)-1):
            # Update the current node with the current value in the frontier with x index.
            current_node = frontier.pop(x)
            
            # To display the room that is being checked.
            print("-> Currently exploring {}... ".format(current_node.state))
            
            #List of the child node in state form (Display coordinate of a room instead of <__main__.Node object at 0x000002421791FD00>)
            child_node_roomname = []
            for child_node in children:
                child_node_roomname.append(child_node.state)
            
            # Sort the children list in ascending order.
            child_node_roomname.sort()
            
            # Check if it is a neighbor of the previous node 
            # If it passes the condition, then the room's size and weight will be added to the bin's total size and weight.
            if (current_node.state in child_node_roomname or not children): 
                # Check if the contents in the room will overload the bin.
                if ((init_size + state_room[current_node.state][0]) <= bin_max_sw["size"]) and ((init_weight + state_room[current_node.state][1]) <= bin_max_sw["weight"]):
                    # Display the current room
                    print("{} has entered {}.".format(name, current_node.state))

                    # To avoid the same room to be added into the solution list twice in a row. 
                    # Mainly for preventing this after restarting - clearing the explored and frontier
                    if current_node != saved_room:
                        solution.append(current_node.state)

                    # Update saved room
                    # To keep track of the last successfully entered room in case there is a need for clearing the frontier and explored list.
                    saved_room = current_node

                    # Add the size and weight of the rubbish in the room into to the bin regardless of whether there is rubbish or not.
                    # Does not matter if it's in an empty room as it will contain size of 0 and weight of 0.
                    init_size += state_room[current_node.state][0]
                    init_weight += state_room[current_node.state][1]

                    # If the room contains rubbish, room to clear will decrease by 1.
                    if current_node.state in [room[0] for room in rubbish_room]:
                        init_rooms = init_rooms - 1
                        print("Rubbish loaded. Current bin has size of {} and weight of {}.".format(init_size, init_weight))
                        print("Room to clear: {} room(s)".format(init_rooms))
                        print("")

                        # Update the current status of the room after clearing the rubbish
                        state_room[current_node.state] = (0,0)

                        # Remove the current room from the rubbish room list.
                        rubbish_room.remove(next(room for room in rubbish_room if room[0] == current_node.state))
                    else:
                        print("Current bin has size of {} and weight of {}.".format(init_size, init_weight))
                        print("Room to clear: {} room(s)".format(init_rooms))
                        print("")
                
                    # Check if current room is a disposal room
                    if current_node.state in disposal_room:
                        # Check if the bin consists of rubbish
                        if init_size > 0 and init_weight > 0:
                            # Empty the bin
                            init_size = 0
                            init_weight = 0
                            print("{} is in the disposal room. The bin is emptied.".format(name))
                            print("Bin has size of {} and weight of {}.".format(init_size, init_weight))
                            
                            # Reset the frontier and explored so that the explored rooms can be revisited again.
                            frontier = []
                            explored = []
                            print("Restarting path...")
                        
                        # Check if no. of rooms to clear is equivalent to no. of rooms to clear in the goal state.
                        if init_rooms == goal_state['roomToClear']:
                            cleared_rubbish = True
                            print("\n{} has cleared all the rooms' rubbish.".format(name))
                            break
                        
                        
                    children = []
                    # Expand the current room.
                    children = expandAndReturnChildren(room_connections, current_node)
                    
                    for child in children:
                    # Check if a node was expanded or in frontier.
                        if not (child.state in [e.state for e in explored]) and not (child.state in [f.state for f in frontier]):
                            frontier.append(child) 
        
                    # Add the current room into the explored list.
                    explored.append(current_node)
                    
                    # Add children list to the current node.
                    current_node.addChildren(children)     
                            
                    print("Frontier: ", [f.state for f in frontier])
                    print("Children: ", [c.state for c in children])
                    print("Explored: ", [e.state for e in explored])
                    print("")
                        
                    # Since this room is expanded successfully, any skipped rooms will be checked again by resetting 'x'.
                    x = 0 

                # If entering room will overload the bin.
                else: 
                    print("Room skipped. Rubbish in room will overload the bin.")
                    print("")

                    # Add back the current node to its initial index in the frontier at same position
                    frontier.insert(x, current_node) 
                    
                    # Jump to the next room first
                    x = x + 1

            # If the room is not a neighbor of the current room Ronny is in.
            else:         
                print("Room skipped. Room is not a neighbor of {}.".format(saved_room.state))
                print("")

                # Add back the current node to its initial index in the frontier
                frontier.insert(x, current_node) # added
                
                # Jump to the next room first
                x = x + 1 

        # If all rooms in the frontier cannot be entered due to "not a neighbor" issue, or entering a room where all its neighbouring rooms have been explored or will overload the rubbish bin,  
        # restart the path with the last successfully entered room as the first room.       
        else: # x = (len(frontier)-1)
            # Reset the frontier, explored, and children list
            frontier = []
            explored = []
            children = []
            
            # Add the last successfully entered room (the room Ronny is in) to the empty frontier.
            frontier.append(saved_room)

            # Reset x
            x = 0

            print("No room can be entered. Restarting path...")
            print("Frontier: ", [f.state for f in frontier])
            print("Explored: ", [e.state for e in explored])
            print("")
                  
    return solution

# Obtain and display the solution
solution = bfs(room_connections, initial_state, goal_state)
print("\nSolution: ", solution)
print("\nNo. of rooms entered: ", len(solution))
path_cost = len(solution) * 10
print("\nPath cost: ", path_cost, "meter\n")

print(" ")

#VISUALISATION PURPOSE (Match coordinates with room names)
for row in range(grid_size[0]):
    for col in range(grid_size[1]):
        room_number = row * grid_size[1] + col + 1
        coordinate = (row, col)
        room_name = f"Room{room_number}"
        room_connections[coordinate] = room_name

matched_rooms = []
for coordinate in solution:
    room_name = room_connections.get(coordinate)
    matched_rooms.append(room_name)
print("To match coordinates with room number (visualise only)")
print(matched_rooms)
from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# For O(1) time complexity for append and pop operations
from collections import deque

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions

# Player path
traversal_path = []

# Inverse player path
steps_to_start = []
visited = {}

# Set up inverse relationship with directions
inverse_directions = { "n": "s", "e": "w", "w": "e", "s": "n" }

def setup_room():
    exits = player.current_room.get_exits()
    visited[player.current_room.id] = deque()
    for exit in exits:
        visited[player.current_room.id].append(exit)

def step_forward():
    # Get the first available direction
    direction = visited[player.current_room.id].popleft()

    # Travel there
    player.travel(direction)

    # Add the inverse direction so we can retrace our path
    steps_to_start.append(inverse_directions[direction])

    if player.current_room.id not in visited:
        # Add current room to visited
        setup_room()
        # Remove the inverse direction since we don't need to go back
        visited[player.current_room.id].remove(inverse_directions[direction])

    # Add the direction we traveled to traversal_path
    traversal_path.append(direction)

def step_back():
    # Go back one room and check again
    direction = steps_to_start.pop()
    traversal_path.append(direction)
    player.travel(direction)

setup_room()
while len(visited) < 500:
    if len(visited[player.current_room.id]) > 0:
        step_forward()
    else:
        step_back()

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")

    print(f"PATH: {traversal_path}")
    print(f"VISITED: {visited}")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######

player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")

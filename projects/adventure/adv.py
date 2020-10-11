from room import Room
from player import Player
from world import World
import sys
sys.path.append('../graph/')
from util import Stack, Queue

import random
from ast import literal_eval

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


# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# directions
directions = {}
opposite_lookup = {'n': 's', 's': 'n', 'w': 'e', 'e': 'w'}

# update rooms in map
def update_map(room, next_room):
    if next_room is not None:
        for i in range(len(room.get_exits())):
            for j in range(len(next_room.get_exits())):
                if next_room.id not in directions:
                    directions[next_room.id] = {next_room.get_exits()[j]: '?' for j in range(len(next_room.get_exits()))}
                if room.get_room_in_direction(room.get_exits()[i]) == next_room:
                    directions[room.id].update({room.get_exits()[i]: next_room.id})
                    directions[next_room.id].update({opposite_lookup.get(room.get_exits()[i]): room.id})
    else:
        directions[room.id] = {room.get_exits()[i]: '?' for i in range(len(room.get_exits()))}

# update player starting room
update_map(world.starting_room, next_room=None)

while len(directions) < len(room_graph):
    #traverse unexplored exits
    if '?' in directions[player.current_room.id].values():
        unexplored_exits = []
        exits = player.current_room.get_exits()
        for e in player.current_room.get_exits():
            if directions[player.current_room.id].get(e) == '?':
                unexplored_exits.append(e)
        rand_exit_no = random.randrange(len(unexplored_exits))
        player_exit = unexplored_exits[rand_exit_no]
        update_map(player.current_room, player.current_room.get_room_in_direction(player_exit))
        traversal_path.append(player_exit)
        player.travel(player_exit)

    # search for new unexplored exit
    if '?' not in directions[player.current_room.id].values():
        path = []
        while '?' not in directions[player.current_room.id].values() and len(directions) < len(room_graph):
            counter = 0
            exits = [e for e in player.current_room.get_exits()]
            if len(path) > 0 and len(exits) > 1:
                exits.remove(opposite_lookup[path[-1]])

            rand_exit_no = random.randrange(len(exits))
            player_exit = exits[rand_exit_no]
            path.append(player_exit)
            player.travel(player_exit)
            counter += 1
            if '?' in directions[player.current_room.id].values():
                for p in path:
                    traversal_path.append(p)
                counter = 0
                path = []
            if len(path) > 20:
                path = path[::-1]
                for p in path:
                    player.travel(opposite_lookup[p])
                counter = 0
                path = []

    print(f"{round(len(directions)/len(room_graph)*100, 2)}% complete")

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
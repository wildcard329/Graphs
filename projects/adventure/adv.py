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
map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

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

def search_exits(room):
    q = Queue()
    seen = set()
    seen.add(room.id)
    for e in directions[room.id]:
        q.enqueue([e])
        print('direction: ',e)
        print('room', room.get_room_in_direction(e).id)
        
    while q.size() > 0:
        p = q.dequeue()
        v = p[-1]

        if v in room.get_exits() and room.get_room_in_direction(v).id in directions:
            room = room.get_room_in_direction(v)

        if room.id not in seen:
            seen.add(room.id)
            if '?' in directions[room.id]:
                print('p: ',p)
                input()
                return p

            exits = room.get_exits()
            for e in exits:
                if room.get_room_in_direction(e).id not in directions:
                    print('p: ',p)
                    return p
                    # for d in p:
                    #     player.travel(d)
                    # while q.size() > 0:
                    #     q.dequeue()
                    #     break

                if room.get_room_in_direction(e).id not in seen:

                    q.enqueue(p + [e])
                if '?' in directions[room.get_room_in_direction(e).id].values():
                    path = p + [e]
                    print('p: ',path)
                    return path
                    # traversal_path.extend(path)
                    # for d in path:
                    #     player.travel(d)
                    # while q.size() > 0:
                    #     q.dequeue()

# def search_for_unexplored(room):
#     q = Queue()
#     seen = set()
#     print(directions[room.id])
#     for e in room.get_exits():
#         q.enqueue([e])

#     while q.size() > 0:
#         p = q.dequeue()
#         v = p[-1]

#         if room.get_room_in_direction(v) not in seen:
#             if room.get_room_in_direction(v) is not None:
#                 seen.add(room.get_room_in_direction(v))
#                 room = room.get_room_in_direction(v)

#             for e in room.get_exits():
#                 q.enqueue(p + [e])

#             if check_room_for_exits(room) is True:
#                 # print('path: ',p)
#                 return p

def find_new_exit(room):
    q = Queue()
    seen = set()
    for e in room.get_exits():
        q.enqueue([e])

    while q.size() > 0:
        p = q.dequeue()
        v = p[-1]

        if directions[room.id][v] not in seen:
            seen.add(directions[room.id][v])
            input(directions[room.id][v])
            room = directions[room.id][v]

            for d in directions[room].get(d):
                if directions[room][d] not in seen:
                    q.enqueue(p + [d])

                if directions[room.id][v] == '?':
                    return p


while len(directions) < len(room_graph):
    # print(directions)
    # input()
    if '?' in directions[player.current_room.id].values():
        unexplored_exits = []
        exits = player.current_room.get_exits()
        for e in player.current_room.get_exits():
            if directions[player.current_room.id].get(e) == '?':
                unexplored_exits.append(e)
        print(f"unexplored: {unexplored_exits}")
        rand_exit_no = random.randrange(len(unexplored_exits))
        player_exit = unexplored_exits[rand_exit_no]
        print(f"room: {player.current_room.id}, exits: {unexplored_exits}, exit: {player_exit}")
        update_map(player.current_room, player.current_room.get_room_in_direction(player_exit))
        traversal_path.append(player_exit)
        player.travel(player_exit)
        input('traversal')

    def check_room_for_exits(room):
        if '?' in directions[room.id].values():
            return True
        return False
        
    if check_room_for_exits(player.current_room) is False:
        # explored_exits = []
        # for e in player.current_room.get_exits():
        #     explored_exits.append(e)
        # rand_exit_no2 = random.randrange(len(explored_exits))
        # p_exit = explored_exits[rand_exit_no2]
        # print(f"Room: {player.current_room.id}, Exits: {player.current_room.get_exits()}, Exit: {p_exit}")
        # traversal_path.append(p_exit)
        # player.travel(p_exit)
        input('search')
        marker = player.current_room
        input(marker.id)
        print(search_exits(marker))
        for direction in search_exits(marker):
            traversal_path.append(direction)
            player.travel(direction)

        # input('search')
        # marker = player.current_room
        # print(f"Marker: {marker}")
        # for direction in find_new_exit(marker):
        #     traversal_path.append(direction)
        #     player.travel(direction)
        # q = Queue()
        # seen = set()
        # exits = marker.get_exits()

        # for e in exits:
        #     input(e)
        #     q.enqueue([e])

        # while check_room_for_exits(marker) is False and q.size() > 0:
        #     p = q.dequeue()
        #     v = p[-1]
        #     print('unexplored is false')

        #     if marker.get_room_in_direction(v) not in seen and marker.get_room_in_direction(v) is not None:
        #         seen.add(marker.get_room_in_direction(v))
        #         marker = marker.get_room_in_direction(v)

        #         for e in marker.get_exits():
        #             if marker.get_room_in_direction(e) not in seen:
        #                 q.enqueue(p + [e])

        #             if check_room_for_exits(marker) is True:
        #                 print('check')
        #                 print('p: ',p)
        #                 print('path: ',traversal_path)
        #                 print('mcr: ',marker.id)
        #                 print('pcr: ',player.current_room.id)
        #                 input()
        #                 for direction in p:
        #                     traversal_path.append(direction)
        #                     player.travel(direction)
        #                 break

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
import random
import sys
sys.path.append('../graph/')
from util import Stack, Queue

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME

        # Add users
        for user in range(num_users):
            self.add_user(user)

        # Create friendships
        max_friendships = num_users * avg_friendships
        assignments = []
        friendpool = [user for user in self.users]

        while max_friendships != 0:
            num_friends = random.randrange(avg_friendships * 2 - 1)
            assignments.append(num_friends)
            max_friendships -= num_friends
            if max_friendships < 0:
                max_friendships = num_users * avg_friendships
                assignments = []
            if len(assignments) == num_users:
                while max_friendships > 0:
                    for num in range(len(assignments)):
                        assigned = random.randrange(2)
                        if assigned == 1:
                            assignments[num] += 1
                            max_friendships -= 1

        # print(assignments)
        # print(len(assignments))
        print(friendpool)
        print(friendpool)
        # print(fp_copy)
        for user in self.users:
            fp_copy = friendpool
            random.shuffle(fp_copy)

            counter = assignments[-1]
            # fp_copy.remove(user)

            while counter > 0 and len(fp_copy) > 0:
                self.add_friendship(user, fp_copy[-1])
                fp_copy.pop()
                counter -= 1

            assignments.pop()
            fp_copy = friendpool

            #     self.add_friendship(user, )
                
            # print(f"user: {user}, friendships: {user_num_friendships}")

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        # !!!! IMPLEMENT ME
        q = Queue()

        q.enqueue([user_id])

        while q.size() > 0:
            p = q.dequeue()
            v = p[-1]

            if v not in visited:
                visited[v] = p

                for f in self.friendships[v]:
                    if f not in visited:
                        q.enqueue(p + [f])

        # print(self.friendships[user_id])
        # for friends in self.friendships:
        #     print(friends)
        # for result in self.users:
        #     print(self.result.friendships)
        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)

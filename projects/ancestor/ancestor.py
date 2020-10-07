import sys
sys.path.append('../graph/')
from util import Stack, Queue


def earliest_ancestor(ancestors, starting_node):
    # print(ancestors, starting_node)
    chart = {}

    q = Queue()

    paths = set()
    for pair in ancestors:
        chart[pair[1]] = set()

    for pair in ancestors:
        chart[pair[1]].add(pair[0])

    q.enqueue([starting_node])

    while q.size() > 0:
        p = q.dequeue()
        v = p[-1] 

        if chart.get(v) is None:
            if q.size() == 0:
                if v == starting_node:
                    return -1
                print(p)
                return v
            continue

        for node in chart.get(v):
            if node is not None:
                q.enqueue(p + [node])
    
    print(paths)

test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]
earliest_ancestor(test_ancestors, 6)
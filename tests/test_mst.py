import os
import sys
from math import sqrt
from random import random, randint
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')
from generate.base import line, setup, lpath
from generate.minimum_spanning_tree import MST, Node, Room

def ignore_test_mst_double():
    a, b = Node(1, x=10, y=10), Node(2, x=20, y=20)
    mst = MST()
    mst.add(a)
    mst.add(b)
    assert len(mst.nodes) == 2

# if __name__ == "__main__":
def ignore_test_mst_nodes():
    width, height = 160, 44
    low, high = .05, .95
    setup(width, height, cx=8, cy=16)
    mst = MST()
    points = set()
    for i in range(100):
        x, y = randint(int(width * low), int(width * high)), randint(int(height * low), int(height * high))
        while (x, y) in points:
            x, y = randint(int(width * low), int(width * high)), randint(int(height * low), int(height * high))
        for j in range(-2, 3):
            for k in range(-2, 3):
                points.add((x + k, y + j))
        mst.add(Node(i, x, y))

    mst.calculate_distances()
    # print(mst)
    # for node in mst.nodes:
    #     print(node.vertices())
    # for node in mst.nodes:
    #     print(node.closest())
    mst.find_all_edges()
    # print('E: ', mst.edges)
    mst.find_all_vertices()
    # print('V: ', mst.vertices)
    mst.run()
    # print(mst.mst)
    mst.output_terminal(line=lpath)

if __name__ == "__main__":
    # ignore_test_mst_double()
    ignore_test_mst_nodes()
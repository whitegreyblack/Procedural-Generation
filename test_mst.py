from drunkards import MST, Node, line, setup, lpath
from random import randint
from math import sqrt

def test_mst_double():
    a, b = Node(1, x=10, y=10), Node(2, x=20, y=20)
    mst = MST()
    mst.add(a)
    mst.add(b)
    assert len(mst.nodes) == 2

if __name__ == "__main__":
    width, height = 160, 88
    low, high = .05, .95
    setup(width, height)
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

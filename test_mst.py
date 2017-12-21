from drunkards import MST, Node
from random import randint
from math import sqrt
def test_mst_double():
    a, b = Node(1, 10, 10), Node(2, 20, 20)
    mst = MST()
    mst.add(a)
    mst.add(b)
    assert len(mst.nodes) == 2

if __name__ == "__main__":
    print('MST TESTS')
    mst = MST()
    points = set()
    for i in range(10):
        x, y = randint(0, 80), randint(0, 25)
        while (x, y) in points:
            x, y = randint(0, 80), randint(0, 25)
        mst.add(Node(i, x, y))

    mst.calculate_distances()
    print(mst)
    # for node in mst.nodes:
    #     print(node.vertices())
    # for node in mst.nodes:
    #     print(node.closest())
    mst.find_all_edges()
    print('E: ', mst.edges)
    mst.find_all_vertices()
    print('V: ', mst.vertices)
    mst.run()
    print(mst.mst)
    mst.output_terminal()
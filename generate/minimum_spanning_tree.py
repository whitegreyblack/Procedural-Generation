import math
import random
from bearlibterminal import terminal
from .color import Color
from .base import line

class Node:
    def __init__(self, node_id, x, y):
        self.id = node_id
        self.x, self.y = x, y
        self.neighbors = {}

    def __str__(self):
        return f"Node {self.id}: ({self.x}, {self.y})"

    def __repr__(self):
        return f"Node {self.id}: ({self.x}, {self.y})"

    def distance(self, other):
        return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)

    def closest(self):
        if self.neighbors:
            return min((self.neighbors[k], k) for k in self.neighbors)

    def vertices(self):
        return set((self.neighbors[k], min(self.id, k), max(self.id, k)) for k in self.neighbors)
            
class Room(Node):
    def __init__(self, node_id, x, y, width=8, height=5):
        super().__init__(node_id, x, y)
        self.width, self.height = width, height
        x1, x2, y1, y2 = self.x - width//2, self.x + width//2 + 1, self.y - height//2, self.y + height//2 + 1
        self.x1, self.x2, self.y1, self.y2 = x1, x2, y1, y2
        self.top_left = (x1, y1)
        self.top_right = (x1, y2)
        self.bot_left = (x2, y1)
        self.bot_right = (x2, y2)
        self.color = Color()

    @property
    def points(self):
        points = set()
        for j in range(self.y1, self.y2):
            for i in range(self.x1, self.x2):
                points.add((i, j))
        return points

    @property
    def walls(self):
        points = set()
        # get x axis
        for j in range(self.y1, self.y2):
            points.add((self.x1, j))
            points.add((self.x2 - 1, j))
        # get y axis
        for i in range(self.x1, self.x2):
            points.add((i, self.y1))
            points.add((i, self.y2 - 1))
        return points

    @property
    def floors(self):
        points = set()
        for j in range(self.y1 + 1, self.y2 - 1):
            for i in range(self.x1 + 1, self.x2 - 1):
                points.add((i, j))
        return points

    @property
    def corners(self):
        return {self.top_left, self.top_right, self.bot_left, self.bot_right}

    def random_point(self):
        return random.choice(list(self.points))

    def random_wall_point(self):
        return random.choice(list(self.walls))

    def random_floor_point(self):
        return random.choice(list(self.floors))

class MST():
    '''Takes in list/set of nodes amd returns a minimum spanning tree.'''
    def __init__(self, nodes=None, noise=.8):
        self.nodes = nodes if nodes else []

    def __repr__(self):
        return f"MST: nodes: {len(self.nodes)}\n  " + \
        "\n  ".join([f"{k}, {self.graph[k]}" for k in self.graph])

    def run(self):
        '''The algorithm follows minimum spanning tree however there are
        several conditions that will be checked during the iterations.

        1. If the nodes are too far apart, will not connect
        2. If graph is not completely connected, will return all groups
           in their own set.
        3. If more than one group, leads to multiple continents
        '''
        self.mst = set()
        pq = sorted(self.edges)
        while pq:
            d, a, b = pq.pop(0)
            # if d >= 15:
            #     break
            # print(a, ':', self.vertices[a], ',', b, ':', self.vertices[b])
            if b not in self.vertices[a] and a not in self.vertices[b]:
                # print('adding', b, '->', a, ':', self.vertices[a])
                self.vertices[a].update(self.vertices[b])
                for c in self.vertices[a]:
                    self.vertices[c] = self.vertices[a]
                    # print('UPDATE', c, self.vertices[c])
                # print('adding', a, '->', b, ':', self.vertices[b])
                self.vertices[b].update(self.vertices[a])
                for c in self.vertices[b]:
                    self.vertices[c] = self.vertices[b]
                    # print('UPDATE', c, self.vertices[c])
                # print(a, ':', self.vertices[a], ',', b, ':', self.vertices[b])
                self.mst.add((a, b))
                if len(self.mst) == len(self.nodes) - 1:
                    break

        # more = int(len(pq) * .01)
        more = int(len(self.nodes) * .3)
        for i in range(min(more, len(pq))):
            d, a, b = pq.pop(0)
            self.mst.add((a, b))
            # if len(self.mst) == len(self.nodes) - 1:
            #     break
            # print()

    def calculate_distances(self):
        if not self.nodes:
            raise ValueError('No nodes in graph')
        for i in self.nodes:
            for j in self.nodes:
                if i != j:
                    i.neighbors[j.id] = i.distance(j)

        self.graph = {node: node.neighbors for node in self.nodes}
        # for k in self.graph:
        #     print(k, self.graph[k])

    def node_with_id(self, nid):
        node = None
        for n in self.nodes:
            if n.id == nid:
                node = n
        return node

    def add(self, node):
        self.nodes.append(node)

    def find_all_edges(self):
        self.edges = {v for node in self.nodes for v in node.vertices()}

    def find_all_vertices(self):
        self.vertices = {node.id: {node.id} for node in self.nodes}

    def output_terminal(self, line=line):
        vertices = set()
        for n in self.nodes:
            vertices.add((n.x, n.y))
            terminal.puts(n.x, n.y, f'[c=red]@[/c]')
        for a, b in self.mst:
            na = self.node_with_id(a)
            nb = self.node_with_id(b)
            for (x, y) in line((na.x, na.y), (nb.x, nb.y))[1:-1]:
                if (x, y) not in vertices:
                    terminal.puts(x, y, f'[c=white].[/c]')
        terminal.refresh()
        terminal.read()

    def output_post_processing(self, line=line):
        pass
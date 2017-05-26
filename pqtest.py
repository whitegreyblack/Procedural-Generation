import Queue as queue

def calcDistance(i, j):
    x1, y1 = i
    x2, y2 = j
    return abs(x1-x2) + abs(y1-y2)

def getNeighbors(land, pq, empty):
    tiles = set(i for i in land)
    print(tiles, type(tiles))
    for k in land:
        x, y = k
        for i in range(-1,2):
            for j in range(-1,2):
                print("I:{},J:{}".format(x+i,y+j))
                # check self, check unempty and check if neighbor is already in territory
                if (i,j) != k and (x+i, y+j) not in empty and (x+i,y+j) not in tiles:
                    tiles.add((i,j))
                    pq.put((calcDistance((x+i,y+j),k), i+j, (i,j), k))
    print("Tiles: {}".format(tiles))
pq = queue.PriorityQueue()
empty = set()
empty.add((2,3))
empty.add((0,1))
getNeighbors([(1,1),(1,2)], pq, empty)
while not pq.empty():
    item = pq.get()
    print(item)
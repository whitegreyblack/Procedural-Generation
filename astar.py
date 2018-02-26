import color as c
import random
import Queue as queue

world = [[random.randint(0, 2) for i in range(6)] for j in range(5)]
print(len(world))
print(len(world[0]))
def getneighbors(x):
    xx, xy = x
    neighbors = []
    for i in range(-1,2):
        for j in range(-1,2):
            if 0 <= xx + i < 5 and 0 <= xy + j < 5:
                if (xx + i, xy + j) != x and world[xx + i][xy + j] > 0:
                    neighbors.append((xx + i, xy + j))
    print('N', neighbors)
    return neighbors

def manhattan(x, y):
    xa, xb = x
    ya, yb = y
    return abs(xa - ya) + abs(xb - yb)

def chebyshev(x, y):
    xa, xb = x
    ya, yb = y
    return int(1 * manhattan(x, y) + (2 - 2 * 1) * min(abs(xa - ya), abs(xb - yb)))

def astarsearch(x, y):
    xx, xy = x
    world[xx][xy] = c.BLUE
    frontier = queue.PriorityQueue()
    frontier.put((0, x))
    came_from = {x: None}
    curr_cost = {x: 0}
    totalcost = 0

    while not frontier.empty():
        distance, point = frontier.get()
        print('USING: ', point)

        if point == y:
            totalcost = distance
            a, b = y
            world[a][b] = c.BLUE
            
        neighbors = getneighbors(point)

        for i in neighbors:
            cost = chebyshev(i, x)
            new_cost = curr_cost[x] + cost
            if i not in curr_cost or new_cost < curr_cost[i]:
                curr_cost[i] = new_cost
                frontier.put((new_cost, i))
                came_from[i] = x
    return totalcost

print(chebyshev((0, 0), (2, 1)))
t = astarsearch((0, 0), (2, 1))
print(t)
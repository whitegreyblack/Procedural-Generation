import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')
from generate.minimum_spanning_tree import Room

def test_room_id():
    r = Room(node_id=0, x=5, y=5)
    assert r.id == 0

def test_room_points():
    r = Room(node_id=0, x=5, y=5)
    assert (r.x, r.y) == (5, 5)

def test_room_walls():
    r = Room(node_id=0, x=5, y=5)
    assert (5, 5) not in r.walls
    assert (1, 5) in r.walls

def test_room_floors():
    r = Room(node_id=0, x=5, y=5)
    assert (5, 5) in r.floors

def test_room_random_wall():
    r = Room(node_id=0, x=5, y=5)
    assert r.random_wall_point() in r.walls

def test_room_random_floor():
    r = Room(node_id=0, x=5, y=5)
    assert r.random_floor_point() in r.floors

def test_room_random_point():
    r = Room(node_id=0, x=5, y=5)
    assert r.random_point() in r.points

def test_room_points_match_floors_and_walls():
    r = Room(node_id=0, x=5, y=5)
    assert r.points == r.floors | r.walls

def test_room_floor_wall_nonoverlap():
    r = Room(node_id=0, x=5, y=5)
    assert set() == r.walls & r.floors

def test_room_points_range():
    r = Room(node_id=0, x=5, y=5)
    for x, y in r.points:
        assert -3 <= x <= 13
        assert 0 <= y <= 10

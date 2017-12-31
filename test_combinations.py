import drunkards
import pytest
from functools import reduce

def test_combinations_invalid_combination():
    x, y = (5, 5)
    comb_type = None
    with pytest.raises(ValueError, message="Invalid Combination"):
        drunkards.Combinations.combinations(comb_type)    

def test_combinations_horizontal_inclusive():
    x, y = (5, 5)
    comb_type = drunkards.Combinations.HORIZONTAL
    steps = drunkards.Combinations.combinations(comb_type, inclusive=True)
    assert 0 == sum(reduce(lambda x, y: (x[0] + y[0], x[1] + y[1]), steps))
    assert len(steps) == 3
    assert (0, 0) in steps
    for xx, yy in steps:
        assert x - 1 <= x + xx <= x + 1
        assert y + yy == y

def test_combinations_horizontal_exclusive():
    x, y = (5, 5)
    comb_type = drunkards.Combinations.HORIZONTAL
    steps = drunkards.Combinations.combinations(comb_type, inclusive=False)
    assert 0 == sum(reduce(lambda x, y: (x[0] + y[0], x[1] + y[1]), steps))
    assert len(steps) == 2
    assert (0, 0) not in steps
    for xx, yy in steps:
        assert x - 1 <= x + xx <= x + 1
        assert y + yy == y

def test_combinations_vertical_inclusive():
    x, y = (5, 5)
    comb_type = drunkards.Combinations.VERTICAL
    steps = drunkards.Combinations.combinations(comb_type, inclusive=True)
    assert 0 == sum(reduce(lambda x, y: (x[0] + y[0], x[1] + y[1]), steps))
    assert len(steps) == 3
    assert (0, 0) in steps
    for xx, yy in steps:
        assert x + xx == x
        assert x -1 <= x + xx <= x + 1

def test_combinations_vertical_exclusive():
    x, y = (5, 5)
    comb_type = drunkards.Combinations.VERTICAL
    steps = drunkards.Combinations.combinations(comb_type, inclusive=False)
    assert 0 == sum(reduce(lambda x, y: (x[0] + y[0], x[1] + y[1]), steps))
    assert len(steps) == 2
    assert (0, 1) in steps
    for xx, yy in steps:
        assert x + xx == x
        assert x -1 <= x + xx <= x + 1

def test_combinations_diagonal_exclusive():
    x, y = (5, 5)
    comb_type = drunkards.Combinations.DIAGONAL
    steps = drunkards.Combinations.combinations(comb_type, inclusive=False)
    assert 0 == sum(reduce(lambda x, y: (x[0] + y[0], x[1] + y[1]), steps))
    assert len(steps) == 4
    assert (0, 0) not in steps
    for xx, yy in steps:
        assert x -1 <= x + xx <= x + 1
        assert y -1 <= y + yy <= y + 1

def test_combinations_diagonal_inclusive():
    x, y = (5, 5)
    comb_type = drunkards.Combinations.DIAGONAL
    steps = drunkards.Combinations.combinations(comb_type, inclusive=True)
    assert 0 == sum(reduce(lambda x, y: (x[0] + y[0], x[1] + y[1]), steps))
    assert len(steps) == 5
    assert (0, 0) in steps
    for xx, yy in steps:
        assert x -1 <= x + xx <= x + 1
        assert y -1 <= y + yy <= y + 1

def test_combinations_lateral_exclusive():
    x, y = (5, 5)
    comb_type = drunkards.Combinations.DIAGONAL
    steps = drunkards.Combinations.combinations(comb_type, inclusive=True)
    assert 0 == sum(reduce(lambda x, y: (x[0] + y[0], x[1] + y[1]), steps))
    assert len(steps) == 5
    assert (0, 0) in steps
    for xx, yy in steps:
        assert x -1 <= x + xx <= x + 1
        assert y -1 <= y + yy <= y + 1


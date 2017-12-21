import drunkards
from random import random, randint
from functools import reduce

def test_constructor_single_callable_with_callable_args():
    width = 10
    array = drunkards.constructor(width, value=lambda x: x * 2 - 1, args=random)
    assert len(array) == width
    for val in array:
        assert -1 <= val < 1

def test_constructor_single_callable_with_args():
    width = 10
    low, high = 0, 5
    array = drunkards.constructor(width, value=randint, args=(low, high))
    assert len(array) == width
    for val in array:
        assert low <= val <= high

def test_constructor_single_callable_without_args():
    width = 10
    array = drunkards.constructor(width, value=random)
    assert len(array) == width
    for val in array:
        assert 0 <= val < 1

def test_constructor_single_uncallable_with_args():
    width = 10
    low, high = 0, 5
    array = drunkards.constructor(width, value=3, args=(low, high))
    assert len(array) == width
    for val in array:
        assert val == 3

def test_constructor_single_uncallable_without_args():
    width = 10
    array = drunkards.constructor(width, value=3)
    assert len(array) == width
    for val in array:
        assert val == 3

def test_constructor_double_callable_with_args():
    width, height = 10, 15
    low, high = 0, 5
    array = drunkards.constructor(width, height, value=randint, args=(low, high))
    assert len(array) == height
    assert len(array[0]) == width    
    for row in array:
        for val in row:
            assert low <= val <= high

def test_constructor_double_callable_without_args():
    width, height = 10, 15
    array = drunkards.constructor(width, height, value=random)
    assert len(array) == height
    assert len(array[0]) == width
    for row in array:
        for val in row:
            assert 0 <= val < 1

def test_constructor_double_uncallable_with_args():
    width, height = 10, 15
    low, high = 0, 5
    array = drunkards.constructor(width, height, value=3, args=(low, high))
    assert len(array) == height
    assert len(array[0]) == width    
    for row in array:
        for val in row:
            assert val == 3

def test_constructor_double_uncallable_without_args():
    width, height = 10, 15
    array = drunkards.constructor(width, height, value=3)
    assert len(array) == height
    assert len(array[0]) == width    
    for row in array:
        for val in row:
            assert val == 3

def test_constructor_triple_callable_with_args():
    width, height, depth = 10, 15, 20
    low, high = 0, 5
    array = drunkards.constructor(width, height, depth, value=randint, args=(low, high))
    assert len(array) == depth
    assert len(array[0]) == height
    assert len(array[0][0]) == width
    for col in array:
        for row in col:
            for val in row:
                assert 0 <= val <= high

def test_constructor_double_no_height_callable_with_args():
    width, depth = 10, 20
    low, high = 0, 5
    array = drunkards.constructor(width, depth=depth, value=randint, args=(low, high))
    assert len(array) == depth
    assert len(array[0]) == width
    for row in array:
        for val in row:
            assert 0 <= val <= high

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


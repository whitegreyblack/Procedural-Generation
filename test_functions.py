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
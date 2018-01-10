import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')
from generate.color import Color

def test_color_no_args():
    c = Color()
    assert c.color == "#000000"

def test_color_single_arg():
    c = Color(r=255)
    assert c.color == "#ff0000"

    c = Color(g=255)
    assert c.color == "#00ff00"

    c = Color(b=255)
    assert c.color == "#0000ff"

def test_color_double_args():
    c = Color(r=255, g=255)
    assert c.color == "#ffff00"

    c = Color(r=255, b=255)
    assert c.color == "#ff00ff"

    c = Color(g=255, b=255)
    assert c.color == "#00ffff"

def test_color_triple_args():
    c = Color(r=255, g=255, b=255)
    assert c.color == "#ffffff"

from game_2048.game_2048 import *

def test_merge_1():
    assert merge([2, 2, 0, 4]) == [4, 4, 0, 0]

print(merge([2, 2, 0, 4]) == [4, 4, 0, 0])
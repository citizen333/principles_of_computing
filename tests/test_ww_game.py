import pytest
from poc.word_wrangler import ww_game

@pytest.mark.parametrize("duplicate_list, output", [
    (list(range(10)), list(range(10))),
    (["d", "f", "b", "f", "f", "d", "k"], ["d", "f", "b", "k"])
])
def test_remove_duplicates(duplicate_list, output):
    assert ww_game.remove_duplicates(duplicate_list) == output

@pytest.mark.parametrize("list1, list2, output", [
    (list(range(10, 0, -1)), list(range(5, 15, 2)), [9, 7, 5]),
    (
        ["d", "f", "b", "f", "f", "d", "k"],
        ["w","x", "y", "k", "a", "b", "b", "z"],
        ["b", "k"]
    )
])
def test_intersect(list1, list2, output):
    assert ww_game.intersect(list1, list2) == output

@pytest.mark.parametrize("list1, list2, output",[
    (list(range(1,7)), list(range(3, 15)),
        sorted(list(range(1,7)) + list(range(3, 15)))),
    (list(range(7)), list(range(3, 5)),
        sorted(list(range(7)) + list(range(3, 5)))),
    (list(range(1,4)), list(range(1,4)),
        sorted(list(range(1,4)) + list(range(1,4))))
])
def test_merge(list1, list2, output):
    assert ww_game.merge(list1, list2) == output

@pytest.mark.parametrize("list1, output",[
    (list(range(5, 1, -2)) + list(range(2)) + list(range(1, 8)),
    sorted(list(range(5, 1, -2)) + list(range(2)) + list(range(1, 8))))
])
def test_merge_sort(list1, output):
    assert ww_game.merge_sort(list1) == output

@pytest.mark.parametrize("word, output",[
    ("abc", ['', 'c', 'b', 'bc', 'cb', 'a', 'ac', 'ca', 'ab',
             'ba', 'abc', 'bac', 'bca', 'acb', 'cab', 'cba']),
    ("aac", ['', 'c', 'a', 'ac', 'ca', 'a', 'ac', 'ca', 'aa',
             'aa', 'aac', 'aac', 'aca', 'aca', 'caa', 'caa'])
])
def test_gen_all_strings(word, output):
    assert ww_game.gen_all_strings(word) == output
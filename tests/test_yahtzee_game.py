import pytest

from yahtzee import yahtzee_game

"""
Test score function
"""


@pytest.mark.parametrize("hand, output", [
    ((1, 1, 2, 6, 6, 6), 18),
    ((1, 5, 3), 5),
    ((5, 5, 5, 6, 6), 15)
])
def test_score(hand, output):
    assert yahtzee_game.score(hand) == output

@pytest.mark.parametrize("held_dice, num_die_sides, num_free_dice, outcome", [
    ((1, 2, 1), 2, 2, 4.5),
    ((), 2, 2, 2.5),
    ((1, 4, 4), 2, 0, 8)
])
def test_expected_value(held_dice, num_die_sides, num_free_dice, outcome):
    assert yahtzee_game.expected_value(held_dice, num_die_sides, num_free_dice) == outcome

@pytest.mark.parametrize("hand, outcome", [
    ((1, 2, 3), {(), (1,), (1, 2), (1, 2, 3), (1, 3), (2,), (2, 3), (3,)}),
    ((1, 2, 1), {(), (1,), (1, 1), (1, 2), (1, 2, 1), (2,), (2, 1)}),
    ((1, 1, 1), {(), (1,), (1, 1), (1, 1, 1)})
])
def test_gen_all_holds(hand, outcome):
    assert yahtzee_game.gen_all_holds(hand) == outcome

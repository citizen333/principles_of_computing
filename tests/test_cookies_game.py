import pytest
from poc.cookies import cookies_game


@pytest.fixture
def new_game():
    return cookies_game.ClickerState()


@pytest.fixture
def thirty_sec_game(new_game):
    new_game.wait(30)
    return new_game


def test_get_cookies(new_game):
    assert new_game.get_cookies() == 0.0


def test_get_cps(new_game):
    assert new_game.get_cps() == 1.0


def test_get_time(new_game):
    assert new_game.get_time() == 0.0


def test_get_history(new_game):
    assert new_game.get_history() == [(0.0, None, 0.0, 0.0)]


def test_time_until(new_game):
    assert new_game.time_until(17) == 17.0


@pytest.mark.parametrize("time, total_cookies, current_cookies, current_time", [
    (11, 11.0, 11.0, 11.0),
    (-3, 0.0, 0.0, 0.0)
])
def test_wait(new_game, time, total_cookies, current_cookies, current_time):
    new_game.wait(time)
    assert new_game._total_cookies == total_cookies
    assert new_game.get_cookies() == current_cookies
    assert new_game.get_time() == current_time


@pytest.mark.parametrize("item_name, cost, add_cps, history, current_cookies, current_cps", [
    ("item_0", -3, 5, [(0.0, None, 0.0, 0.0)], 30.0, 1.0),
    ("item_1", 10, 4, [(0.0, None, 0.0, 0.0), (30.0, "item_1", 10.0, 30.0)], 20.0, 5.0),
    ("item_2", 35, 4, [(0.0, None, 0.0, 0.0)], 30.0, 1.0),
])
def test_buy_item(thirty_sec_game, item_name, cost, add_cps,
                  history, current_cookies, current_cps):
    thirty_sec_game.buy_item(item_name, cost, add_cps)
    assert thirty_sec_game.get_history() == history
    assert thirty_sec_game.get_cookies() == current_cookies
    assert thirty_sec_game.get_cps() == current_cps

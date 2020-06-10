import pytest
from poc.zombie_apocalypse import za_game

@pytest.fixture
def apocalypse_sim_blank():
    return za_game.Apocalypse(3, 4)

@pytest.fixture
def apocalypse_sim_full():
    return za_game.Apocalypse(3, 4, [[0, 0], [2, 3]], [[2, 0]], [[0, 3]])

def test_apocalypse_clear(apocalypse_sim_full):
    apocalypse_sim_full.clear()
    assert str(apocalypse_sim_full) == '[0, 0, 0, 0]\n[0, 0, 0, 0]\n[0, 0, 0, 0]\n'
    assert list(apocalypse_sim_full.zombies()) == []
    assert list(apocalypse_sim_full.humans()) == []

def test_zombie_list(apocalypse_sim_full):
    apocalypse_sim_full.add_zombie(1, 1)
    apocalypse_sim_full.add_zombie(2, 2)
    assert apocalypse_sim_full.num_zombies() == 3
    assert list(apocalypse_sim_full.zombies()) == [[2, 0], [1, 1], [2, 2]]

def test_humans_list(apocalypse_sim_full):
    apocalypse_sim_full.add_human(1, 1)
    apocalypse_sim_full.add_human(2, 2)
    assert apocalypse_sim_full.num_humans() == 3
    assert list(apocalypse_sim_full.humans()) == [[0, 3], [1, 1], [2, 2]]
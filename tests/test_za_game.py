import pytest
from poc.zombie_apocalypse import za_game

@pytest.fixture
def apocalypse_sim_blank():
    return za_game.Apocalypse(3, 4)

@pytest.fixture
def apocalypse_sim_full():
    return za_game.Apocalypse(3, 4, [[0, 0], [2, 3]], [[2, 0]], [[0, 2]])

@pytest.fixture
def apocalypse_more_actors(apocalypse_sim_full):
    apocalypse_sim_full.add_zombie(1, 1)
    apocalypse_sim_full.add_human(2, 1)
    return apocalypse_sim_full

def test_apocalypse_clear(apocalypse_sim_full):
    apocalypse_sim_full.clear()
    assert str(apocalypse_sim_full) == '[0, 0, 0, 0]\n[0, 0, 0, 0]\n[0, 0, 0, 0]\n'
    assert list(apocalypse_sim_full.zombies()) == []
    assert list(apocalypse_sim_full.humans()) == []

def test_zombie_list(apocalypse_sim_full):
    apocalypse_sim_full.add_zombie(1, 1)
    apocalypse_sim_full.add_zombie(2, 2)
    assert apocalypse_sim_full.num_zombies() == 3
    assert list(apocalypse_sim_full.zombies()) == [(2, 0), (1, 1), (2, 2)]

def test_humans_list(apocalypse_sim_full):
    apocalypse_sim_full.add_human(1, 1)
    apocalypse_sim_full.add_human(2, 2)
    assert apocalypse_sim_full.num_humans() == 3
    assert list(apocalypse_sim_full.humans()) == [(0, 2), (1, 1), (2, 2)]

@pytest.mark.parametrize("entity_type, output",[
        (za_game.HUMAN, [[12, 1, 0, 1],
                         [2, 1, 1, 2],
                         [1, 0, 1, 12]]),
        (za_game.ZOMBIE, [[12, 1, 2, 3],
                          [1, 0, 1, 2],
                          [0, 1, 2, 12]])
])
def test_compute_distance_field(apocalypse_more_actors, entity_type, output):
    assert apocalypse_more_actors.compute_distance_field(entity_type) == output


def test_move_human(apocalypse_more_actors):
    zombie_distance_field = apocalypse_more_actors\
                                .compute_distance_field(za_game.ZOMBIE)
    apocalypse_more_actors.move_humans(zombie_distance_field)
    assert list(apocalypse_more_actors.humans()) == [(0, 3), (2, 2)]

def test_move_zombies(apocalypse_more_actors):
    human_distance_field = apocalypse_more_actors\
                                .compute_distance_field(za_game.HUMAN)
    print(apocalypse_more_actors)
    print(list(apocalypse_more_actors.zombies()))
    print(human_distance_field)
    apocalypse_more_actors.move_zombies(human_distance_field)
    assert list(apocalypse_more_actors.zombies()) == [(2, 1), (2, 1)]
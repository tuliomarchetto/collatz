from collatz.core import (
    T,
    collatz_step,
    max_excursion,
    parity_vector,
    stopping_time,
    syracuse,
    total_stopping_time,
    trajectory,
    v2,
)


def test_maps():
    assert collatz_step(7) == 22 and collatz_step(22) == 11
    assert T(7) == 11 and T(22) == 11
    assert syracuse(7) == 11 and syracuse(3) == 5
    assert T(7, d=-1) == 10
    assert v2(48) == 4


def test_trajectory_27():
    tr = trajectory(27, accelerated=False)
    assert tr[-1] == 1
    assert len(tr) - 1 == 111  # 27 takes 111 steps (original map)
    assert max(tr) == 9232


def test_stopping_times():
    assert total_stopping_time(1) == 0
    assert total_stopping_time(2) == 1
    assert stopping_time(3) == 4  # 3->5->8->4->2 (T): drops below 3 at step 4
    assert max_excursion(27) == 4616  # 9232/2 under the accelerated map


def test_parity_vector_shift():
    pv = parity_vector(27, 8)
    assert pv[0] == 1
    assert parity_vector(T(27), 7) == pv[1:]

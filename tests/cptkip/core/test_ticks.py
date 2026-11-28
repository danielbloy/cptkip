import time

from cptkip.core.ticks import TICKS_MAX, TICKS_PERIOD, ticks_add, ticks_diff, ticks_less, ticks_ms


class TestTicks:

    def test_ticks_ms_is_in_range_and_advances(self) -> None:
        start = ticks_ms()
        assert 0 <= start <= TICKS_MAX
        time.sleep(0.05)
        elapsed = ticks_diff(ticks_ms(), start)
        assert 40 <= elapsed <= 500

    def test_ticks_add_wraps(self) -> None:
        assert ticks_add(10, 5) == 15
        assert ticks_add(TICKS_MAX, 1) == 0
        assert ticks_add(TICKS_MAX - 4, 10) == 5
        assert ticks_add(5, -10) == TICKS_PERIOD - 5

    def test_ticks_diff_handles_wrap_around(self) -> None:
        assert ticks_diff(15, 10) == 5
        assert ticks_diff(10, 15) == -5
        assert ticks_diff(ticks_add(TICKS_MAX, 10), TICKS_MAX) == 10
        assert ticks_diff(TICKS_MAX, ticks_add(TICKS_MAX, 10)) == -10
        assert ticks_diff(3, TICKS_MAX - 2) == 6

    def test_ticks_less_handles_wrap_around(self) -> None:
        assert ticks_less(10, 15)
        assert not ticks_less(15, 10)
        assert not ticks_less(10, 10)
        assert ticks_less(TICKS_MAX, ticks_add(TICKS_MAX, 1))
        assert not ticks_less(ticks_add(TICKS_MAX, 1), TICKS_MAX)

    def test_values_fit_in_a_circuitpython_small_int(self) -> None:
        """
        Every value stays below 2**30 so it is a small int on CircuitPython and never
        allocates on the heap.
        """
        for value in (ticks_ms(), ticks_add(TICKS_MAX, TICKS_MAX), ticks_diff(0, TICKS_MAX)):
            assert -(1 << 30) <= value < (1 << 30)

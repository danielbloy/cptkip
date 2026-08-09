import time

import pytest

from cptkip.zero.run import run_for, update_for


class MockUpdate:
    def __init__(self):
        self.count = 0

    def update(self):
        self.count += 1


class MockAnimate:
    def __init__(self):
        self.count = 0

    def animate(self):
        self.count += 1


class MockUpdateAndAnimate:
    def __init__(self):
        self.count_update = 0
        self.count_animate = 0

    def update(self):
        self.count_update += 1

    def animate(self):
        self.count_animate += 1


class TestRunZero:
    """
    The tests in here are trivial as the examples uses these thoroughly
    and therefore test them adequeately.
    """

    def test_run_for_invalid(self):
        """
        Validates that run_for() rejects an invalid duration.
        """
        with pytest.raises(ValueError):
            run_for(0, lambda: None)

        with pytest.raises(ValueError):
            run_for(-1, lambda: None)

    def test_run_for(self):
        """
        Validates that run_for() executes the loop for the specified number of seconds.
        """
        count = 0

        def inc():
            nonlocal count
            count += 1

        # Try 1 second
        start = time.monotonic()
        run_for(1, inc)
        end = time.monotonic()

        assert end - start < 1.01
        assert count > 0

        # Try 2 seconds
        count = 0
        start = time.monotonic()
        run_for(2, inc)
        end = time.monotonic()

        assert end - start < 2.01
        assert count > 0

    def test_update_for_invalid(self):
        """
        Validates that update_for() rejects an invalid duration.
        """
        with pytest.raises(ValueError):
            update_for(0)

        with pytest.raises(ValueError):
            update_for(-1)

        with pytest.raises(ValueError):
            update_for(-1, lambda: None)

        with pytest.raises(ValueError):
            update_for(-1, 1)

    def test_update_for(self):
        """
        Validates that update_for() executes the loop for the specified number of seconds.
        """
        # Test with nothing to call.
        start = time.monotonic()
        update_for(1)
        end = time.monotonic()
        assert end - start < 2.01

        # Test with one update()
        start = time.monotonic()
        update = MockUpdate()
        update_for(1, update)
        end = time.monotonic()
        assert end - start < 2.01
        assert update.count > 0

        # Test with one animate()
        start = time.monotonic()
        animate = MockAnimate()
        update_for(1, animate)
        end = time.monotonic()
        assert end - start < 2.01
        assert animate.count > 0

        # Test with one update() and one animate()
        start = time.monotonic()
        update = MockUpdate()
        animate = MockAnimate()
        update_for(1, update, animate)
        end = time.monotonic()
        assert end - start < 2.01
        assert update.count > 0
        assert animate.count > 0

        # Test that is an object has update() and animate(), only update is called.
        start = time.monotonic()
        update_and_animate = MockUpdateAndAnimate()
        update_for(1, update_and_animate)
        end = time.monotonic()
        assert end - start < 2.01
        assert update_and_animate.count_update > 0
        assert update_and_animate.count_animate == 0

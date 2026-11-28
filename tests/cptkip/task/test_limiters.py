from time import sleep

from cptkip.task.limiters import count_limiter, duration_limiter


class TestCountLimiter:

    def test_count_limiter(self) -> None:
        """
        Some simple test for count limiter.
        """
        limiter = count_limiter(-1)
        assert limiter() is False

        limiter = count_limiter(0)
        assert limiter() is False

        limiter = count_limiter(1)
        assert limiter() is True
        assert limiter() is False

        limiter = count_limiter(2)
        assert limiter() is True
        assert limiter() is True
        assert limiter() is False


class TestDurationLimiter:

    def test_duration_limiter(self) -> None:
        """
        Some simple tests for duration limiter.
        """
        limiter = duration_limiter(-1)
        assert limiter() is False

        limiter = duration_limiter(0)
        assert limiter() is True
        sleep(0.001)
        assert limiter() is False

        limiter = duration_limiter(0.2)
        assert limiter() is True
        assert limiter() is True
        assert limiter() is True
        sleep(0.05)
        assert limiter() is True
        assert limiter() is True
        sleep(0.05)
        assert limiter() is True
        assert limiter() is True
        sleep(0.05)
        assert limiter() is True
        assert limiter() is True
        sleep(0.06)
        assert limiter() is False

    def test_duration_limiter_ignores_wall_clock_changes(self, monkeypatch):
        """
        duration_limiter must measure elapsed time with a monotonic clock, so a frozen
        (or jumping) wall clock does not affect it.
        """
        import time
        monkeypatch.setattr(time, "time", lambda: 0.0)
        limiter = duration_limiter(0.05)
        assert limiter()
        time.sleep(0.1)
        assert not limiter()

def execute():
    from time import monotonic, sleep
    from cptkip.task.limiters import count_limiter, duration_limiter

    limiter = count_limiter(3)
    assert [limiter() for _ in range(5)] == [True, True, True, False, False]

    limiter = duration_limiter(0.5)
    start = monotonic()
    while limiter():
        sleep(0.01)
    elapsed = monotonic() - start
    print(f"duration_limiter(0.5) ran for {elapsed:.2f}s")
    # Generous upper bound: before #79 duration_limiter used time.time(), which only
    # has whole-second resolution on CircuitPython.
    assert 0.45 <= elapsed <= 1.5, f"duration_limiter(0.5) ran for {elapsed:.2f}s"


if __name__ == '__main__':
    execute()

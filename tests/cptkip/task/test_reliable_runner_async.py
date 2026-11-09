import asyncio

from cptkip.task.limiters import count_limiter
from cptkip.task.reliable_runner_async import run


class TestReliableRunnerAsync:

    def test_run_with_no_tasks(self):
        """
        Calls run() but passes no functions. run() should return gracefully.
        """
        run()

    def test_run_with_one_task(self):
        """
        Calls run() with a single task that terminates immediately having been called once.
        """
        one_count: int = 0

        async def one() -> None:
            nonlocal one_count
            one_count += 1

        run(one)

        assert one_count == 1

    def test_run_with_two_tasks(self):
        """
        Calls run() with two tasks that terminate immediately having been called once.
        """
        one_count: int = 0
        two_count: int = 0

        async def one() -> None:
            nonlocal one_count
            one_count += 1

        async def two() -> None:
            nonlocal two_count
            two_count += 1

        run(one, two)

        assert one_count == 1
        assert two_count == 1

    def test_run_with_three_tasks(self):
        """
        Runs three tasks, each of which completes at a different point in time.
        """
        one_count: int = 0
        two_count: int = 0
        three_count: int = 0

        async def one() -> None:
            nonlocal one_count
            while one_count < 11:
                one_count += 1
                await asyncio.sleep(0)

        async def two() -> None:
            nonlocal two_count
            while two_count < 22:
                two_count += 1
                await asyncio.sleep(0)

        async def three() -> None:
            nonlocal three_count
            while three_count < 33:
                three_count += 1
                await asyncio.sleep(0)

        run(three, one, two)

        assert one_count == 11
        assert two_count == 22
        assert three_count == 33

    def test_run_with_three_tasks_round_robin(self):
        """
        Runs three tasks and validates they run in a round-robin fashion.
        """
        call_order = []

        async def one() -> None:
            one_count: int = 0
            while one_count < 2:
                one_count += 1
                call_order.append("one")
                await asyncio.sleep(0)

        async def two() -> None:
            two_count: int = 0
            while two_count < 3:
                two_count += 1
                call_order.append("two")
                await asyncio.sleep(0)

        async def three() -> None:
            three_count: int = 0
            while three_count < 1:
                three_count += 1
                call_order.append("three")
                await asyncio.sleep(0)

        run(one, two, three)

        assert call_order == ["one", "two", "three", "one", "two", "two"]

    def test_run_with_three_tasks_round_robin_no_await(self):
        """
        Runs three tasks and none have an await so they will not run in a round-robin fashion
        """
        call_order = []

        async def one() -> None:
            one_count: int = 0
            while one_count < 2:
                one_count += 1
                call_order.append("one")

        async def two() -> None:
            two_count: int = 0
            while two_count < 3:
                two_count += 1
                call_order.append("two")

        async def three() -> None:
            three_count: int = 0
            while three_count < 1:
                three_count += 1
                call_order.append("three")

        run(one, two, three)

        assert call_order == ["one", "one", "two", "two", "two", "three"]

    def test_run_with_task_that_throws_exception(self):
        """
        Calls run() with a task that throws an exception.
        """
        call_count: int = 0

        async def raise_exception() -> None:
            nonlocal call_count
            while call_count < 30:
                call_count += 1

                raise Exception

        # Runner will catch the exception and terminate.
        run(raise_exception)
        assert call_count == 30

    def test_run_with_some_tasks_that_throw_exceptions(self):
        """
        Calls run() with multiple tasks, some of which throw an exception. The runner should
        continue executing the other tasks. Depending on the configuration of restart_on_exception,
        will determine if the exception raising tasks get removed from execution.
        """
        call_count_1: int = 0
        call_count_2: int = 0
        call_count_3: int = 0
        call_count_4: int = 0

        async def one() -> None:
            nonlocal call_count_1
            while call_count_1 < 10:
                call_count_1 += 1
                await asyncio.sleep(0)

        async def two() -> None:
            nonlocal call_count_2
            while call_count_2 < 20:
                call_count_2 += 1
                await asyncio.sleep(0)

        # This raises an exception every time.
        async def three() -> None:
            nonlocal call_count_3
            while call_count_3 < 30:
                call_count_3 += 1
                await asyncio.sleep(0)
                raise Exception("three")

        # This raises an exception twice
        async def four() -> None:
            nonlocal call_count_4
            while call_count_4 < 15:
                call_count_4 += 1
                await asyncio.sleep(0)
                if call_count_4 in (3, 6):
                    raise Exception("four")

        # Runner will catch the exception and terminate.
        run(one, two, three, four)
        assert call_count_1 == 10
        assert call_count_2 == 20
        assert call_count_3 == 30
        assert call_count_4 == 15  # Stops at first exception

        # Now repeat the test with restart disabled.
        call_count_1: int = 0
        call_count_2: int = 0
        call_count_3: int = 0
        call_count_4: int = 0
        run(one, two, three, four, restart_on_exception=False)
        assert call_count_1 == 10
        assert call_count_2 == 20
        assert call_count_3 == 1
        assert call_count_4 == 3  # Stops at first exception

    def test_funcs_never_called(self) -> None:
        """
        Validates that the runner terminates straight away
        when the continue_func always returns False.
        """
        called = False

        async def task() -> None:
            nonlocal called
            called = True

        run(task, continue_func=lambda: False)

        assert not called

    def test_runner_stops(self):
        """
        Validates that the runner terminates when the continue_func returns False.
        """
        call_count_1: int = 0
        call_count_2: int = 0
        call_count_3: int = 0

        async def runaway() -> None:
            nonlocal call_count_1
            while True:
                call_count_1 += 1
                await asyncio.sleep(0)

        async def two() -> None:
            nonlocal call_count_2
            while call_count_2 < 20:
                call_count_2 += 1
                await asyncio.sleep(0)

        # This raises an exception every time.
        async def three() -> None:
            nonlocal call_count_3
            while call_count_3 < 30:
                call_count_3 += 1
                await asyncio.sleep(0)
                raise Exception("three")

        continue_fn = count_limiter(40)

        run(runaway, two, three, continue_func=continue_fn)
        assert call_count_1 == 40
        assert call_count_2 == 20
        assert call_count_3 <= 30  # The exception handling means we cannot be certain how many

import asyncio

import pytest

from cptkip.task.basic_runner_async import run


class TestBasicRunnerAsync:

    def test_run_with_no_tasks(self):
        """
        Calls run() but passes an empty list of functions. run() should return gracefully.
        """
        run([])

    def test_run_with_one_task(self):
        """
        Calls run() with a single task that terminates immediately having been called once.
        """
        one_count: int = 0

        async def one() -> None:
            nonlocal one_count
            one_count += 1

        run([one])

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

        run([one, two])

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

        run([three, one, two])

        assert one_count == 11
        assert two_count == 22
        assert three_count == 33

    def test_run_with_three_tasks_round_robin(self):
        """
        Runs three tasks and validates they run in a round-robin fashion.
        """
        one_count: int = 0
        two_count: int = 0
        three_count: int = 0
        call_order = []

        async def one() -> None:
            nonlocal one_count
            while one_count < 2:
                one_count += 1
                call_order.append("one")
                await asyncio.sleep(0)

        async def two() -> None:
            nonlocal two_count
            while two_count < 3:
                two_count += 1
                call_order.append("two")
                await asyncio.sleep(0)

        async def three() -> None:
            nonlocal three_count
            while three_count < 1:
                three_count += 1
                call_order.append("three")
                await asyncio.sleep(0)

        run([one, two, three])

        assert call_order == ["one", "two", "three", "one", "two", "two"]

    def test_run_with_three_tasks_round_robin_no_await(self):
        """
        Runs three tasks and none have an await so they will not run in a round-robin fashion
        """
        one_count: int = 0
        two_count: int = 0
        three_count: int = 0
        call_order = []

        async def one() -> None:
            nonlocal one_count
            while one_count < 2:
                one_count += 1
                call_order.append("one")

        async def two() -> None:
            nonlocal two_count
            while two_count < 3:
                two_count += 1
                call_order.append("two")

        async def three() -> None:
            nonlocal three_count
            while three_count < 1:
                three_count += 1
                call_order.append("three")

        run([one, two, three])

        assert call_order == ["one", "one", "two", "two", "two", "three"]

    def test_run_with_task_that_throws_exception(self):
        """
        Calls run() with a task that throws an exception. This will propagate out as
        basic runner has no error handling.
        """

        async def raise_exception() -> None:
            raise Exception

        with pytest.raises(Exception):
            run([raise_exception])

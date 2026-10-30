from cptkip.task.reliable_runner import run


class TestReliableRunner:

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

        def one() -> bool:
            nonlocal one_count
            one_count += 1
            return False

        run(one)

        assert one_count == 1

    def test_run_with_two_tasks(self):
        """
        Calls run() with two tasks that terminate immediately having been called once.
        """
        one_count: int = 0
        two_count: int = 0

        def one() -> bool:
            nonlocal one_count
            one_count += 1
            return False

        def two() -> bool:
            nonlocal two_count
            two_count += 1
            return False

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

        def one() -> bool:
            nonlocal one_count
            one_count += 1
            return one_count < 11

        def two() -> bool:
            nonlocal two_count
            two_count += 1
            return two_count < 22

        def three() -> bool:
            nonlocal three_count
            three_count += 1
            return three_count < 33

        run(three, one, two)

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

        def one() -> bool:
            nonlocal one_count
            one_count += 1
            call_order.append("one")
            return one_count < 2

        def two() -> bool:
            nonlocal two_count
            two_count += 1
            call_order.append("two")
            return two_count < 3

        def three() -> bool:
            nonlocal three_count
            three_count += 1
            call_order.append("three")
            return three_count < 1

        run(one, two, three)

        assert call_order == ["one", "two", "three", "one", "two", "two"]

    def test_run_with_task_that_throws_exception(self):
        """
        Calls run() with a task that throws an exception.
        """
        call_count: int = 0

        def raise_exception() -> bool:
            nonlocal call_count
            call_count += 1
            # Put a hard stop in here to avoid running forever
            if call_count >= 30:
                return False

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

        def one() -> bool:
            nonlocal call_count_1
            call_count_1 += 1
            return call_count_1 < 10

        def two() -> bool:
            nonlocal call_count_2
            call_count_2 += 1
            return call_count_2 < 20

        # This raises an exception every time.
        def three() -> bool:
            nonlocal call_count_3
            call_count_3 += 1
            # Put a hard stop in here to avoid running forever
            if call_count_3 >= 30:
                return False

            raise Exception("three")

        # This raises an exception twice
        def four() -> bool:
            nonlocal call_count_4
            call_count_4 += 1
            if call_count_4 in (3, 6):
                raise Exception("four")

            return call_count_4 < 15

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

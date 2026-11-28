import asyncio

import cptkip.device.button as button
import cptkip.task.periodic_task_async as periodic_task
import tests.cptkip.utilities as utils
from cptkip.task.limiters import count_limiter


class MockInputPin:
    def __init__(self, value: bool = True, pullup: bool = True):
        self.value = value
        self.pullup = pullup

    def deinit(self) -> None:
        pass


# noinspection PyTypeChecker
class TestButton:
    def test_deinit_can_be_called_multiple_times(self):
        """
        Validates that deinit() can be called multiple times without issue.
        """
        btn = button.Button(MockInputPin())
        assert btn.pin.value

        btn.deinit()
        btn.deinit()
        btn.deinit()

    def test_with_resources(self):
        """
        Validates that a button can be used in a with statement.
        """

        with button.Button(MockInputPin()) as btn:
            pass

    def test_no_callbacks(self):
        """
        Validates the most basic case with no callbacks.
        """
        for pullup in [True, False, None]:
            btn = button.Button(MockInputPin(value=pullup is None or pullup, pullup=pullup))

            async def update() -> None:
                btn.update()

            task = periodic_task.create(update, continue_func=lambda: False)
            asyncio.run(task())

            task = periodic_task.create(update, continue_func=count_limiter(1))
            asyncio.run(task())

            task = periodic_task.create(update, continue_func=count_limiter(10))
            asyncio.run(task())

    def test_click(self):
        """
        Validates the most basic case with a single click.
        """

        for pullup in [True, False, None]:
            single_click_count: int = 0

            def single_click() -> None:
                nonlocal single_click_count
                single_click_count += 1

            pin = MockInputPin(value=pullup is None or pullup, pullup=pullup)
            btn = button.Button(pin, click=single_click)

            async def update() -> None:
                btn.update()

            task = periodic_task.create(update,
                                        continue_func=utils.value_flip(1.0, pin, [0.1, 0.3]))
            asyncio.run(task())

            assert single_click_count == 1

    def test_multi_click(self):
        """
        Validates the most basic case with a multi click.
        """
        for pullup in [True, False, None]:
            multi_click_count: int = 0

            def multi_click() -> None:
                nonlocal multi_click_count
                multi_click_count += 1

            pin = MockInputPin(value=pullup is None or pullup, pullup=pullup)
            btn = button.Button(pin, multi_click=multi_click)

            async def update() -> None:
                btn.update()

            task = periodic_task.create(update, continue_func=utils.value_flip(1, pin,
                                                                               [0.1, 0.3, 0.4,
                                                                                0.6]))
            asyncio.run(task())

            assert multi_click_count == 1

    def test_long_click(self):
        """
        Validates the most basic case with a long click.
        """
        for pullup in [True, False, None]:
            long_click_count: int = 0

            def long_click() -> None:
                nonlocal long_click_count
                long_click_count += 1

            pin = MockInputPin(value=pullup is None or pullup, pullup=pullup)
            btn = button.Button(pin, long_click=long_click)

            async def update() -> None:
                btn.update()

            task = periodic_task.create(update, continue_func=utils.value_flip(3, pin, [0.05, 2.1]))
            asyncio.run(task())

            assert long_click_count == 1

    def test_all_clicks(self):
        """
        Validates the most basic case with a mixture of clicks in the following order:
            * multi-click
            * single-click
            * long-click
        """
        for pullup in [True, False, None]:
            single_click_count: int = 0
            multi_click_count: int = 0
            long_click_count: int = 0

            def single_click() -> None:
                nonlocal single_click_count
                single_click_count += 1
                assert single_click_count == 1
                assert multi_click_count == 1
                assert long_click_count == 0

            def multi_click() -> None:
                nonlocal multi_click_count
                multi_click_count += 1
                assert single_click_count == 0
                assert multi_click_count == 1
                assert long_click_count == 0

            def long_click() -> None:
                nonlocal long_click_count
                long_click_count += 1
                assert single_click_count == 1
                assert multi_click_count == 1
                assert long_click_count == 1

            pin = MockInputPin(value=pullup is None or pullup, pullup=pullup)
            btn = button.Button(pin, click=single_click, multi_click=multi_click,
                                long_click=long_click)

            async def update() -> None:
                btn.update()

            task = periodic_task.create(
                update,
                continue_func=utils.value_flip(3.5, pin, [0.1, 0.3, 0.4, 0.6, 0.9, 1.1, 1.2, 3.3]))
            asyncio.run(task())

            assert single_click_count == 1
            assert multi_click_count == 1
            assert long_click_count == 1

    def test_click_multi(self):
        """
        Validates the multiple single clicks.
        """
        for pullup in [True, False, None]:
            single_click_count: int = 0

            def single_click() -> None:
                nonlocal single_click_count
                single_click_count += 1

            pin = MockInputPin(value=pullup is None or pullup, pullup=pullup)
            btn = button.Button(pin, click=single_click)

            async def update() -> None:
                btn.update()

            task = periodic_task.create(update, continue_func=utils.value_flip(1.2, pin,
                                                                               [0.1, 0.3, 0.6,
                                                                                0.8]))
            asyncio.run(task())

            assert single_click_count == 2

    def test_press_release_and_click_count(self):
        """
        Validates press/release callbacks fire on each transition and click_count
        records the number of presses in a multi-click.
        """
        events = []
        pin = MockInputPin(value=True, pullup=True)
        btn = button.Button(pin,
                            multi_click=lambda: events.append(("multi", btn.click_count)),
                            press=lambda: events.append("press"),
                            release=lambda: events.append("release"))

        async def update() -> None:
            btn.update()

        task = periodic_task.create(update,
                                    continue_func=utils.value_flip(1.0, pin, [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]))
        asyncio.run(task())

        assert events == ["press", "release", "press", "release", "press", "release", ("multi", 3)]

    def test_long_duration_is_configurable(self):
        """
        Validates a shorter long_duration_ms triggers a long click sooner.
        """
        long_clicks = 0

        def long_click() -> None:
            nonlocal long_clicks
            long_clicks += 1

        pin = MockInputPin(value=True, pullup=True)
        btn = button.Button(pin, long_click=long_click, long_duration_ms=300)

        async def update() -> None:
            btn.update()

        # Held down for 0.5 seconds: long enough for 300ms but not the 2 second default.
        task = periodic_task.create(update, continue_func=utils.value_flip(0.8, pin, [0.1, 0.6]))
        asyncio.run(task())

        assert long_clicks == 1

import asyncio

import cptkip.device.button as button
import cptkip.task.periodic_task as periodic_task
import tests.cptkip.utilities as utils


class MockInputPin:
    def __init__(self, value: bool = True):
        self.value = value

    def deinit(self) -> None:
        pass


# noinspection PyTypeChecker
class TestButton:
    def test_no_callbacks(self):
        """
        Validates the most basic case with no callbacks.
        """

        btn = button.Button(MockInputPin)

        async def update() -> None:
            btn.update()

        task = periodic_task.create(update, continue_func=utils.stop)
        asyncio.run(task())

        task = periodic_task.create(update, continue_func=utils.count_limiter(1))
        asyncio.run(task())

        task = periodic_task.create(update, continue_func=utils.count_limiter(10))
        asyncio.run(task())

    def test_click(self):
        """
        Validates the most basic case with a single click.
        """

        single_click_count: int = 0

        def single_click() -> None:
            nonlocal single_click_count
            single_click_count += 1

        pin = MockInputPin()
        btn = button.Button(pin, click=single_click)

        async def update() -> None:
            btn.update()

        task = periodic_task.create(update, continue_func=utils.value_flip(1.0, pin, [0.1, 0.3]))
        asyncio.run(task())

        assert single_click_count == 1

    def test_multi_click(self):
        """
        Validates the most basic case with a multi click.
        """

        multi_click_count: int = 0

        def multi_click() -> None:
            nonlocal multi_click_count
            multi_click_count += 1

        pin = MockInputPin()
        btn = button.Button(pin, multi_click=multi_click)

        async def update() -> None:
            btn.update()

        task = periodic_task.create(update, continue_func=utils.value_flip(1, pin, [0.1, 0.3, 0.4, 0.6]))
        asyncio.run(task())

        assert multi_click_count == 1

    def test_long_click(self):
        """
        Validates the most basic case with a long click.
        """

        long_click_count: int = 0

        def long_click() -> None:
            nonlocal long_click_count
            long_click_count += 1

        pin = MockInputPin()
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

        pin = MockInputPin()
        btn = button.Button(pin, click=single_click, multi_click=multi_click, long_click=long_click)

        async def update() -> None:
            btn.update()

        task = periodic_task.create(update,
                                    continue_func=utils.value_flip(3.5, pin, [0.1, 0.3, 0.4, 0.6, 0.9, 1.1, 1.2, 3.3]))
        asyncio.run(task())

        assert single_click_count == 1
        assert multi_click_count == 1
        assert long_click_count == 1

    def test_click_multi(self):
        """
        Validates the multiple single clicks.
        """

        single_click_count: int = 0

        def single_click() -> None:
            nonlocal single_click_count
            single_click_count += 1

        pin = MockInputPin()
        btn = button.Button(pin, click=single_click)

        async def update() -> None:
            btn.update()

        task = periodic_task.create(update, continue_func=utils.value_flip(1.2, pin, [0.1, 0.3, 0.6, 0.8]))
        asyncio.run(task())

        assert single_click_count == 2

import asyncio

import cptkip.device.button as button
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
        btn = button.create(MockInputPin, continue_func=utils.stop)
        asyncio.run(btn())

        btn = button.create(MockInputPin, continue_func=utils.count_limiter(1))
        asyncio.run(btn())

        btn = button.create(MockInputPin, continue_func=utils.count_limiter(10))
        asyncio.run(btn())

    def test_click(self):
        """
        Validates the most basic case with a single click.
        """

        single_click_count: int = 0

        async def single_click() -> None:
            nonlocal single_click_count
            single_click_count += 1

        pin = MockInputPin()
        btn = button.create(pin, click=single_click,
                            continue_func=utils.value_flip(1.0, pin, [0.1, 0.3]))
        asyncio.run(btn())

        assert single_click_count == 1

    def test_multi_click(self):
        """
        Validates the most basic case with a multi click.
        """

        multi_click_count: int = 0

        async def multi_click() -> None:
            nonlocal multi_click_count
            multi_click_count += 1

        pin = MockInputPin()
        btn = button.create(pin, multi_click=multi_click,
                            continue_func=utils.value_flip(1, pin, [0.1, 0.3, 0.4, 0.6]))
        asyncio.run(btn())

        assert multi_click_count == 1

    def test_long_click(self):
        """
        Validates the most basic case with a long click.
        """

        long_click_count: int = 0

        async def long_click() -> None:
            nonlocal long_click_count
            long_click_count += 1

        pin = MockInputPin()
        btn = button.create(pin, long_click=long_click,
                            continue_func=utils.value_flip(3, pin, [0.05, 2.1]))
        asyncio.run(btn())

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

        async def single_click() -> None:
            nonlocal single_click_count
            single_click_count += 1
            assert single_click_count == 1
            assert multi_click_count == 1
            assert long_click_count == 0

        async def multi_click() -> None:
            nonlocal multi_click_count
            multi_click_count += 1
            assert single_click_count == 0
            assert multi_click_count == 1
            assert long_click_count == 0

        async def long_click() -> None:
            nonlocal long_click_count
            long_click_count += 1
            assert single_click_count == 1
            assert multi_click_count == 1
            assert long_click_count == 1

        pin = MockInputPin()
        btn = button.create(pin, click=single_click, multi_click=multi_click, long_click=long_click,
                            continue_func=utils.value_flip(3.5, pin, [0.1, 0.3, 0.4, 0.6, 0.9, 1.1, 1.2, 3.3]))
        asyncio.run(btn())

        assert single_click_count == 1
        assert multi_click_count == 1
        assert long_click_count == 1

    def test_click_multi(self):
        """
        Validates the multiple single clicks.
        """

        single_click_count: int = 0

        async def single_click() -> None:
            nonlocal single_click_count
            single_click_count += 1

        pin = MockInputPin()
        btn = button.create(pin, click=single_click,
                            continue_func=utils.value_flip(1.2, pin, [0.1, 0.3, 0.6, 0.8]))
        asyncio.run(btn())

        assert single_click_count == 2

    def test_using_begin_func(self):
        """
        Validates the begin function is called once and only once.
        """
        single_click_count: int = 0

        async def single_click() -> None:
            assert begin_count == 1
            nonlocal single_click_count
            single_click_count += 1

        begin_count: int = 0

        async def begin_func() -> None:
            assert single_click_count == 0
            nonlocal begin_count
            begin_count += 1

        pin = MockInputPin()
        btn = button.create(pin, click=single_click, begin=begin_func,
                            continue_func=utils.value_flip(1.0, pin, [0.1, 0.3]))

        asyncio.run(btn())
        assert single_click_count == 1
        assert begin_count == 1

    def test_using_end_func(self):
        """
        Validates the end function is called once and only once.
        """
        single_click_count: int = 0

        async def single_click() -> None:
            assert end_count == 0
            nonlocal single_click_count
            single_click_count += 1

        end_count: int = 0

        async def end_func() -> None:
            assert single_click_count == 1
            nonlocal end_count
            end_count += 1

        pin = MockInputPin()
        btn = button.create(pin, click=single_click, end=end_func,
                            continue_func=utils.value_flip(1.0, pin, [0.1, 0.3]))

        asyncio.run(btn())
        assert single_click_count == 1
        assert end_count == 1

    def test_using_begin_and_end_funcs(self):
        """
        Validates the begin and end functions are called once and only once.
        """
        single_click_count: int = 0

        async def single_click() -> None:
            assert begin_count == 1
            assert end_count == 0
            nonlocal single_click_count
            single_click_count += 1

        begin_count: int = 0

        async def begin_func() -> None:
            assert single_click_count == 0
            assert end_count == 0
            nonlocal begin_count
            begin_count += 1

        end_count: int = 0

        async def end_func() -> None:
            assert begin_count == 1
            assert single_click_count == 1
            nonlocal end_count
            end_count += 1

        pin = MockInputPin()
        btn = button.create(pin, click=single_click, begin=begin_func, end=end_func,
                            continue_func=utils.value_flip(1.0, pin, [0.1, 0.3]))

        asyncio.run(btn())
        assert single_click_count == 1
        assert begin_count == 1
        assert end_count == 1

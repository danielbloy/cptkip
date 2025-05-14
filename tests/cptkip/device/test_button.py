import asyncio

import cptkip.device.button as button
import cptkip.utilities as utils


class MockInputPin:
    def __init__(self, value: bool = True):
        self.value = value

    def deinit(self) -> None:
        pass


class TestButton:
    def test_no_callbacks(self):
        """
        Validates the most basic case with no callbacks.
        """
        btn = button.new(MockInputPin, continue_func=utils.stop)
        asyncio.run(btn())

        btn = button.new(MockInputPin, continue_func=utils.count_limiter(1))
        asyncio.run(btn())

        btn = button.new(MockInputPin, continue_func=utils.count_limiter(10))
        asyncio.run(btn())

    def test_click(self):
        """
        Validates the most basic case with a single click.
        """

        click_count: int = 0

        async def single_click() -> None:
            nonlocal click_count
            click_count += 1

        pin = MockInputPin()
        btn = button.new(pin, click=single_click,
                         continue_func=utils.value_flip(1, pin, [0.1, 0.3]))
        asyncio.run(btn())

        assert click_count == 1

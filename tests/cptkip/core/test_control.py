import cptkip.core.control as control


class TestControl:

    def test_ns_per_second(self):
        assert control.NS_PER_SECOND == 1_000_000_000

    def test_periodic_loop_wait_ratio(self):
        assert control.PERIODIC_LOOP_WAIT_RATIO > 0
        assert isinstance(control.PERIODIC_LOOP_WAIT_RATIO, int)

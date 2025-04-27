import cptkip.cpu.cpu as cpu


class TestCpu:
    def test_info(self):
        """
        Tests the expected values are returned when calling info()
        """
        assert len(cpu.info()) == 3
        assert "temperature" in cpu.info()
        assert "frequency" in cpu.info()
        assert "voltage" in cpu.info()

    def test_restart(self):
        """
        Simply tests there is no error when calling restart()
        """
        cpu.restart()

import cptkip.core.environment as environment
import cptkip.cpu.cpu as cpu


class FakeCpu:
    def __init__(self, temperature, frequency, voltage):
        self.temperature = temperature
        self.frequency = frequency
        self.voltage = voltage


class FakeMicrocontroller:
    """Stand-in for the `microcontroller` module, which only exists on-device."""

    def __init__(self, temperature=42.0, frequency=133_000_000, voltage=3.3):
        self.cpu = FakeCpu(temperature, frequency, voltage)
        self.reset_called = False

    def reset(self):
        self.reset_called = True


class TestCpu:
    def test_info(self):
        """
        Tests the expected values are returned when calling info()
        """
        assert len(cpu.info()) == 3
        assert "temperature" in cpu.info()
        assert "frequency" in cpu.info()
        assert "voltage" in cpu.info()

    def test_info_on_desktop_reports_not_available(self):
        """
        On desktop (no microcontroller module) every value is "n/a".
        """
        assert cpu.info() == {"temperature": "n/a", "frequency": "n/a", "voltage": "n/a"}

    def test_info_on_microcontroller(self, monkeypatch):
        """
        On a microcontroller, real values reported by the `microcontroller`
        module are returned as-is.
        """
        fake = FakeMicrocontroller(temperature=42.0, frequency=133_000_000, voltage=3.3)
        monkeypatch.setattr(cpu, "microcontroller", fake, raising=False)
        monkeypatch.setattr(environment, "is_running_on_microcontroller", lambda: True)

        assert cpu.info() == {"temperature": 42.0, "frequency": 133_000_000, "voltage": 3.3}

    def test_info_on_microcontroller_with_unsupported_values(self, monkeypatch):
        """
        Any of temperature/frequency/voltage that the board reports as None
        (unsupported) is surfaced as "n/a", same as on desktop.
        """
        fake = FakeMicrocontroller(temperature=None, frequency=None, voltage=None)
        monkeypatch.setattr(cpu, "microcontroller", fake, raising=False)
        monkeypatch.setattr(environment, "is_running_on_microcontroller", lambda: True)

        assert cpu.info() == {"temperature": "n/a", "frequency": "n/a", "voltage": "n/a"}

    def test_restart(self):
        """
        Simply tests there is no error when calling restart()
        """
        cpu.restart()

    def test_restart_on_microcontroller(self, monkeypatch):
        """
        On a microcontroller, restart() resets it via the `microcontroller` module.
        """
        fake = FakeMicrocontroller()
        monkeypatch.setattr(cpu, "microcontroller", fake, raising=False)
        monkeypatch.setattr(environment, "is_running_on_microcontroller", lambda: True)

        cpu.restart()
        assert fake.reset_called

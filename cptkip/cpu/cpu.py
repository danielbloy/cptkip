import cptkip.core.environment as environment

if environment.is_running_on_microcontroller():
    import microcontroller


# noinspection PyUnresolvedReferences
def info() -> dict:
    """
    Returns some basic information about the state of the CPU: temperature,
    frequency and voltage. On a microcontroller these are real values, or
    "n/a" if the board doesn't report a particular one. On desktop, all
    three are always "n/a".
    """
    if environment.is_running_on_microcontroller():
        # Each property is a hardware read, so read each exactly once.
        cpu = microcontroller.cpu
        temperature = cpu.temperature
        frequency = cpu.frequency
        voltage = cpu.voltage
        return {
            "temperature": "n/a" if temperature is None else temperature,
            "frequency": "n/a" if frequency is None else frequency,
            "voltage": "n/a" if voltage is None else voltage,
        }

    else:
        return {
            "temperature": "n/a",
            "frequency": "n/a",
            "voltage": "n/a",
        }


# noinspection PyUnresolvedReferences
def restart() -> None:
    """
    Reboots the microcontroller; does nothing for a non-microcontroller.
    """
    if environment.is_running_on_microcontroller():
        microcontroller.reset()

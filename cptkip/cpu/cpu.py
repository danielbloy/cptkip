import cptkip.core.environment as environment

if environment.is_running_on_microcontroller():
    import microcontroller


def info():
    """
    Returns some basic information about the state of the CPU.
    """
    if environment.is_running_on_microcontroller():
        return {
            "temperature": "n/a" if microcontroller.cpu.temperature is None else microcontroller.cpu.temperature,
            "frequency": "n/a" if microcontroller.cpu.frequency is None else microcontroller.cpu.frequency,
            "voltage": "n/a" if microcontroller.cpu.voltage is None else microcontroller.cpu.voltage,
        }

    else:
        return {
            "temperature": "n/a",
            "frequency": "n/a",
            "voltage": "n/a",
        }


def restart():
    """
    Reboots the microcontroller; does nothing for a non-microcontroller.
    """
    if environment.is_running_on_microcontroller():
        microcontroller.reset()

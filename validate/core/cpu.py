def execute():
    import cptkip.cpu.cpu as cpu

    # Read once: each call to info() reads the hardware and builds a new dict.
    info = cpu.info()

    print(f"Temperature .. : {info["temperature"]}")
    print(f"Frequency .... : {info["frequency"]}")
    print(f"Voltage ...... : {info["voltage"]}")

    assert info is not None
    assert len(info) == 3
    assert info["temperature"] is not None
    assert info["frequency"] is not None
    assert info["voltage"] is not None


if __name__ == '__main__':
    execute()

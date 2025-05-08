def execute():
    import cptkip.cpu.cpu as cpu
    import cptkip.core.logging as log

    log.set_log_level(log.INFO)
    assert cpu.info() is not None
    assert len(cpu.info()) == 3
    assert cpu.info()["temperature"] is not None
    assert cpu.info()["frequency"] is not None
    assert cpu.info()["voltage"] is not None


if __name__ == '__main__':
    execute()

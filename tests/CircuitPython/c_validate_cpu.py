def execute():
    import cptkip.cpu.cpu as cpu
    import cptkip.core.logging as log

    log.set_log_level(log.INFO)
    log.info('PASS' if cpu.info() is not None else 'FAIL FAIL FAIL FAIL')
    log.info(cpu.info())


if __name__ == '__main__':
    execute()

def execute():
    import cptkip.core.logging as log
    log.set_log_level(log.INFO)
    log.info('PASS')

    import cptkip.config.configuration as config

    # This tests that the logging level is loaded from the config file along with other properties.
    assert config.LOG_LEVEL == log.ERROR
    assert config.TEST_VALUE == 123.456
    assert config.TEST_STRING == "Hello world!"
    assert config.DEBUG

    log.critical('PASS')
    log.error('PASS')
    log.warn('FAIL FAIL FAIL FAIL')
    log.info('FAIL FAIL FAIL FAIL')
    log.debug('FAIL FAIL FAIL FAIL')


if __name__ == '__main__':
    execute()

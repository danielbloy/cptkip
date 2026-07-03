# NOTE: For the tests in here to pass, the file `validate/config/py` needs to be
#       copied to the root of the CircuitPython drive.

def execute():
    import cptkip.core.logging as log
    log.set_log_level(log.DEBUG)
    log.debug('PASS')

    import cptkip.config.configuration as config

    # This tests that the logging level is loaded from the config file along with other properties.
    assert config.LOG_LEVEL == log.INFO
    assert config.TEST_VALUE == 123.456
    assert config.TEST_STRING == "Hello world!"
    assert config.DEBUG

    log.critical('PASS')
    log.error('PASS')
    log.warn('PASS PASS PASS PASS')
    log.info('PASS PASS PASS PASS')
    log.debug('FAIL FAIL FAIL FAIL')


if __name__ == '__main__':
    execute()

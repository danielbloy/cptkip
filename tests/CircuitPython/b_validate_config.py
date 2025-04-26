def execute():
    import cptkip.core.logging as log
    import cptkip.config.configuration as config
    log.critical('PASS')
    log.error('PASS')
    log.warn('PASS')
    log.info('FAIL FAIL FAIL FAIL')
    log.debug('FAIL FAIL FAIL FAIL')
    log.warn('PASS' if config.LOG_LEVEL == log.WARNING else 'FAIL FAIL FAIL FAIL')
    log.warn('PASS' if config.TEST_VALUE == 123.456 else 'FAIL FAIL FAIL FAIL')
    log.warn('PASS' if config.TEST_STRING == "Hello world!" else 'FAIL FAIL FAIL FAIL')
    log.warn('PASS' if config.DEBUG else 'FAIL FAIL FAIL FAIL')


if __name__ == '__main__':
    execute()

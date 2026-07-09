# This tests the logging works as expected. It uses printf() to duplicate
# all expected output.

def execute():
    import cptkip.core.logging as log

    # None of the FAIL strings should be output.
    original_log_level = log.LEVEL
    try:
        log.set_log_level(log.CRITICAL)
        log.error('FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL')
        log.warn('FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL')
        log.info('FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL')
        log.debug('FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL')

        log.set_log_level(log.ERROR)
        print('VALIDATE : Log level critical should be output')
        log.critical('Log level critical should be output')
        print('VALIDATE : Log level error should be output')
        log.error('Log level error should be output')
        log.warn('FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL')
        log.info('FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL')
        log.debug('FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL')

        log.set_log_level(log.WARNING)
        print('VALIDATE : Log level critical should be output')
        log.critical('Log level critical should be output')
        print('VALIDATE : Log level error should be output')
        log.error('Log level error should be output')
        print('VALIDATE : Log level error should be output')
        log.warn('Log level warning should be output')
        log.info('FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL')
        log.debug('FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL')

    finally:
        # Restore the configured log level
        log.set_log_level(original_log_level)


if __name__ == '__main__':
    execute()

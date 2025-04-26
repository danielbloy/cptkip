def execute():
    import cptkip.core.environment as environment
    import cptkip.core.logging as log

    # Output some information about the environment we are executing in.
    log.set_log_level(log.INFO)
    log.info(f'Is running in CI ................. : {environment.is_running_in_ci()}')
    log.info(f'Is running under test ............ : {environment.is_running_under_test()}')
    log.info(f'Is running on a microcontroller .. : {environment.is_running_on_microcontroller()}')
    log.info(f'Is running on a desktop .......... : {environment.is_running_on_desktop()}')
    log.info(f'Are pins available ............... : {environment.are_pins_available()}')

    # Set the log level to ERROR. None of the FAIL strings should be output.
    log.set_log_level(log.ERROR)
    log.critical('PASS')
    log.error('PASS')
    log.warn('FAIL FAIL FAIL FAIL')
    log.info('FAIL FAIL FAIL FAIL')
    log.debug('FAIL FAIL FAIL FAIL')

    log.set_log_level(log.INFO)
    log.critical('PASS')
    log.error('PASS')
    log.warn('PASS')
    log.info('PASS')
    log.debug('FAIL FAIL FAIL FAIL')


if __name__ == '__main__':
    execute()

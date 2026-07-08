def execute():
    import cptkip.core.environment as environment
    import cptkip.core.logging as log

    # Output some information about the environment we are executing in.
    log.set_log_level(log.CRITICAL)
    log.critical(f'Is running in CI ................. : {environment.is_running_in_ci()}')
    log.critical(f'Is running under test ............ : {environment.is_running_under_test()}')
    log.critical(f'Is running on a microcontroller .. : {environment.is_running_on_microcontroller()}')
    log.critical(f'Is running on a desktop .......... : {environment.is_running_on_desktop()}')
    log.critical(f'Are pins available ............... : {environment.are_pins_available()}')

    # None of the FAIL strings should be output.
    log.error('FAIL FAIL FAIL FAIL')
    log.warn('FAIL FAIL FAIL FAIL')
    log.info('FAIL FAIL FAIL FAIL')
    log.debug('FAIL FAIL FAIL FAIL')

    log.set_log_level(log.ERROR)
    log.critical('PASS')
    log.error('PASS')
    log.warn('FAIL FAIL FAIL FAIL')
    log.info('FAIL FAIL FAIL FAIL')
    log.debug('FAIL FAIL FAIL FAIL')


if __name__ == '__main__':
    execute()

def execute():
    import cptkip.core.environment as environment
    import cptkip.core.logging as log
    import cptkip.core.memory as memory

    memory.report_memory_usage()

    # Output some information about the environment we are executing in.
    log.set_log_level(log.INFO)
    log.info(f'Is running in CI ................. : {environment.is_running_in_ci()}')
    log.info(f'Is running under test ............ : {environment.is_running_under_test()}')
    log.info(f'Is running on a microcontroller .. : {environment.is_running_on_microcontroller()}')
    log.info(f'Is running on a desktop .......... : {environment.is_running_on_desktop()}')
    log.info(f'Are pins available ............... : {environment.are_pins_available()}')

    # Set the log level to ERROR. None of the ERROR strings should be output.
    log.set_log_level(log.ERROR)
    log.critical('This text should appear')
    log.error('This text should appear')
    log.warn('ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR')
    log.info('ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR')
    log.debug('ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR')

    log.set_log_level(log.INFO)
    log.critical('This text should appear')
    log.error('This text should appear')
    log.warn('This text should appear')
    log.info('This text should appear')
    log.debug('ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR')

    memory.report_memory_usage_and_free()


if __name__ == '__main__':
    execute()

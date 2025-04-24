import cptkip.core.environment as environment
import cptkip.core.log as log

log.set_log_level(log.INFO)
log.info(f'Is running in CI ................. : {environment.is_running_in_ci()}')
log.info(f'Is running under test ............ : {environment.is_running_under_test()}')
log.info(f'Is running on a microcontroller .. : {environment.is_running_on_microcontroller()}')
log.info(f'Is running on a desktop .......... : {environment.is_running_on_desktop()}')
log.info(f'Are pins available ............... : {environment.are_pins_available()}')

log.critical('This critical text will appear with log level info')
log.error('This error text will appear with log level info')
log.warn('This warning text will appear with log level info')
log.info('This information text will appear with log level info')
log.debug('This debug text will NOT appear with log level info')

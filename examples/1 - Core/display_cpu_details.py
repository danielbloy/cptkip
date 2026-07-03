#
# This example uses the logging framework to output CPU information.
#
import cptkip.core.logging as log
import cptkip.cpu.cpu as cpu

log.set_log_level(log.INFO)
log.info(cpu.info())

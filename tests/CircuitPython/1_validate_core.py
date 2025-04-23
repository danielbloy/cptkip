from cptkip.core.environment import is_running_on_microcontroller
from cptkip.core.log import set_log_level, info, INFO

set_log_level(INFO)
info(f'Is running on a microcontroller: {is_running_on_microcontroller()}')

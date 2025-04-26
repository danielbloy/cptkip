def execute():
    from cptkip.core.environment import is_running_on_microcontroller
    from cptkip.core.logging import set_log_level, info, INFO

    set_log_level(INFO)
    info(f'Is running on a microcontroller: {is_running_on_microcontroller()}')


if __name__ == '__main__':
    execute()

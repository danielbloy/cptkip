# This script simply outputs the various properties determined
# from the environment.

def execute():
    import cptkip.core.environment as environment

    # Output some information about the environment we are executing in.
    print(f'Is running in CI ................. : {environment.is_running_in_ci()}')
    print(f'Is running under test ............ : {environment.is_running_under_test()}')
    print(f'Is running on a microcontroller .. : {environment.is_running_on_microcontroller()}')
    print(f'Is running on a desktop .......... : {environment.is_running_on_desktop()}')
    print(f'Are pins available ............... : {environment.are_pins_available()}')

    # Validate that the returned values are either True or False.
    assert environment.is_running_in_ci() is True or environment.is_running_in_ci() is False
    assert environment.is_running_under_test() is True or environment.is_running_under_test() is False
    assert environment.is_running_on_microcontroller() is True or environment.is_running_on_microcontroller() is False
    assert environment.is_running_on_desktop() is True or environment.is_running_on_desktop() is False
    assert environment.are_pins_available() is True or environment.are_pins_available() is False


if __name__ == '__main__':
    execute()

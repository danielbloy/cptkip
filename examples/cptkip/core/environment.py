import cptkip.core.environment as environment

print('Is running in CI ................. : ', environment.is_running_in_ci())
print('Is running under test ............ : ', environment.is_running_under_test())
print('Is running on a microcontroller .. : ', environment.is_running_on_microcontroller())
print('Is running on a desktop .......... : ', environment.is_running_on_desktop())
print('Are pins available ............... : ', environment.are_pins_available())

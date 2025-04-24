import cptkip.core.environment as environment

print(f'Is running in CI ................. : {environment.is_running_in_ci()}')
print(f'Is running under test ............ : {environment.is_running_under_test()}')
print(f'Is running on a microcontroller .. : {environment.is_running_on_microcontroller()}')
print(f'Is running on a desktop .......... : {environment.is_running_on_desktop()}')
print(f'Are pins available ............... : {environment.are_pins_available()}')
print("")
environment.report()

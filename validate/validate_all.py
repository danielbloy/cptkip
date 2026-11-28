# This script runs all the validation tests. It is a convenient way to
# test a large subset of the functionality on a single device.
import validate.utils as utils
import validate.validate_animation as animation
import validate.validate_core as core
import validate.validate_device as device
import validate.validate_network as network
import validate.validate_pin as pin
import validate.validate_task as task

scripts = [core, task, pin, device, animation, network]


def execute() -> list:
    """
    Runs every validation module, then prints an overall summary. Returns the results.
    """
    results = []
    for script in scripts:
        results += utils.execute_modules(script.modules)

    print("\nOverall:")
    utils.print_summary(results)
    return results


if __name__ == '__main__':
    utils.exit_on_failure(execute())

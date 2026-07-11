import validate.task.basic_runner as basic_runner
import validate.task.memory_monitor as memory_monitor
import validate.utils as utils

modules = [basic_runner, memory_monitor]

if __name__ == '__main__':
    utils.execute_modules(modules)

import validate.task.basic_runner as basic_runner
import validate.task.basic_runner_async as basic_runner_async
import validate.task.memory_monitor as memory_monitor
import validate.task.memory_monitor_async as memory_monitor_async
import validate.task.periodic_task as periodic_task
import validate.task.periodic_task_async as periodic_task_async
import validate.utils as utils

modules = [basic_runner, memory_monitor, periodic_task, basic_runner_async, memory_monitor_async, periodic_task_async]

if __name__ == '__main__':
    utils.execute_modules(modules)

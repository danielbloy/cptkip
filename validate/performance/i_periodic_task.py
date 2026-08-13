from cptkip.task.periodic_task import create
from validate.performance.task_runner import execute, continue_func


def task() -> None:
    print('task')


periodic_task = create(task, frequency=3, continue_func=continue_func, initial_delay=1)

execute(periodic_task, False)
execute(periodic_task, True)

# Load the next file
from validate.performance.script_runner import execute_next_script

execute_next_script(__file__)

import cptkip.task.periodic_task_async as periodic_task
from validate.performance.task_runner_async import execute, continue_func


async def task() -> None:
    print('task')


periodic_task = periodic_task.create(
    task, frequency=3, continue_func=continue_func, initial_delay=1)

execute(periodic_task, False)
execute(periodic_task, True)

# Load the next file
from validate.performance.script_runner import execute_next_script

execute_next_script(__file__)

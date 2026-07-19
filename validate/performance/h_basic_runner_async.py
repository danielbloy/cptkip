from validate.performance.task_runner_async import execute


async def task():
    pass


execute(task, False)
execute(task, True)

# Load the next file
from validate.performance.script_runner import execute_next_script

execute_next_script(__file__)

from cptkip.task.triggered_task_async import create
from validate.performance.task_runner_async import execute, continue_func


async def begin() -> None:
    print("begin")


async def end() -> None:
    print("end")


task = create(lambda: True, 0.5, begin=begin, end=end, continue_func=continue_func)

execute(task, False)
execute(task, True)

# Load the next file
from validate.performance.script_runner import execute_next_script

execute_next_script(__file__)

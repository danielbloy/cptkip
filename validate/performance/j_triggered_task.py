from cptkip.task.triggered_task import create
from validate.performance.task_runner import execute, continue_func


def begin() -> None:
    print("begin")


def end() -> None:
    print("end")


task = create(lambda: True, 0.5, begin=begin, end=end, continue_func=continue_func)

execute(task, False)
execute(task, True)

# Load the next file
from validate.performance.script_runner import execute_next_script

execute_next_script(__file__)

from validate.performance.task_runner import execute


def task():
    pass


execute(task, False, use_reliable_runner=True)
execute(task, True, use_reliable_runner=True)

# Load the next file
from validate.performance.script_runner import execute_next_script

execute_next_script(__file__)

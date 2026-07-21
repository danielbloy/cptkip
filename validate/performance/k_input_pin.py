from validate.performance.task_runner import execute


def task():
    pass
    # TODO: Implement


execute(task, False)
execute(task, True)

# Load the next file
from validate.performance.script_runner import execute_next_script

execute_next_script(__file__)

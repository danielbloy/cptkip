from validate.performance.task_runner import execute

execute(lambda: None, False)
execute(lambda: None, True)

# Load the next file
from validate.performance.script_runner import execute_next_script

execute_next_script(__file__)

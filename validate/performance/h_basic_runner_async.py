from validate.performance.task_runner_async import execute
from validate.performance.task_settings import runtime


async def task():
    global cycles
    cycles += 1


cycles = 0
execute(task, False)
print(f"CYCLES ..... : {((cycles / runtime) // 100) / 10:,.1f} K/s")

cycles = 0
execute(task, True)
print(f"CYCLES ..... : {((cycles / runtime) // 100) / 10:,.1f} K/s")

# Load the next file
from validate.performance.script_runner import execute_next_script

execute_next_script(__file__)

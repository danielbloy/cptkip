from cptkip.task.triggered_events_task_async import create
from validate.performance.task_runner_async import execute, continue_func


async def begin() -> None:
    print("begin")


async def callback(value) -> None:
    print("callback", value)


async def end() -> None:
    print("end")


task = create(
    lambda: True,
    events=[
        (0.1, "1"),
        (0.2, "2"),
        (0.3, "3"),
        (0.4, "4"),
        (0.5, "5")
    ],
    begin=begin,
    callback=callback,
    end=end,
    continue_func=continue_func)

execute(task, False)
execute(task, True)

# Load the next file
from validate.performance.script_runner import execute_next_script

execute_next_script(__file__)

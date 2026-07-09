"""
This module contains all the setup and instrumentation code to assist executing
the on device validation and profiling. The only function you should need to use
is execute() as it bootstraps everything else.
"""
import traceback

import cptkip.config.configuration as config
import cptkip.core.logging as log
import cptkip.core.memory as memory
from cptkip.core.environment import is_running_on_desktop

# These are not available in CircuitPython.
if is_running_on_desktop():
    pass

PROFILE = False
PROFILE_TOP = 10

if hasattr(config, 'PROFILE'):
    PROFILE = config.PROFILE

if hasattr(config, 'PROFILE_TOP'):
    PROFILE_TOP = config.PROFILE_TOP


def execute_modules(modules: list[object]):
    """
    Executes each of the modules in turn. This is expected to be used only by the
    top level validate scripts.
    """
    for module in modules:
        try:
            log.critical("Executing module {}".format(module))
            memory.reset_memory_usage()
            memory.report_memory_usage_and_free()
            __start_profiling()
            module.execute()
            __end_profiling()
            memory.report_memory_usage_and_free()

            del module

        except MemoryError as err:
            log.critical("Memory Error")
            traceback.print_exception(err)


def __start_profiling():
    # See: https://docs.python.org/3/library/tracemalloc.html
    # And: https://stackoverflow.com/questions/552744/how-do-i-profile-memory-usage-in-python
    if is_running_on_desktop() and PROFILE:
        import tracemalloc
        tracemalloc.start()


def __end_profiling(top: int = PROFILE_TOP):
    if is_running_on_desktop() and PROFILE:
        import tracemalloc
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')
        print(f"[ Top {top} ]")
        for stat in top_stats[:top]:
            print(stat)

import a_validate_core
import b_validate_config
import c_validate_cpu

import cptkip.core.memory as memory

modules = [a_validate_core, b_validate_config, c_validate_cpu]


def execute():
    for module in modules:
        memory.report_memory_usage()
        module.execute()
        memory.report_memory_usage_and_free()


if __name__ == '__main__':
    execute()

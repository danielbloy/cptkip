import cptkip.core.logging as log
import cptkip.core.memory as memory
import validate.validate_a_core as a
import validate.validate_b_config as b
import validate.validate_c_cpu as c
import validate.validate_d_tasks as d
import validate.validate_e_pins as e

modules = [a, b, c, d, e]


def execute():
    memory.report_memory_usage()
    for module in modules:
        log.critical("Executing module {}".format(module))
        module.execute()
        memory.report_memory_usage_and_free()


if __name__ == '__main__':
    execute()

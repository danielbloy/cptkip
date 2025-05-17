import cptkip.core.logging as log
import cptkip.core.memory as memory
import tests.validate.validate_a_core as a
import tests.validate.validate_b_config as b
import tests.validate.validate_c_cpu as c
import tests.validate.validate_d_task as d
import tests.validate.validate_e_pin as e
import tests.validate.validate_f_device as f
import tests.validate.validate_g_animation as g

modules = [a, b, c, d, e, f, g]


def execute():
    memory.report_memory_usage()
    for module in modules:
        log.critical("Executing module {}".format(module))
        module.execute()
        memory.report_memory_usage_and_free()
        del module


if __name__ == '__main__':
    execute()

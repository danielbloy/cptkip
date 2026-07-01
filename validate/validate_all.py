import cptkip.core.logging as log
import cptkip.core.memory as memory
import validate.validate_a_core as a
import validate.validate_b_config as b
import validate.validate_c_cpu as c
import validate.validate_d_task as d
import validate.validate_d_task_async as da
import validate.validate_e_pin as e
import validate.validate_f_device as f
import validate.validate_g_animation as g

modules = [a, b, c, d, da, e, f, g]


def execute():
    memory.report_memory_usage()
    for module in modules:
        log.critical("Executing module {}".format(module))
        module.execute()
        memory.report_memory_usage_and_free()
        del module


if __name__ == '__main__':
    execute()

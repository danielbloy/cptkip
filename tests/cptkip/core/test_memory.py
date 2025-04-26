import cptkip.core.memory as memory


class TestMemory:

    def test_report_memory_usage(self):
        """
        Simply tests there is no error when calling report_memory_usage()
        """
        memory.report_memory_usage()
        memory.report_memory_usage("Message")

    def test_report_memory_usage_and_free(self):
        """
        Simply tests there is no error when calling report_memory_usage_and_free()
        """
        memory.report_memory_usage_and_free()
        memory.report_memory_usage_and_free("Message")

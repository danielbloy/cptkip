import cptkip.core.memory as memory


class TestMemory:

    def test_reset_memory_usage(self):
        """
        Validates there is no error when calling reset and it does actually
        reset the counters.
        """
        memory.reset_memory_usage()
        assert memory.peak_used_ram == 0
        assert memory.used_ram == 0
        assert memory.free_ram == 0
        assert memory.total_ram == 0

        memory.sample_memory_usage()

        memory.reset_memory_usage()
        assert memory.peak_used_ram == 0
        assert memory.used_ram == 0
        assert memory.free_ram == 0
        assert memory.total_ram == 0

    def test_sample_memory_usage(self):
        """
        Validates that sample_memory_usage() collects statistics. We do not validate
        those statistics though.
        """
        memory.reset_memory_usage()

        memory.sample_memory_usage()
        assert memory.peak_used_ram != 0
        assert memory.used_ram != 0
        assert memory.free_ram != 0
        assert memory.total_ram != 0

        # Call multiple times to check for errors.
        memory.sample_memory_usage()
        memory.sample_memory_usage()
        memory.sample_memory_usage()

    def test_report_memory_usage(self):
        """
        Simply tests there is no error when calling report_memory_usage()
        """
        memory.report_memory_usage()

    def test_report_memory_usage_and_free(self):
        """
        Simply tests there is no error when calling report_memory_usage_and_free()
        """
        memory.report_memory_usage_and_free()

    def test_running_all_memory_functions(self):
        """
        Simple validation test that runs all the functions in a sequence.
        """
        memory.reset_memory_usage()

        memory.sample_memory_usage()
        memory.sample_memory_usage()
        memory.sample_memory_usage()

        memory.report_memory_usage()

        memory.sample_memory_usage()
        memory.sample_memory_usage()
        memory.sample_memory_usage()

        memory.report_memory_usage_and_free()

        memory.reset_memory_usage()

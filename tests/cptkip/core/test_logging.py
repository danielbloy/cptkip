import cptkip.core.logging as log


class TestLogging:

    def test_set_log_level(self):
        """
        Simply tests there is no error when calling set_log_level()
        """
        log.set_log_level(log.DEBUG)
        log.set_log_level(log.WARNING)

    def test_stacktrace(self):
        """
        Simply tests there is no error when calling stacktrace()
        """
        try:
            raise Exception("raise error")
        except Exception as e:
            log.stacktrace(e)

    def test_log(self):
        """
        Simply tests there is no error when calling log()
        """
        log.log(log.INFO, "LOG message")

    def test_debug(self):
        """
        Simply tests there is no error when calling debug()
        """
        log.debug("DEBUG message")

    def test_info(self):
        """
        Simply tests there is no error when calling info()
        """
        log.info("INFO message")

    def test_warn(self):
        """
        Simply tests there is no error when calling warn()
        """
        log.warn("WARN message")

    def test_error(self):
        """
        Simply tests there is no error when calling error()
        """
        log.error("ERROR message")

    def test_critical(self):
        """
        Simply tests there is no error when calling critical()
        """
        log.critical("CRITICAL message")

    def test_log_prefix_per_level(self, capsys):
        """
        Validates that log() selects the correct prefix for each level.
        """
        log.set_log_level(log.DEBUG)
        try:
            for level, prefix in (
                    (log.CRITICAL, log.C),
                    (log.ERROR, log.E),
                    (log.WARNING, log.W),
                    (log.INFO, log.I),
                    (log.DEBUG, log.D)):
                log.log(level, "message")
                out = capsys.readouterr().out
                assert out.startswith(prefix)
        finally:
            log.set_log_level(log.WARNING)

    def test_log_level_filtering(self, capsys):
        """
        Validates that messages more verbose than the current level are
        suppressed and messages at or below it are printed.
        """
        log.set_log_level(log.WARNING)
        try:
            log.info("suppressed")
            assert capsys.readouterr().out == ""

            log.warn("shown")
            assert capsys.readouterr().out != ""

            log.critical("shown")
            assert capsys.readouterr().out != ""
        finally:
            log.set_log_level(log.WARNING)

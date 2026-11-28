import cptkip.core.environment as environment


class TestEnvironment:
    def test_report(self):
        """
        Simply tests there is no error calling the report method.
        """
        environment.report()

    def test_controller_or_desktop(self):
        """
        Just a simple test to make sure we are not returning a microcontroller and desktop environment
        """
        assert environment.is_running_on_desktop() != environment.is_running_on_microcontroller()

    def test_is_running_in_test(self):
        """
        Simple test for when running under test.
        """
        assert environment.is_running_under_test()

    def test_is_running_in_ci(self):
        """
        Simple test for when running in CI.
        """
        if environment.is_running_in_ci():
            assert not environment.is_running_on_microcontroller()
            assert environment.is_running_on_desktop()
            assert not environment.are_pins_available()


_CI_VARIABLES = ("CI", "TRAVIS", "CIRCLECI", "GITLAB_CI", "GITHUB_ACTIONS", "GITHUB_RUN_ID")
_BLINKA_VARIABLES = ("BLINKA_U2IF", "BLINKA_FT232H", "BLINKA_FT2232H", "BLINKA_FT4232H",
                     "BLINKA_MCP2221", "BLINKA_GREATFET", "CPTKIP_PINS")


def _reload_with(monkeypatch, env: dict, platform: str = None):
    """
    Re-evaluates cptkip.core.environment with the given environment variables (and
    optionally sys.platform). The environment module computes everything at import
    time, so it has to be reloaded to exercise its branches in-process.
    """
    import importlib
    import sys
    for name in _CI_VARIABLES + _BLINKA_VARIABLES:
        monkeypatch.delenv(name, raising=False)
    for name, value in env.items():
        monkeypatch.setenv(name, value)
    if platform:
        monkeypatch.setattr(sys, "platform", platform)
    importlib.reload(environment)


class TestEnvironmentBranches:
    """
    These reload the environment module; the original state is restored afterwards
    by undoing the patches and reloading again.
    """

    def teardown_method(self):
        import importlib
        importlib.reload(environment)

    def test_ci_forces_linux_without_pins(self, monkeypatch, capsys):
        _reload_with(monkeypatch, {"GITHUB_ACTIONS": "true", "BLINKA_U2IF": "1"}, platform="win32")
        assert environment.is_running_in_ci()
        assert environment.is_running_under_test()
        assert environment.is_running_on_linux()
        assert not environment.is_running_on_windows()
        assert not environment.is_running_on_mac()
        assert not environment.are_pins_available()

        environment.report()
        assert "Running in CI" in capsys.readouterr().out
        monkeypatch.undo()

    def test_platform_accessors(self, monkeypatch):
        for platform, linux, mac, windows in [("linux", True, False, False),
                                              ("darwin", False, True, False),
                                              ("win32", False, False, True)]:
            _reload_with(monkeypatch, {}, platform=platform)
            assert not environment.is_running_in_ci()
            assert environment.is_running_on_linux() == linux
            assert environment.is_running_on_mac() == mac
            assert environment.is_running_on_windows() == windows
            assert environment.is_running_on_desktop()
        monkeypatch.undo()

    def test_blinka_environment_variables_enable_pins(self, monkeypatch):
        import sys
        import types
        monkeypatch.setitem(sys.modules, "board", types.ModuleType("board"))
        for name in _BLINKA_VARIABLES:
            _reload_with(monkeypatch, {name: "1"})
            assert environment.are_pins_available(), name

        _reload_with(monkeypatch, {})
        assert not environment.are_pins_available()
        monkeypatch.undo()

    def test_blinka_board_errors_mean_no_pins(self, monkeypatch):
        """
        Blinka raises errors other than ImportError when no supported board is found;
        these must be treated as "no pins" rather than crashing on import.
        """
        import builtins
        real_import = builtins.__import__

        def failing_import(name, *args, **kwargs):
            if name == "board":
                raise NotImplementedError("Board not supported")
            return real_import(name, *args, **kwargs)

        monkeypatch.setattr(builtins, "__import__", failing_import)
        _reload_with(monkeypatch, {"BLINKA_FT232H": "1"})
        assert not environment.are_pins_available()
        monkeypatch.undo()

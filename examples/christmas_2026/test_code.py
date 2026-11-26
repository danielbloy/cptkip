import sys
from pathlib import Path

#
_FIXTURE_DIR = str(Path(__file__).parent)
_MODULES_TO_RELOAD = ("config", "device", "cptkip.config.configuration")


# noinspection unused-imports
class TestCode:
    def test_code(self, monkeypatch):
        monkeypatch.syspath_prepend(_FIXTURE_DIR)
        for name in _MODULES_TO_RELOAD:
            monkeypatch.delitem(sys.modules, name, raising=False)

        import cptkip.config.configuration as configuration

        import examples.christmas_2026.code as code

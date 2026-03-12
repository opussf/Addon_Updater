import logging
# import pytest
from addon_updater import Curseforge


class TestCurseforge:
    def test_default_logger(self):
        """Logger is named after Curseforge, not AddonData."""
        obj = Curseforge(cfID=12345)
        assert obj.logger.name == "addon_updater"

    def test_cfid_stored(self):
        """cfID is stored on the object."""
        obj = Curseforge(cfID=12345)
        assert obj.cfID == 12345

    def test_custom_logger(self):
        """Custom logger is passed through to parent."""
        custom_logger = logging.getLogger("my_logger")
        obj = Curseforge(cfID=12345, logger=custom_logger)
        assert obj.logger.name == "my_logger"

    def test_inherits_data_storage(self):
        """Curseforge inherits DataStorage from AddonData."""
        from addon_updater import DataStorage
        obj = Curseforge(cfID=12345)
        assert isinstance(obj.cursor, DataStorage)

    def test_different_ids(self):
        """Two instances can have different cfIDs."""
        obj1 = Curseforge(cfID=111)
        obj2 = Curseforge(cfID=222)
        assert obj1.cfID != obj2.cfID

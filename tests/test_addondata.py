import logging
# import pytest
from addon_updater import AddonData


class TestAddonData:
    def test_default_logger(self):
        """Logger is created from class name when none provided."""
        obj = AddonData()
        assert obj.logger.name == "addon_updater"

    def test_custom_logger(self):
        """Custom logger is used when provided."""
        custom_logger = logging.getLogger("my_logger")
        obj = AddonData(logger=custom_logger)
        assert obj.logger.name == "my_logger"

    def test_data_storage_initialized(self):
        """DataStorage is created on init."""
        obj = AddonData()
        assert obj.cursor is not None

    def test_data_storage_type(self):
        """cursor is a DataStorage instance."""
        from addon_updater import DataStorage
        obj = AddonData()
        assert isinstance(obj.cursor, DataStorage)

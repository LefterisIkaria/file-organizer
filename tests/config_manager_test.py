import os
import unittest
from src.models.category import Category
from src.models.schedule.schedule import Schedule
from src.models.schedule.schedule_enums import *
from src.models.config import Config
from src.models.config_manager import ConfigAlreadyExistsError, ConfigError, ConfigManager, ConfigNotFoundError

def get_config_path() -> str:
    user_home = os.path.expanduser("~")
    app_dir = os.path.join(user_home, ".file-organizer")
    config_path = os.path.join(app_dir, "app.json")

    return config_path


class TestConfigManager(unittest.TestCase):


    def test_loading_configs(self):

        # 1. Existence of Configuration File
        self.assertTrue(os.path.exists(get_config_path()), "Config file does not exist")

        config_manager = ConfigManager("config/mock.config.json")
        configs = config_manager.get_configs()

        # 2. Type of Config Data
        self.assertIsInstance(configs, list, "Config data is not a list")

        # 3. Non-Emptiness
        self.assertTrue(configs, "Config data list is empty")

        # 4. Type of Each Config
        for config in configs:
            self.assertIsInstance(config, Config, "Item in config list is not an instance of Config")

        # 5. Valid Config Properties
        # Example: if each Config object has a 'name' property that should be a string:
        for config in configs:
            self.assertIsInstance(config.dir, str, "Config 'dir' property is not a string")
            self.assertTrue(config.categories, "Config categories don't exists")
            self.assertIsInstance(config.schedule, Schedule, "Config schedule is not a 'Schedule' object")



    def test_finding_config(self):
         config_manager = ConfigManager("config/mock.config.json")
         config = config_manager.get_config("/path/to/dir")

         self.assertIsInstance(config, Config, "Not a Config instance")

    
    def test_create_new_config(self):
        config_manager = ConfigManager("config/mock.config.json")

        new_config = Config(
            dir="/path/to/new/dir",
            categories=set([
                Category(name="New Category 1", extensions=set([".one", ".two"]), categorize_extensions=True),
                Category(name="New Category 2", extensions=set([".three", ".four"]), categorize_extensions=True)
            ]),
            schedule=Schedule(type=ScheduleType.DAY, interval=2, time="00:00"),
            active=False
        )

       # 1. No Exceptions
        try:
            config_manager.create_config(new_config)

            # Get the new created config
            created_config = config_manager.get_config("/path/to/new/dir")
            # 2. Config Existence
            self.assertIsNotNone(created_config, "Config was not created")

            # 3. Config Properties
            self.assertEqual(created_config.dir, new_config.dir, "Directory paths do not match")
            self.assertEqual(created_config.schedule, new_config.schedule, "Schedules do not match")
            self.assertEqual(created_config.active, new_config.active, "Active statuses do not match")

            # 4. Assert that I can't recreate the same config
            config_manager.create_config(created_config)
        
        except ConfigAlreadyExistsError as e:
            self.assertTrue(True, "Expected ConfigAlreadyExistsError was not raised")
        except Exception as e:
            self.assertTrue(False, "Exception occurred while creating config")
        
    

    def test_update_config(self):

        config_manager = ConfigManager("config/mock.config.json")
        config = config_manager.get_config("/path/to/new/dir")
        
        # 1. Update active state
        config.active = not config.active
        try:
            config_manager.update_config(config)
        except ConfigError as e:
            self.assertFalse(e, "ConfigError was raised")

        # 2. Rename a category
        try:
            config_manager.rename_category(config, category_name="New Category 2", new_category_name="XDD")
        except ConfigError as e:
            self.assertTrue(e, "ConfigError expected")
        except Exception as e:
            self.assertFalse(e, "Exception was raised when renaming a category")

        # 3. Update configs schedule
        try:
            config_manager.update_config_schedule(config, Schedule(type=ScheduleType.MINUTE, interval=10))
        except Exception as e:
            self.assertFalse(e, "Exception was raised when renaming a category")

    
    def test_delete_config(self):

        config_manager = ConfigManager("config/mock.config.json")
        
        try:
            config = config_manager.get_config("/path/to/delete/dir")
            config_manager.delete_config(config)
        except ConfigNotFoundError as e:
            self.assertTrue(e, "ConfigNotFound Error expected")
        except Exception as e:
            self.assertTrue(False, "Error while deleting the config")
        




if __name__ == '__main__':
    unittest.main()
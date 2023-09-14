import json
import os
import shutil
from unittest import TestCase
from models import Category, Config, Schedule
from config_service import ConfigFileService


MOCK_CONFIGS = [
    {
        "active": True,
        "directory": "/home/test1",
        "categories": [
            {
                "name": "Documents",
                "extensions": [".doc", ".pdf"],
                "categorize_extensions": True
            },
            {
                "name": "Code",
                "extensions": [".py", ".c", ".cpp"],
                "categorize_extensions": False
            }
        ],
        "schedule": {
            "active": True,
            "type": "MINUTE",
            "interval": 2
        }
    },
    {
        "active": False,
        "directory": "/home/test2",
        "categories": [
            {
                "name": "Music",
                "extensions": [".mp3"],
                "categorize_extensions": False
            },
            {
                "name": "Video",
                "extensions": [".mp4", ".ova"],
                "categorize_extensions": False
            }
        ],
        "schedule": {
            "active": True,
            "type": "HOUR",
            "interval": 5
        }
    }
]


class TestConfigService(TestCase):


    def _create_and_populate_mock_directory(self):
        """ Create a mock directory and two json mock files"""    
        os.makedirs(self.mock_dir, exist_ok=True)

        for config in MOCK_CONFIGS:
            config_filepath = os.path.join(self.mock_dir, f"{config['directory'].replace('/', '_')}.json")
            with open(config_filepath, 'w') as f:
                json.dump(config, f)


    def _assert_configs_equals(self, actual: Config, expected: Config):
        """ Assert that two configs are equal"""
        self.assertEqual(actual.directory, expected.directory)
        self.assertEqual(actual.active, expected.active)
        self.assertEqual(actual.schedule, expected.schedule)
        
        # Comparing categories
        self.assertEqual(len(actual.categories), len(expected.categories))
        for actual_category, expected_category in zip(actual.categories, expected.categories):
            self.assertEqual(actual_category.name, expected_category.name)
            self.assertEqual(actual_category.extensions, expected_category.extensions)
            self.assertEqual(actual_category.categorize_extensions, expected_category.categorize_extensions)


    def setUp(self) -> None:
        self.mock_dir = "mock_dir"
        
        # Create the mock directory
        self._create_and_populate_mock_directory()
        
        # The ConfigService before each test
        self.service = ConfigFileService(self.mock_dir)

    
    def tearDown(self) -> None:
        # Clean up by deleting the temporary directory after tests are done
        shutil.rmtree(self.mock_dir)
   
    

    def test_get_configs(self):
        # 1. Retrive configs
        all_configs = self.service.get_configs()

        # 2. Number of configs
        self.assertEqual(len(all_configs), len(MOCK_CONFIGS), "Number of configs mismatch")

        # 3. Equality
        for retrieved_config, mock_config in zip(all_configs, MOCK_CONFIGS):
            self._assert_configs_equals(actual=retrieved_config, expected=Config.from_dict(mock_config))
    

    def test_get_config(self):
        
        config1 = self.service.get_config(directory="/home/test1")
        config2 = self.service.get_config(directory="/home/test2")

        # Is the same as the mock
        self._assert_configs_equals(actual=config1, expected=Config.from_dict(MOCK_CONFIGS[0]))
        self._assert_configs_equals(actual=config2, expected=Config.from_dict(MOCK_CONFIGS[1]))
    

    def test_create_configs(self):
        
        # 1. Config to create
        new_config = Config(
            active=True,
            directory="/home/new",
            categories=[Category(name="NEW CATEGORY", extensions=[".new"], categorize_extensions=True)],
            schedule=Schedule(active=True, type="HOUR", interval=10)
        )

        # 2. Create the config
        self.service.create_config(new_config)
        
        # 4. Check if filepath created
        created_filepath = os.path.join(self.mock_dir, f"{new_config.dir_to_filename()}.json")
        self.assertTrue(os.path.exists(created_filepath), "The json file was not created")
    

    def test_update_config(self):
        # 1. Fetch the first config
        config = self.service.get_config(directory="/home/test1")

        # 2. Make changes
        config.active = False
        config.categories = [Category(name="Another", extensions=[".xd", ".xdd"], categorize_extensions=False)]
        config.schedule = Schedule(active=False, type="HOUR", interval=10)

        # 3. Update the config
        self.service.update_config(directory=config.directory, config=config)

        # 4. Fetch updated config
        updated_config = self.service.get_config(directory=config.directory)

        # 5. Assert that is the updated
        self._assert_configs_equals(actual=updated_config, expected=config)
    

    def test_delete_config(self):
        
        # 1. fetch the config and check if it exists
        exists_config = self.service.get_config(directory="/home/test2")
        self.assertIsNotNone(exists_config)
        
        # 2. delete the config
        self.service.delete_config(directory="/home/test2")

        # 3. Verify that the config no longer exists
        not_exists_config = self.service.get_config("/home/test2")
        self.assertIsNone(not_exists_config)

        # 4. Ensure that the json file is removed
        expected_filepath = os.path.join(self.mock_dir, f"{exists_config.dir_to_filename()}.json")
        self.assertFalse(os.path.exists(expected_filepath))
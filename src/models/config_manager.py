import logging
import json
from src.models.schedule.schedule import Schedule
from src.models.category import Category
from src.models.config import Config


class ConfigError(Exception):
    pass

class ConfigAlreadyExistsError(ConfigError):
    pass

class ConfigNotFoundError(ConfigError):
    pass


class ConfigManager:
    
    def __init__(self, config_path: str) -> None:
        self.config_path = config_path
        self.configs: dict[str, Config] = {}
        self._load_data()


    def _load_data(self) -> None:
        try:
            with open(self.config_path, "r") as f:
                json_data = json.load(f)
            self.configs = {dir: Config.from_dict(dir, data) for dir, data in json_data.items()}
        except FileNotFoundError:
            logging.error(f"File not found on path: {self.config_path}")
            self.configs = {}
        except json.JSONDecodeError:
            logging.error(f"Error decoding JSON file: {self.config_path}")
            raise ConfigError("Invalid JSON format")


    def _save_data(self) -> None:
        try:
            with open(self.config_path, "w") as f:
                json.dump({dir: config.to_dict() for dir, config in self.configs.items()}, f, indent=4)
        except Exception as e:
            logging.error(f"Error saving to file: {e}")
            raise ConfigError("Could not save configuration")


    def get_configs(self) -> list[Config]:
        return list(self.configs.values())


    def get_config(self, dir: str) -> Config:
        if dir not in self.configs:
            raise ConfigNotFoundError(f"Config with dir payh {dir} not found")
        return self.configs.get(dir)


    def create_config(self, config: Config) -> None:
        if config.dir in self.configs:
            raise ConfigAlreadyExistsError("Config already exists")
        self.configs[config.dir] = config
        self._save_data()


    def update_config(self, config: Config) -> None:
        if config.dir not in self.configs:
            raise ConfigNotFoundError(f"Config with key {config.dir} not found")
        self.configs[config.dir] = config
        self._save_data()


    def delete_config(self, config: Config) -> None:
        if config.dir not in self.configs:
            raise ConfigNotFoundError(f"Config with key {config.dir} not found")
        del self.configs[config.dir]
        self._save_data()
    

    def config_exists(self, dir: str):
        return dir in self.configs
    

    def update_config_schedule(self, config: Config, schedule: Schedule) -> None:
        """
        Update the Schedule of the given config

        :param config: The configuration object
        "param schedule: the new schedule
        """

        # Check if the directory path exists in the configs
        if config.dir not in self.configs:
            raise ConfigNotFoundError(f"Config with dir path {config.dir} not found")
        
        config.schedule = schedule

        self._save_data()


    def rename_category(self, config: Config, category_name: str, new_category_name: str) -> None:
        """
        Rename a category for a given configuration.

        :param config: The configuration object.
        :param category_name: The old category name.
        :param new_category_name: The new category name.
        """

        # Check if the directory path exists in the configs
        if config.dir not in self.configs:
            raise ConfigNotFoundError(f"Config with dir path {config.dir} not found")

        # Check if the category exists
        found_category =  next((category for category in config.categories if category.name == category_name), None)
        if not found_category:
            raise ConfigError(f"Category '{category_name}' not found for directory '{dir}'")

        # Remove the old category from the set
        config.categories.remove(found_category)

        # Create a new category with the new name and the same data as the old category
        updated_category = Category(
            name=new_category_name, 
            extensions=found_category.extensions, 
            categorize_extensions=found_category.categorize_extensions
        )

        # Add the new category to the set
        config.categories.add(updated_category)

        # Save the updated data
        self._save_data()
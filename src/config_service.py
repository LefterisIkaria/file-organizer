from abc import ABC, abstractmethod
import json
import os
import logging
from typing import Optional
from models import Config

LOG = logging.getLogger(__name__)

class IConfigService(ABC):

    @abstractmethod
    def get_configs(self) -> list[Config]:
        """Returns the list of available Configs."""
        pass

    @abstractmethod
    def get_config(self, directory: str) -> Optional[Config]:
        """Load a specific Config by its name."""
        pass

    @abstractmethod
    def create_config(self, config: Config) -> None:
        """Save a Config object."""
        pass

    @abstractmethod
    def delete_config(self, directory: str) -> None:
        """Delete a Config."""
        pass

    @abstractmethod
    def update_config(self, directory: Config, config: Config) -> None:
        """Update an existing Config."""
        pass



class ConfigFileService(IConfigService):
    

    def __init__(self, configs_directory: str) -> None:
        if not os.path.exists(configs_directory):
            raise Exception("Configs directory don't exists")
        
        self.configs_directory = configs_directory
        self.configs_map: dict[str, tuple[Config, str]] = dict()
        self._load_configs()


    def _load_configs(self) -> None:
        """Loads the configs from the configs directory"""
        for file in os.listdir(self.configs_directory):
            if file.endswith('.json'):
                config_path = os.path.join(self.configs_directory, file)
                with open(config_path, 'r') as f:
                    data = json.load(f)
                    config = Config.from_dict(data)

                    # Validate config
                    if not config.is_valid():
                        LOG.warning(f"Config {file} is invalid and will be skipped.")
                        continue

                    self.configs_map[config.directory] = (config, file)


    def get_configs(self) -> list[Config]:
        """Returns the list of available Configs."""
        return sorted([config_tuple[0] for config_tuple in self.configs_map.values()], key=lambda config: config.directory)

    def get_config(self, directory: str) -> Optional[Config]:
        """Load a specific Config by its name."""
        config_tuple = self.configs_map.get(directory)
        return config_tuple[0] if config_tuple else None

    def create_config(self, config: Config) -> None:
        """Save a Config object."""
        if config.directory in self.configs_map:
            raise ValueError("Config for this directory already exists")
        filename = f"{config.dir_to_filename()}.json"
        file_path = os.path.join(self.configs_directory, filename)
        with open(file_path, 'w') as f:
            json.dump(config.to_dict(), f)
        self.configs_map[config.directory] = (config, filename)

    def delete_config(self, directory: str) -> None:
        """Delete a Config."""
        config_tuple = self.configs_map.get(directory)
        if not config_tuple:
            raise ValueError("Config not found")
        filename = config_tuple[1]
        file_path = os.path.join(self.configs_directory, filename)
        os.remove(file_path)
        del self.configs_map[directory]

    def update_config(self, directory: Config, config: Config) -> None:
        """Update an existing Config."""
        config_tuple = self.configs_map.get(directory)
        if not config_tuple:
            raise ValueError("Config not found")
        filename = config_tuple[1]
        file_path = os.path.join(self.configs_directory, filename)
        with open(file_path, 'w') as f:
            json.dump(config.to_dict(), f)
        self.configs_map[directory] = (config, filename)
import os
import logging

from src.filter_chain.core import *
from src.models.config import Config

logger = logging.getLogger(__name__)


class DirectoryExistenceFilter(Filter):
    """
    Ensures that the target directory exists.
    """

    priority: int = 0

    def do_filter(self, config: Config, chain: FilterChain) -> FilterResponse:
        logger.debug(f"Checking existence of directory: {config.dir}")
        if not os.path.exists(config.dir):
            logger.error(f"Directory does not exist: {config.dir}")
            return FilterResponse("failure", config, f"Directory {config.dir} does not exist.")

        return chain.next(config)


class DirectoryCriticalFilter(Filter):
    """
    Checks if the directory is a system or critical directory.
    """

    priority: int = 1

    def do_filter(self, config: Config, chain: FilterChain) -> FilterResponse:
        logger.debug(f"Checking if directory is critical: {config.dir}")
        if self._is_critical_directory(config.dir):
            logger.error(f"Cannot process a critical directory: {config.dir}")
            return FilterResponse("failure", config, f"Directory {config.dir} is a critical directory and cannot be processed.")

        return chain.next(config)

    def _is_critical_directory(self, path: str):

        # A basic list of most common os critical paths
        CRITICAL_DIRS = [
            "/bin", "/sbin", "/etc", "/lib", "/usr",
            "/var", "/proc", "/sys", "/dev", "/root",
            "/run", "/boot",
            "C:\\Windows", "C:\\Windows\\System32", "C:\\Program Files",
            "C:\\Program Files (x86)", "C:\\Users\\Default",
            "/Applications", "/Library", "/System", "/Users", "/private", "/usr/local"
        ]

        # Check if path starts with one of the critical directories
        for dir in CRITICAL_DIRS:
            # Ensure it's a subdirectory, not just a prefix
            if path.startswith(dir + os.path.sep):
                return True

        return False


class DirectoryPermissionsFilter(Filter):
    """
    Checks for sufficient permissions to read and write to the directory.
    """

    priority: int = 1

    def do_filter(self, config: Config, chain: FilterChain) -> FilterResponse:
        logger.debug(f"Checking permissions for directory: {config.dir}")
        if not os.access(config.dir, os.R_OK | os.W_OK):
            logger.error(
                f"Insufficient permissions for directory: {config.dir}")
            return FilterResponse("failure", config, f"Insufficient permissions to read or write to the directory {config.dir}.")

        return chain.next(config)

import logging
from dataclasses import dataclass

LOG = logging.getLogger(__name__)

@dataclass
class Category:
    name: str
    extensions: set[str] 
    categorize_extensions: bool

    @staticmethod
    def from_dict(data: dict[str, any]) -> 'Category':
        return Category(
            name=data['name'],
            extensions=data['extensions'],
            categorize_extensions=data['categorize_extensions']
        )
    

    def to_dict(self) -> dict[str, any]:
        return {
            'name': self.name,
            'extensions': list(self.extensions),
            'categorize_extensions': self.categorize_extensions
        }
        

@dataclass
class Schedule:
    type: str
    interval: int
    active: bool


    @staticmethod
    def from_dict(data: dict[str, any]) -> 'Schedule':
        return Schedule(
            type=data['type'],
            interval=data['interval'],
            active=data['active']
        )
    

    def to_dict(self) -> dict[str, any]:
        return {
            'type': self.type,
            'interval': self.interval,
            'active': self.active
        }


@dataclass
class Config:
    active: bool
    directory: str
    categories: set[Category]
    schedule: Schedule


    @staticmethod
    def from_dict(data: dict[str, any]) -> 'Config':
        return Config(
            active=data['active'],
            directory=data['directory'],
            categories=[Category.from_dict(category) for category in data['categories']],
            schedule=Schedule.from_dict(data['schedule'])
        )
    

    def to_dict(self) -> dict[str, any]:
        return {
            'active': self.active,
            'directory': self.directory,
            'categories': [category.to_dict() for category in self.categories],
            'schedule': self.schedule.to_dict()
        }
    

    def dir_to_filename(self) -> str:
        """Convert a directory string to a filename-friendly string."""
        return self.directory.replace("/", "_")


    def has_valid_categories(self) -> bool:
        """
        Validates the Config categories
        """
        # Check if at least one category is specified.
        if not hasattr(self, 'categories') or not self.categories:
            LOG.warning("Config validation failed: No categories specified.")
            return False

        # Ensure categories have unique names.
        names = [category.name for category in self.categories]
        if len(names) != len(set(names)):
            LOG.warning("Config validation failed: Duplicate category names detected.")
            return False

        # Ensure categories have unique extensions.
        extensions = [ext for category in self.categories for ext in category.extensions]
        if len(extensions) != len(set(extensions)):
            LOG.warning("Config validation failed: Duplicate extensions detected across categories.")
            return False
        
        return True
    

    def has_valid_schedule(self) -> bool:
        """
        Validates the Config schedule
        """
        
        # Check for a schedule and its completeness, if it exists.
        if hasattr(self, 'schedule'):
            required_schedule_fields = ['type', 'interval', 'active']  # Add fields as necessary
            for field in required_schedule_fields:
                if not hasattr(self.schedule, field):
                    LOG.warning(f"Config validation failed: Missing field '{field}' in schedule.")
                    return False
        
        return True


    def is_valid(self) -> bool:
        """
        Validates the Config object.
        """
        # Check if the directory attribute exists and is not empty.
        if not hasattr(self, 'directory') or not self.directory:
            LOG.warning("Config validation failed: Missing directory.")
            return False
        
        if not self.has_valid_categories():
            return False
        
        if not self.has_valid_schedule():
            return False       

        return True


    def __eq__(self, other):
        if not isinstance(other, Config):
            return NotImplemented
        return self.directory == other.directory


    def __hash__(self):
        return hash(self.directory)
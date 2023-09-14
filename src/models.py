import logging
from dataclasses import dataclass, field

LOG = logging.getLogger(__name__)

@dataclass
class Category:
    """
    Represents a file categorization rule.
    
    Attributes:
        name (str): Name of the category.
        extensions (set[str]): File extensions associated with this category.
        categorize_extensions (bool): Whether to categorize the extensions. Default is False.
    """

    name: str
    extensions: set[str] = field(default_factory=set)
    categorize_extensions: bool = False

    @staticmethod
    def from_dict(data: dict[str, any]) -> 'Category':
        """Creates a Category instance from a dictionary."""
        return Category(
            name=data['name'],
            extensions=data['extensions'],
            categorize_extensions=data['categorize_extensions']
        )
    

    def to_dict(self) -> dict[str, any]:
        """Converts the Category instance to a dictionary."""
        return {
            'name': self.name,
            'extensions': list(self.extensions),
            'categorize_extensions': self.categorize_extensions
        }
        

@dataclass
class Schedule:
    """
    Represents a schedule for a task.
    
    Attributes:
        type (str): Type of the schedule interval (e.g., "MINUTE"). Default is "MINUTE".
        interval (int): Interval for the schedule. Default is 1.
        active (bool): Whether the schedule is active.
    """


    type: str = "MINUTE"
    interval: int = 1
    active: bool = bool


    @staticmethod
    def from_dict(data: dict[str, any]) -> 'Schedule':
        """Creates a Schedule instance from a dictionary."""
        return Schedule(
            type=data['type'],
            interval=data['interval'],
            active=data['active']
        )
    

    def to_dict(self) -> dict[str, any]:
        """Converts the Schedule instance to a dictionary."""
        return {
            'type': self.type,
            'interval': self.interval,
            'active': self.active
        }


@dataclass
class Config:
    """
    Represents a configuration for file organization.
    
    Attributes:
        directory (str): Directory to which the configuration applies.
        active (bool): Whether this configuration is active. Default is True.
        categories (set[Category]): Set of categories for file organization. Default is an empty set.
        schedule (Schedule): Schedule for the configuration. Default is a new Schedule instance.
    """

    directory: str
    active: bool = True
    categories: set[Category] = field(default_factory=set)
    schedule: Schedule = field(default_factory=Schedule)

    @staticmethod
    def from_dict(data: dict[str, any]) -> 'Config':
        """Creates a Config instance from a dictionary."""
        return Config(
            active=data['active'],
            directory=data['directory'],
            categories=[Category.from_dict(category) for category in data['categories']],
            schedule=Schedule.from_dict(data['schedule'])
        )
    

    def to_dict(self) -> dict[str, any]:
        """Converts the Config instance to a dictionary."""
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
        """Validates the categories in the Config."""
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
        """Validates the schedule in the Config."""
        
        # Check for a schedule and its completeness, if it exists.
        if hasattr(self, 'schedule'):
            required_schedule_fields = ['type', 'interval', 'active']  # Add fields as necessary
            for field in required_schedule_fields:
                if not hasattr(self.schedule, field):
                    LOG.warning(f"Config validation failed: Missing field '{field}' in schedule.")
                    return False
        
        return True


    def is_valid(self) -> bool:
        """Validates the entire Config object."""
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
        """Overrides the default equality method."""
        if not isinstance(other, Config):
            return NotImplemented
        return self.directory == other.directory


    def __hash__(self):
        """Overrides the default hash method."""
        return hash(self.directory)
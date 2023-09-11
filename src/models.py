from dataclasses import dataclass

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


    def __eq__(self, other):
        if not isinstance(other, Config):
            return NotImplemented
        return self.dir == other.dir


    def __hash__(self):
        return hash(self.dir)
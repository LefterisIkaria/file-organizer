from src.models.category import Category
from src.models.schedule.schedule import Schedule


class Config:

    def __init__(self, dir: str, categories: set[Category], schedule: Schedule, active: bool) -> None:
        self.dir = dir
        self.categories = categories
        self.schedule = schedule
        self.active = active
    

    def to_dict(self):
        return {
            'categories': {category.name: category.to_dict() for category in self.categories} if self.categories else {},
            'schedule': self.schedule.to_dict() if self.schedule else None,
            'active': self.active
        }
    
    @staticmethod
    def from_dict(dir: str, data: dict) -> 'Config':
        categories = {Category.from_dict(name, data) for name, data in data.get('categories', {}).items()}
        schedule = Schedule.from_dict(data.get('schedule', {}))
        active = data.get('active')
        return Config(
            dir=dir,
            categories=categories,
            schedule=schedule,
            active=active
        )
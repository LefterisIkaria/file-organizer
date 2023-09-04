from .category import Category
from .schedule.schedule import Schedule


class Config:
    def __init__(self, data: dict):
        self.dir = data.get("dir")
        self.categories = self._extract_categories(data.get("categories"))
        self.schedule = Schedule.from_dict(data.get("schedule"))
        self.active = data.get("active", False)

        self._validate()

    def _extract_categories(self, categories_data: dict) -> list[Category]:
        return [Category(name, data) for name, data in categories_data.items()]
    

    def _validate(self):
        # Validate directory path
        if not self.dir or not isinstance(self.dir, str) or self.dir.isspace():
            raise ValueError("Invalid or missing 'dir' in configuration.")

        # Validate categories
        if not self.categories or not isinstance(self.categories, list):
            raise ValueError(
                "'categories' must be a List of Category objects.")

        all_extensions = [
            ext for category in self.categories for ext in category.extensions]
        if len(all_extensions) != len(set(all_extensions)):
            raise ValueError("Duplicate extensions found across categories.")

        # Validate schedule
        if not self.schedule:
            raise ValueError("'schedule' must be a valid Schedule object.")

        # Validate active flag
        if not isinstance(self.active, bool):
            raise ValueError("'active' flag must be a boolean.")
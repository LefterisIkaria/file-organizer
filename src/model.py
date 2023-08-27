from typing import List, Dict


class Category:
    def __init__(self, name: str, data: Dict):
        self.name = name
        self.extensions = set(data.get("extensions", []))
        self.categorize_extensions = data.get("categorize_extensions", False)

        self._validate()

    def _validate(self):
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Invalid category name.")
        if not isinstance(self.extensions, set):
            raise ValueError("Extensions should be a set.")
        if not isinstance(self.categorize_extensions, bool):
            raise ValueError("Invalid value for categorize_extensions flag.")


class Config:
    def __init__(self, data: dict):
        self.dir = data.get("dir")
        self.categories = self._extract_categories(data.get("categories", []))
        self.schedule = data.get("schedule")
        self.active = data.get("active", False)

        self._validate()

    def _extract_categories(self, categories_data: dict) -> List[Category]:
        return [Category(name, data) for name, data in categories_data.items()]

    def _validate(self):
        # Validate directory path
        if not self.dir or not isinstance(self.dir, str) or self.dir.isspace():
            raise ValueError("Invalid or missing 'dir' in configuration.")

        # Validate categories
        if not self.categories or not isinstance(self.categories, List):
            raise ValueError(
                "'categories' must be a List of Category objects.")

        all_extensions = [
            ext for category in self.categories for ext in category.extensions]
        if len(all_extensions) != len(set(all_extensions)):
            raise ValueError("Duplicate extensions found across categories.")

        # Validate schedule
        # if not isinstance(self.schedule, dict):
            # raise ValueError("'schedule' must be a dictionary.")
        # if self.schedule.get("type") not in ["seconds", "minutes", "hours", "days"]:
            # raise ValueError("Invalid 'type' in schedule.")
        # if not isinstance(self.schedule.get("value"), int) or self.schedule.get("value") <= 0:
            # raise ValueError("'value' in schedule must be a positive integer.")

        # Validate active flag
        if not isinstance(self.active, bool):
            raise ValueError("'active' flag must be a boolean.")

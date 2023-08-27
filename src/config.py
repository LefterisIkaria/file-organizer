
class Config:
    def __init__(self, data: dict):
        # Basic properties from the config
        self.dir = data.get("dir")
        self.categories = data.get("categories", {})
        self.schedule = data.get("schedule")
        self.active = data.get("active", False)
        self.sort_extensions = data.get("sort_extensions", False)

        # Validate the configuration data
        self._validate()

    def _validate(self):
        # Validate directory path
        if not self.dir or not isinstance(self.dir, str):
            raise ValueError("Invalid or missing 'dir' in configuration.")

        # Validate categories
        if not isinstance(self.categories, dict):
            raise ValueError("'categories' must be a dictionary.")
        for category, extensions in self.categories.items():
            if not isinstance(category, str) or not isinstance(extensions, list):
                raise ValueError(
                    f"Invalid category or extensions for {category}.")

        # Additional validations can be added as needed

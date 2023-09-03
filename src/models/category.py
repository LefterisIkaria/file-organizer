class Category:
    def __init__(self, name: str, data: dict):
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




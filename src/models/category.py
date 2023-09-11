class Category:

    def __init__(self, name: str, extensions: set[str], categorize_extensions: bool) -> None:
        self.name = name
        self.extensions = extensions
        self.categorize_extensions = categorize_extensions


    def to_dict(self) -> dict:
        return {
            'extensions': list(self.extensions),
            'sort_extensions': self.categorize_extensions
        }
    
    @staticmethod
    def from_dict(name: str, data: dict) -> 'Category':
        return Category(
            name=name,
            extensions=set(data.get('extensions', [])),
            categorize_extensions=data.get('categorize_extensions', False)
        )
from typing import TypeVar

T = TypeVar("T")

class FilterResponse:
    def __init__(self, status: str, data: T, error: str = ""):
        self.status = status
        self.data = data
        self.error = error
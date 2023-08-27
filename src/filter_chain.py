from typing import List, TypeVar, Generic
from abc import ABC, abstractmethod
from model import Config


T = TypeVar("T")


class FilterResponse:
    def __init__(self, status: str, data: T, error: str = ""):
        self.status = status
        self.data = data
        self.error = error


class Filter(Generic[T], ABC):

    @abstractmethod
    def do_filter(self, input: T, chain: 'FilterChain') -> FilterResponse:
        pass


class FilterChain:
    def __init__(self, filters: List[Filter[T]]):
        self.filters = filters
        self.index = 0

    def execute(self, input: T) -> FilterResponse:
        return self.next(input)

    def next(self, input: T) -> FilterResponse:
        if self.index < len(self.filters):
            filter = self.filters[self.index]
            self.index += 1
            return filter.do_filter(input, self)
        return FilterResponse("success", "Directory organized successfully")

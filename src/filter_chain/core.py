from typing import TypeVar, Generic
from abc import ABC, abstractmethod

from .filter_response import FilterResponse

T = TypeVar("T")

class Filter(Generic[T], ABC):

    priority: int = 0

    @abstractmethod
    def do_filter(self, input: T, chain: 'FilterChain') -> FilterResponse:
        pass


class FilterChain:
    def __init__(self, filters: list[Filter[T]]):
        self.filters = sorted(filters, key=lambda x: x.priority)
        self.index = 0

    def execute(self, input: T) -> FilterResponse:
        return self.next(input)

    def next(self, input: T) -> FilterResponse:
        if self.index < len(self.filters):
            filter = self.filters[self.index]
            self.index += 1
            return filter.do_filter(input, self)
        return FilterResponse("success", "Directory organized successfully")

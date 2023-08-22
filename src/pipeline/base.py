from typing import TypeVar, Generic, List, Any

I = TypeVar("I")
O = TypeVar("O")


class Filter(Generic[I, O]):
    def process(self, input: I) -> O:
        raise NotImplementedError


class Pipeline:
    def __init__(self):
        self.filters: List[Filter] = []

    def add_filter(self, filter: Filter) -> None:
        self.filters.append(filter)

    def run(self, data: Any) -> Any:
        for filter in self.filters:
            data = filter.process(data)
        return data

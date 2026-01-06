from abc import ABC , abstractmethod


class RunInterface(ABC):
    def run(self) -> None:
        pass
from abc import ABC , abstractmethod


class RunInterface(ABC):
    @abstractmethod
    def run(self) -> None:
        pass
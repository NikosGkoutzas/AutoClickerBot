from abc import ABC , abstractmethod



class ChromeBootInterface(ABC):
    @abstractmethod
    def boot(self) -> None:
        pass
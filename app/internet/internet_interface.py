from abc import ABC , abstractmethod



class InternetInterface(ABC):
    @abstractmethod
    def check_for_internet_connection(self) -> bool:
        pass
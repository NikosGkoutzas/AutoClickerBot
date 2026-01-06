from abc import ABC , abstractmethod



class InternetInterface(ABC):
    @abstractmethod
    def check_and_wait_for_internet_connection(self) -> bool:
        pass
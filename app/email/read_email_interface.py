from abc import ABC , abstractmethod



class ReadEmailInterface(ABC):    
    @abstractmethod
    def fetch_last_emails(self) -> None:
        pass
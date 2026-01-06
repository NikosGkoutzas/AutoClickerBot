from abc import ABC , abstractmethod
import email



class ReadEmailInterface(ABC):    
    @abstractmethod
    def fetch_last_emails(self) -> None:
        pass
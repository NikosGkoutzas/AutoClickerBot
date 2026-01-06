from abc import ABC , abstractmethod
from datetime import datetime



class CalculationInterface(ABC):
    @abstractmethod
    def app_in_time(self) -> bool:
        pass


    @abstractmethod
    def updates_completed(self) -> bool:
        pass


    @abstractmethod
    def extract_update_results(self) -> str:
        pass


    @abstractmethod
    def sleep_till_next_day(self) -> None:
        pass

    
    @abstractmethod
    def list_of_all_machines(self) -> str:
        pass
    
    
    @abstractmethod
    def compute_time_of_new_version_installation(self) -> datetime.time:
        pass
    
    
    @abstractmethod
    def delay_between_updates(self) -> int:
        pass
    
    
    @abstractmethod
    def check_emails(self) -> bool:
        pass
    
    
    @abstractmethod
    def updates_completed_earlier_wait(self) -> None:
        pass
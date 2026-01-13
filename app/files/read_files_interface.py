from abc import ABC , abstractmethod
import datetime


class ReadFilesInterface(ABC):
    @abstractmethod
    def can_app_run_at_current_time(self) -> bool:
        pass


    @abstractmethod
    def general_read_int(self , filename: str) -> int:
        pass


    @abstractmethod
    def read_number_of_urls(self) -> int:
        pass

    
    @abstractmethod
    def read_app_version(self) -> str:
        pass
    

    @abstractmethod
    def read_url_current_pos(self) -> int:
        pass


    @abstractmethod
    def read_url_from_current_pos(self) -> str:
        pass


    @abstractmethod
    def read_delay_per_update(self) -> float:
        pass


    @abstractmethod
    def read_total_updates(self) -> int:
        pass


    @abstractmethod
    def read_total_errors(self) -> int:
        pass


    @abstractmethod
    def read_number_of_removed_machines(self) -> int:
        pass


    @abstractmethod
    def read_number_of_inserted_machines(self) -> int:
        pass

    
    @abstractmethod
    def read_every_url(self) -> list[str]:
        pass


    @abstractmethod
    def read_update_number_of_machine(self) -> list[int]:
        pass


    @abstractmethod
    def read_number_of_github_updates(self) -> int:
        pass


    @abstractmethod
    def read_error_datetime(self) -> datetime.datetime | None:
        pass


    @abstractmethod
    def check_errors_occurred_10(self) -> bool:
        pass


    @abstractmethod
    def read_progress_number(self) -> int:
        pass


    @abstractmethod
    def read_start_time(self) -> datetime.datetime:
        pass


    @abstractmethod
    def read_end_time(self) -> datetime.datetime:
        pass
        
        
    @abstractmethod
    def read_datetime_general(self , filename: str) -> datetime.datetime:
        pass
    
    
    @abstractmethod
    def read_time_general(self , filename: str) -> datetime.time:
        pass
    
    
    @abstractmethod
    def read_email_dates(self) -> list[str]:
        pass
    
    
    @abstractmethod
    def read_app_started(self) -> bool:
        pass
    
    
    @abstractmethod
    def read_app_ended(self) -> bool:
        pass
    
    
    @abstractmethod
    def read_number_of_captcha_challenges(self) -> int:
        pass
    
    
    @abstractmethod
    def read_check_email_every_20_minutes(self) -> datetime.time:
        pass
    
    
    @abstractmethod
    def read_daily_report_sent(self) -> int:
        pass
from abc import ABC , abstractmethod



class WriteFilesInterface(ABC):
    @abstractmethod
    def compute_delay_between_updates(self) -> None:
        pass


    @abstractmethod
    def general_write_int(self , filename: str) -> None:
        pass


    @abstractmethod
    def write_url_current_pos(self) -> None:
        pass

    
    @abstractmethod
    def write_app_version(self , semantic_versioning: str) -> None:
        pass
    
    
    @abstractmethod
    def write_new_version_update_flag(self , flag: int) -> None:
        pass

    @abstractmethod
    def write_delay_per_update(self , delay: int) -> None:
        pass


    @abstractmethod
    def write_total_updates(self) -> None:
        pass


    @abstractmethod
    def write_total_errors(self) -> None:
        pass


    @abstractmethod
    def write_number_of_removed_machines(self) -> None:
        pass


    @abstractmethod
    def write_number_of_inserted_machines(self) -> None:
        pass


    @abstractmethod
    def write_update_number_of_machine(self , line: int) -> None:
        pass


    @abstractmethod
    def write_number_of_github_updates(self) -> None:
        pass
    
    
    @abstractmethod
    def write_time_general(self , filename: str , dt: str) -> None:
        pass


    @abstractmethod
    def write_internet_error_date(self , dt: str) -> None:
        pass


    @abstractmethod
    def write_progress_number(self) -> None:
        pass


    @abstractmethod
    def add_machine(self , url_link: str) -> None:
        pass


    @abstractmethod
    def remove_machine(self , url_link: str) -> None:
        pass
    
    
    @abstractmethod
    def write_email_dates(self , dt: str) -> None:
        pass
    
    
    @abstractmethod
    def write_number_in_file(self , filename , number) -> None:
        pass
    
    
    @abstractmethod
    def write_app_started(self) -> None:
        pass
    
    
    @abstractmethod
    def write_app_ended(self) -> None:
        pass
    
    
    @abstractmethod
    def write_number_of_captcha_challenge(self) -> None:
        pass
    
    
    @abstractmethod
    def write_check_email_every_20_minutes(self) -> None:
        pass
    
    
    @abstractmethod
    def reset_all_updates_per_machine(self) -> None:
        pass
    
    
    @abstractmethod
    def reset_all_files(self) -> None:
        pass
    
    
    @abstractmethod
    def update_credentials_from_env(self , new_username: str | None , new_password: str | None) -> None:
        pass
    
    
    @abstractmethod
    def write_daily_report_sent(self) -> None:
        pass
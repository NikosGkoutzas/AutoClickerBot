from abc import ABC , abstractmethod



class WriteFilesInterface(ABC):
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
    def write_last_internet_error_time(self , dt: str) -> None:
        pass
    
    
    @abstractmethod
    def write_internet_errors(self) -> None:
        pass
    

    @abstractmethod
    def write_number_of_removed_machines(self , number: int) -> None:
        pass


    @abstractmethod
    def write_number_of_inserted_machines(self , number: int, geiaaaaaaaaaaaa:str) -> None:
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
    def write_error_time(self , dt: str) -> None:
        pass
    
    
    @abstractmethod
    def write_last_internet_error_time(self , dt: str) -> None:
        pass


    @abstractmethod
    def add_machine(self , url_link: str) -> None:
        pass


    @abstractmethod
    def remove_machine(self , url_link: str) -> None:
        pass
    
    
    @abstractmethod
    def write_email_uids(self , email_uid: bytes) -> None:
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
    def update_credentials_from_env(self , new_username: str | None , new_password: str | None) -> None:
        pass
    
    
    @abstractmethod
    def write_daily_report_sent(self , value: int) -> None:
        pass
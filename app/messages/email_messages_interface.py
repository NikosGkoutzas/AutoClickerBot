from abc import ABC , abstractmethod
from datetime import datetime


class EmailMessagesInterface(ABC):
    @abstractmethod
    def time_message(self) -> str:
        pass
    
    
    @abstractmethod
    def built_with_python_and_copyright_message(self) -> str:
        pass
    
    
    @abstractmethod
    def launch_app_title_message(self) -> str:
        pass
    
    
    @abstractmethod
    def launch_app_body_message(self) -> str:
        pass
    
    
    @abstractmethod
    def no_internet_title_message(self) -> str:
        pass
    
    
    @abstractmethod
    def no_internet_body_message(self , occured: str , restored: str):
        pass
    
    @abstractmethod
    def daily_report_title_message(self) -> str:
        pass


    @abstractmethod
    def daily_report_body_message(self ,
                                  total_updates_of_day: int ,
                                  total_issues: int ,
                                  total_machines: int ,
                                  inserted_machines: int ,
                                  removed_machines: int ,
                                  updated_result: str) -> str:
        pass


    @abstractmethod
    def new_version_started_title_message(self) -> str:
        pass
    
    
    @abstractmethod
    def new_version_started_body_message(self) -> str:
        pass
    
    
    @abstractmethod
    def credentails_update_title_message(self , cond_str: str) -> str:
        pass
    
    
    @abstractmethod
    def credentials_update_body_message(self , cond_str: str) -> str:
        pass
    
    
    @abstractmethod
    def progress_title_message(self) -> str:
        pass
    
    
    @abstractmethod
    def progress_body_message(self ,
                              number_of_machines: int ,
                              current_updates: int ,
                              current_errors: int ,
                              most_recent_error: str ,
                              added_machines: int ,
                              removed_machines: int ,
                              progress_body_message: int ,
                              version: str
                              ) -> str:
        pass
    
    
    @abstractmethod
    def machine_inserted_title_message(self , number_of_inserted_machines: int , invalid_machines: list[str]) -> str:
        pass
    
    
    @abstractmethod
    def machine_inserted_body_message(self , list_of_added_machines: list[str] , not_existing_machines: list[str] , number_of_machines: int) -> str:
        pass
    
    
    @abstractmethod
    def machine_removed_title_message(self , number_of_removed_machines: int , not_existing_machines: list[str]) -> str:
        pass
    
    
    @abstractmethod
    def machine_removed_body_message(self , list_of_removed_machines: list[str] , not_existing_machines: list[str] , number_of_machines: int) -> str:
        pass
    
    
    @abstractmethod
    def install_new_version_title_message(self) -> str:
        pass
    
    
    @abstractmethod
    def install_new_version_body_message(self , new_version: str , new_time: datetime.time) -> str:
        pass
    
    
    @abstractmethod
    def see_all_available_links_title_message(self) -> str:
        pass
    
    
    @abstractmethod
    def see_all_available_links_body_message(self , list_of_all_machines: str) -> str:
        pass
    
    
    @abstractmethod
    def unable_to_login_title_message(self) -> str:
        pass
    
    
    @abstractmethod
    def unable_to_login_body_message(self) -> str:
        pass
    
    
    @abstractmethod
    def captcha_failed_to_solve_title_message(self) -> str:
        pass
    
    
    @abstractmethod
    def captcha_failed_to_solve_body_message(self) -> str:
        pass
    
    
    @abstractmethod
    def notify_every_10_errors_title_message(self) -> str:
        pass
    
    
    @abstractmethod
    def notify_every_10_errors_body_message(self , errors: int) -> str:
        pass
    
    
    @abstractmethod
    def connect_via_rustdesk_title_message(self) -> str:
        pass
    
    
    @abstractmethod
    def connect_via_rustdesk_body_message(self) -> str:
        pass
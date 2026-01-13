from abc import ABC , abstractmethod


class SendEmailInterface(ABC):
    @abstractmethod
    def send_email_launch(self) -> None:
        pass


    @abstractmethod
    def send_email_no_internet_connection(self , occured: str , restored: str) -> None:
        pass


    @abstractmethod
    def send_email_daily_report(self) -> None:
        pass


    @abstractmethod
    def send_email_link_inserted(self , list_added_links: list[str] , list_added_invalied_links: list[str]) -> None:
        pass


    @abstractmethod
    def send_email_link_removed(self , list_removed_links: list[str] , list_removed_invalied_links: list[str]) -> None:
        pass


    @abstractmethod
    def send_email_new_version_updated(self) -> None:
        pass


    @abstractmethod
    def send_email_credentials_updated(self , cond_str: str) -> None:
        pass


    @abstractmethod
    def send_email_progress(self) -> None:
        pass
    
    
    @abstractmethod
    def send_email_install_new_version(self , success: bool) -> None:
        pass
    
    
    @abstractmethod
    def send_email_all_links(self) -> None:
        pass
    
    
    @abstractmethod
    def send_email_unable_to_login(self) -> None:
        pass
    
    
    @abstractmethod
    def send_email_captcha_failed_to_solve(self) -> None:
        pass
    
    
    @abstractmethod
    def send_email_every_10_errors_occured(self , errors: int) -> None:
        pass
    
    
    @abstractmethod
    def send_email_connect_via_rustdesk(self) -> None:
        pass
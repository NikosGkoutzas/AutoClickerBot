from abc import ABC , abstractmethod


class DriverInterface(ABC):
    @abstractmethod
    def start_driver(self) -> None:
        pass
    
    
    @abstractmethod
    def quit_driver(self) -> None:
        pass
    
    
    @abstractmethod
    def login(self) -> int:
        pass
    
    
    @abstractmethod
    def logout(self) -> None:
        pass
    

    @abstractmethod
    def update_machine(self , url_link: str) -> int:
        pass
    
    
    @abstractmethod
    def is_captcha_active_before_login_credentials(self) -> int:
        pass
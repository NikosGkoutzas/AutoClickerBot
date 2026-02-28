from abc import ABC , abstractmethod



class ActionInterface(ABC):
    @abstractmethod
    def update_machine_procedure(self) -> None:
        pass
    
    
    @abstractmethod
    def check_login(self) -> None:
        pass
    
    
    @abstractmethod
    def latest_version_available(self) -> bool:
        pass
    
    
    @abstractmethod
    def open_teamviewer(self) -> None:
        pass
    
    
    @abstractmethod
    def close_teamviewer(self) -> None:
        pass
    
    
    @abstractmethod
    def check_if_teamviewer_is_already_connected(self) -> bool:
        pass
    
    
    @abstractmethod
    def check_if_teamviewer_is_already_disconnected(self) -> bool:
        pass
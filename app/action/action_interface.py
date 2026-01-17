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
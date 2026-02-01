from abc import ABC , abstractmethod


class ResetFilesInterface(ABC):
    @abstractmethod
    def reset_all_files():
        pass
    
    
    @abstractmethod
    def reset_all_updates_per_machine(self) -> None:
        pass
    
    
    @abstractmethod
    def reset_total_updates(self) -> None:
        pass
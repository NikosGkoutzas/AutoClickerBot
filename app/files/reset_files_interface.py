from abc import ABC, abstractmethod


class ResetFilesInterface(ABC):
    @abstractmethod
    def reset_all_files(self) -> None:
        pass

    @abstractmethod
    def reset_all_updates_per_machine(self) -> None:
        pass

    @abstractmethod
    def reset_total_updates(self) -> None:
        pass

    @abstractmethod
    def reset_app_started(self) -> None:
        pass

    @abstractmethod
    def reset_app_ended(self) -> None:
        pass

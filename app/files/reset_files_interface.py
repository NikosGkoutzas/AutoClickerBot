from abc import ABC , abstractmethod


class ResetFilesInterface(ABC):
    @abstractmethod
    def reset_all_files():
        pass
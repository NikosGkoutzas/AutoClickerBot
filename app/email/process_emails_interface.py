from abc import ABC , abstractmethod


class ProcessEmailsInterface(ABC):
    @abstractmethod
    def process_add_link_email(self , list_added_links: list[str]) -> tuple[list[str] , list[str]]:
        pass
    
    
    @abstractmethod
    def process_remove_link_email(self , list_removed_links: list[str]) -> tuple[list[str] , list[str]]:
        pass
    
    
    @abstractmethod
    def process_change_credentials_email(self , list_changed_credentials: list[str]) -> str:
        pass
    
    
    @abstractmethod
    def process_new_version_email(self , list_semantic_versioning: list[str]) -> tuple[bool , str]:
        pass
    

    @abstractmethod
    def download_new_version_from_github(self , semantic_input: str) -> bool:
        pass
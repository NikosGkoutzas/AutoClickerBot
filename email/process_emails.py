from .process_emails_interface import ProcessEmailsInterface
from ..files.read_files_interface import ReadFilesInterface
from ..files.write_files_interface import WriteFilesInterface
import inject , os



class ProcessEmails(ProcessEmailsInterface):
    #@inject.autoparams()
    def __init__(self , read_files_interface: ReadFilesInterface , write_files_interface: WriteFilesInterface):
        self.read_files = read_files_interface
        self.write_files = write_files_interface



    def process_add_link_email(self , list_added_links: list[str]) -> tuple[list[str] , list[str]]:
        invalid_links = []
        valid_links = []

        for link in list_added_links:
            if(link in self.read_files.read_every_url() or (
                not link.startswith('https://www.car.gr/xyma/view/') or not link.endswith('electronord-gr'))):
                    invalid_links.append(link)
            
            else:
                self.write_files.add_machine(link)
                valid_links.append(link)
        
        return valid_links , invalid_links
                
                
                
                

    
    def process_remove_link_email(self , list_removed_links: list[str]) -> tuple[list[str] , list[str]]:
        invalid_links = []
        valid_links = []

        for link in list_removed_links:
            if(link not in self.read_files.read_every_url() or (
                not link.startswith('https://www.car.gr/xyma/view/') or not link.endswith('electronord-gr'))):
                    invalid_links.append(link)
            
            else:
                self.write_files.remove_machine(link)
                valid_links.append(link)
        
        return valid_links , invalid_links
    
    
    
    
    
    def process_change_credentials_email(self , list_changed_credentials: list[str]) -> str:        
        if(not (len(list_changed_credentials) == 1 or len(list_changed_credentials) == 2) ):
            return 'Please ensure your request includes one or two credential updates: username or password.'    
            
            
        old_username = os.getenv('site_username')
        old_password = os.getenv('site_password')
        new_username = None
        new_password = None
        
        for cred in list_changed_credentials:
            name , value = cred.split(':' , 1)
            name = name.strip().lower()
            value = value.strip()
            
            if(name == 'username'):
                if(old_username == value):
                    return 'The new username matches the existing username and cannot be applied.'
                
                if(new_username is not None):
                    return 'The username was provided more than once in the request.'
                    
                else:
                    new_username = value               
                
            if(name == 'password'):
                if(old_password == value):
                    return 'The new password matches the existing username and cannot be applied.'
                
                if(new_password is not None):
                    return 'The password was provided more than once in the request.'
                    
                else:
                    new_password = value 
                            
        if(new_username is None and new_password is None): 
            return 'Your request does not include a username or password update.'
            
        
        # change credentials in .env file
        self.write_files.update_credentials_from_env(new_username if new_username is not None else None ,
                                                     new_password if new_password is not None else None)
        return 'Ok'
    
    
    
    
    
    def process_new_version_email(self , list_semantic_versioning: list[str]) -> tuple[bool , str]:
        
        if(list_semantic_versioning and list_semantic_versioning[0].strip().lower() in ['major' , 'minor' , 'patch']):
            return True , list_semantic_versioning[0].strip().lower()
        
        return False , None